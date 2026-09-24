#!/usr/bin/env python3
"""Bring a knowledge base's frontmatter to the 0.17 format.

Usage:  kb_migrate.py [--apply]

Dry run by default: prints, per file, what would change. `--apply` rewrites the
frontmatter, and the agent-block fences in the body. Run it on a base under
git, so the result can be reviewed as a diff.

1. `origin` and `generated` become `authored` (`machine` → `agent`) and `date`.
2. `verified` and `approved` become `status`: `stable` with either of them is
   `confirmed`, `deprecated` and `abandoned` are both `retired`. A legacy
   `verified` list counts the same way.
3. `sources` becomes `from` (items by `kb:<id>`, outside documents by URL),
   plus `code: <repository url>@<commit>` and `paths`. `symbol`, `symbols` and
   `retrieved` are dropped. **An item citing more than one repository keeps the
   first and reports the rest** — the format now holds one.
4. `<!-- machine: ... -->` fences become `<!-- agent -->`.

Keys are rewritten in the schema's order. A file whose frontmatter holds a
comment is reported and skipped, since rewriting would lose it. Every rewritten
block is parsed back and compared with what was intended before anything is
written. Running it twice changes nothing the second time.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_export import (  # noqa: E402
    ID_SCHEME,
    INIT,
    items_by_id,
    read_items,
    resolve_kb,
    resolve_resource,
    split_frontmatter,
)

import yaml  # noqa: E402  (kb_export already required it)


class Loader(yaml.SafeLoader):
    """Timestamps and dates stay strings, so they are written back as read."""


Loader.yaml_implicit_resolvers = {
    key: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


STAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2}))?$")
ORDER = ("id", "type", "title", "authored", "date", "status", "importance",
         "from", "code", "paths")
STATUS = {"stable": "confirmed", "deprecated": "retired", "abandoned": "retired"}
REPO_KEYS = ("path", "paths", "symbol", "symbols", "commit")
OPEN_RE = re.compile(r"^<!-- machine:[^\n]*-->[ \t]*$", re.M)
CLOSE_RE = re.compile(r"^<!-- /machine -->[ \t]*$", re.M)


def scalar(value):
    # Written bare, as the base writes them; quoting would be noise.
    if isinstance(value, str) and STAMP_RE.match(value):
        return value
    text = yaml.safe_dump(value, default_flow_style=True, width=10**6, allow_unicode=True)
    return text.strip().removesuffix("...").strip()


def flow(value):
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{k}: {flow(v)}" for k, v in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(flow(v) for v in value) + "]"
    return scalar(value)


def emit(meta):
    """Frontmatter in the schema's key order, one line each."""
    keys = [k for k in ORDER if k in meta] + [k for k in meta if k not in ORDER]
    return "\n".join(f"{key}: {flow(meta[key])}" for key in keys)


def day(value):
    """The date out of a timestamp, however PyYAML handed it over."""
    text = str(value)
    return text[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", text) else None


def settled(meta):
    """Whether anything ever checked or approved this item."""
    return bool(meta.get("approved")) or bool(meta.get("verified"))


def convert_sources(kb, meta, by_id, originals, changes):
    sources = meta.pop("sources", None)
    if not isinstance(sources, list):
        return
    refs, code, paths, extra = [], None, [], []
    for entry in sources:
        if not isinstance(entry, dict):
            continue
        resource = str(entry.get("resource", ""))
        if resource.startswith(ID_SCHEME):
            refs.append(resource)
        elif resource.startswith("/"):
            target = resolve_resource(kb, resource, by_id)
            if target and originals[target].get("id"):
                refs.append(ID_SCHEME + str(originals[target]["id"]))
            else:
                refs.append(resource)
                changes.append(f"UNRESOLVED {resource} (left in `from`)")
        elif any(key in entry for key in REPO_KEYS):
            these = entry.get("paths") or ([entry["path"]] if "path" in entry else [])
            if code is None:
                code = f"{resource}@{entry['commit']}" if entry.get("commit") else resource
                paths = [str(p) for p in these]
            else:
                extra.append(resource)
        else:
            refs.append(resource)
    if refs:
        meta["from"] = refs
    if code:
        meta["code"] = code
    if paths:
        meta["paths"] = paths
    changes.append(f"sources → from {len(refs)}, code {'yes' if code else 'no'}")
    for resource in extra:
        changes.append(f"DROPPED second repository {resource} — one per item now")


def migrate(kb, path, meta, by_id, originals, changes):
    origin = meta.pop("origin", None)
    if origin is not None:
        meta["authored"] = "agent" if origin == "machine" else str(origin)
        changes.append(f"origin: {origin} → authored: {meta['authored']}")

    generated = meta.pop("generated", None)
    if "date" not in meta and isinstance(generated, dict):
        when = day(generated.get("at"))
        if when:
            meta["date"] = when
            changes.append(f"generated.at → date: {when}")

    old = str(meta.get("status", ""))
    if old in STATUS:
        meta["status"] = STATUS[old] if old != "stable" or settled(meta) else "draft"
        changes.append(f"status: {old} → {meta['status']}")
    for key in ("verified", "approved"):
        if meta.pop(key, None) is not None:
            changes.append(f"{key} dropped")

    convert_sources(kb, meta, by_id, originals, changes)


def retag(body, changes):
    body, opened = OPEN_RE.subn("<!-- agent -->", body)
    body, closed = CLOSE_RE.subn("<!-- /agent -->", body)
    if opened or closed:
        changes.append(f"{opened} agent block(s) refenced")
    return body


def main(argv):
    apply = argv == ["--apply"]
    if argv and not apply:
        print(__doc__.strip())
        return 2
    kb = resolve_kb()
    if not kb:
        print(f"kb_migrate: no knowledge base found ({INIT} makes one)")
        return 1

    raw, metas = {}, {}
    for path, _, _ in read_items(kb):
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        block, _ = split_frontmatter(text)
        meta = yaml.load(block, Loader=Loader)
        if isinstance(meta, dict):
            raw[path], metas[path] = (text, block), meta
    by_id = items_by_id((p, m, None) for p, m in metas.items())

    # Resolve against the original frontmatter throughout, so the order files
    # are visited in cannot change what a reference resolves to.
    originals = {p: yaml.load(raw[p][1], Loader=Loader) for p in metas}
    touched = 0
    for path in sorted(metas):
        text, block = raw[path]
        if re.search(r"(^|\s)#", block, re.M):
            print(f"{os.path.relpath(path, kb)}: skipped — frontmatter holds a comment")
            continue
        meta = yaml.load(block, Loader=Loader)
        changes = []
        migrate(kb, path, meta, by_id, originals, changes)
        tail = retag(text[4 + len(block):], changes)
        if not changes:
            continue
        touched += 1
        print(os.path.relpath(path, kb))
        for change in changes:
            print(f"  {change}")
        new_block = emit(meta)
        if yaml.load(new_block, Loader=Loader) != meta:
            print("  ERROR: rewritten frontmatter does not read back the same; not written")
            continue
        if apply:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("---\n" + new_block + tail)

    verb = "rewrote" if apply else "would rewrite"
    print(f"kb_migrate: {verb} {touched} file(s)" + ("" if apply else " — --apply to write"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
