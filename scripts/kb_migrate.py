#!/usr/bin/env python3
"""Bring a knowledge base's frontmatter to the 0.14 format.

Usage:  kb_migrate.py [--apply]

Dry run by default: prints, per file, what would change. `--apply` rewrites
only the frontmatter of the files that change; bodies are never touched. Run
it on a base under git, so the result can be reviewed as a diff.

1. A `sources` entry naming an item by base-relative path becomes `kb:<id>`.
2. A `verified` list becomes its latest non-human entry. A `human:` entry in
   it was approval before the two were split: it becomes `approved` where the
   item has none.
3. A note drops evidence entries that repeat one of its captures' — evidence
   is recorded once, where it was read. Only exact repeats go; anything the
   note was checked against beyond its captures stays.

A file whose frontmatter holds a comment is reported and skipped, since
rewriting would lose it. Every rewritten block is parsed back and compared
with what was intended before anything is written.
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


def scalar(value):
    # Written bare, as the base writes them; quoting would be noise.
    if isinstance(value, str) and STAMP_RE.match(value):
        return value
    text = yaml.safe_dump(value, default_flow_style=True, width=10**6)
    return text.strip().removesuffix("...").strip()


def flow(value):
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{k}: {flow(v)}" for k, v in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(flow(v) for v in value) + "]"
    return scalar(value)


def emit(meta):
    """Frontmatter in the house style: flow mappings for stamps, one block
    entry per source."""
    lines = []
    for key, value in meta.items():
        if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
            lines.append(f"{key}:")
            for entry in value:
                for i, (k, v) in enumerate(entry.items()):
                    lines.append(f"{'  - ' if i == 0 else '    '}{k}: {flow(v)}")
        else:
            lines.append(f"{key}: {flow(value)}")
    return "\n".join(lines)


def is_human(entry):
    return isinstance(entry, dict) and str(entry.get("by", "")).startswith("human:")


def evidence_key(entry):
    return tuple(sorted((k, str(v)) for k, v in entry.items()))


def migrate(kb, path, meta, by_id, metas):
    changes = []
    sources = meta.get("sources")
    if isinstance(sources, list):
        for entry in sources:
            if not isinstance(entry, dict):
                continue
            resource = str(entry.get("resource", ""))
            if resource.startswith("/"):
                target = resolve_resource(kb, resource, by_id)
                if target and metas[target].get("id"):
                    entry["resource"] = ID_SCHEME + str(metas[target]["id"])
                    changes.append(f"{resource} → {entry['resource']}")
                else:
                    changes.append(f"UNRESOLVED {resource} (left as is)")

    verified = meta.get("verified")
    if isinstance(verified, list):
        machine = [e for e in verified if isinstance(e, dict) and not is_human(e)]
        human = [e for e in verified if is_human(e)]
        if machine:
            meta["verified"] = machine[-1]
        else:
            del meta["verified"]
        if human and "approved" not in meta:
            meta["approved"] = human[-1]
            changes.append(f"approved ← {human[-1].get('by')}")
        changes.append(f"verified: {len(verified)} entries → {1 if machine else 0}")

    if meta.get("type") == "Note" and isinstance(sources, list):
        inherited = set()
        for entry in sources:
            target = resolve_resource(kb, entry.get("resource"), by_id) if isinstance(entry, dict) else None
            if target:
                for e in metas[target].get("sources") or []:
                    if isinstance(e, dict) and not str(e.get("resource", "")).startswith(("/", ID_SCHEME)):
                        inherited.add(evidence_key(e))
        kept = [
            e for e in sources
            if not (isinstance(e, dict) and evidence_key(e) in inherited)
        ]
        if len(kept) != len(sources):
            changes.append(f"evidence repeated from captures dropped: {len(sources) - len(kept)}")
            meta["sources"] = kept
    return changes


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
        changes = migrate(kb, path, meta, by_id, originals)
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
                handle.write("---\n" + new_block + text[4 + len(block):])

    verb = "rewrote" if apply else "would rewrite"
    print(f"kb_migrate: {verb} {touched} file(s)" + ("" if apply else " — --apply to write"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
