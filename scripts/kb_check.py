#!/usr/bin/env python3
"""Check knowledge-base frontmatter against ../reference/schema.md.

Usage:  kb_check.py <file-or-directory>...

Reports one line per problem and exits 1 if any is an error. Warnings do not
affect the exit code. Requires PyYAML; without it the check is skipped rather
than failed, since it is an aid and never a gate.

Deliberately mechanical. It checks the shape of the frontmatter — keys that
must be present, values that must parse — plus that agent blocks in the body
open and close in turn, and nothing that depends on where an item lives. Types
are open (OKF permits any) and the layout is free to change, so a checker that
enumerated either would be wrong before it was useful. Everything about meaning
is the reader's job.

It looks beyond a file for two things. Identity: a `kb:<id>` in `from` must
name exactly one item in the enclosing base, and no other item may share the
file's own `id`. And staleness: a `confirmed` note whose slug pool holds a
human capture the note does not list has a dictated claim that never reached
it.
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    print("kb_check: PyYAML not installed — frontmatter check skipped")
    sys.exit(0)

AUTHORS = {"human", "agent"}
STATUSES = {"draft", "confirmed", "retired"}
# Two shapes (see the schema): an item that stays in the base is
# `<slug>_<n>`, no date — a card, which leaves the base, is twelve random
# base62 characters instead. A slug ending in a number is indistinguishable
# from a suffix here, which is why the check is a shape and not a guarantee
# of uniqueness.
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
ID_RE = re.compile(rf"^(?:{SLUG}_\d+|[A-Za-z0-9]{{12}})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A repository by URL, then the commit the claims were checked against.
CODE_RE = re.compile(r"^https?://\S+@\S+$")
REQUIRED = ("id", "type", "title", "authored", "date", "status")
# A soft budget: past it, frontmatter is usually carrying copied evidence or
# history that belongs elsewhere.
FRONTMATTER_LINES = 12

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_export import ID_SCHEME, items_by_id, read_items  # noqa: E402

_bases = {}


def base_of(path):
    """The knowledge base enclosing a file — the nearest SCHEMA.md above it."""
    directory = os.path.dirname(os.path.abspath(path))
    while directory != os.path.dirname(directory):
        if os.path.isfile(os.path.join(directory, "SCHEMA.md")):
            return directory
        directory = os.path.dirname(directory)
    return None


def base(kb):
    """(every item's paths by ID, every item's frontmatter by ID)."""
    if kb not in _bases:
        items = list(read_items(kb))
        metas = {str(m.get("id", "")): m for _, m, _ in items}
        _bases[kb] = (items_by_id(items), metas)
    return _bases[kb]


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    return None if end < 0 else text[4:end]


def check_blocks(problems, body):
    """Agent blocks must open and close in turn; an unclosed one would
    swallow the user's claims, a stray close would leak the agent's."""
    depth = 0
    for match in re.finditer(r"^<!-- (/?agent) -->\s*$", body, re.M):
        if match.group(1) == "agent":
            if depth:
                problems.append(("error", "agent block opened inside another"))
            depth = 1
        else:
            if not depth:
                problems.append(("error", "agent block closed but never opened"))
            depth = 0
    if depth:
        problems.append(("error", "agent block never closed"))


def check_strings(problems, meta, key):
    """A flat list of strings, which `from` and `paths` both are."""
    value = meta[key]
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        problems.append(("error", f"`{key}` must be a list of strings"))
        return False
    return True


def check_from(problems, meta, kb):
    if not check_strings(problems, meta, "from"):
        return
    for resource in meta["from"]:
        if resource.startswith(ID_SCHEME):
            if kb:
                found = len(base(kb)[0].get(resource[len(ID_SCHEME):]) or [])
                if found != 1:
                    problems.append(("error", f"`{resource}` names {found} items"))
        elif not resource.startswith("http"):
            problems.append(
                ("error", f"`from` entry {resource!r} is not `kb:<id>` or a URL")
            )


def check_pool(problems, meta, kb):
    """A confirmed note must list every human capture of its subject: one it
    does not is a dictated claim that never reached the note."""
    if not kb or meta.get("type") != "Note" or meta.get("status") != "confirmed":
        return
    match = re.match(rf"^({SLUG})_\d+$", str(meta.get("id", "")))
    if not match:
        return
    listed = {
        r[len(ID_SCHEME):]
        for r in (meta.get("from") or [])
        if isinstance(r, str) and r.startswith(ID_SCHEME)
    }
    pool = re.compile(rf"^{re.escape(match.group(1))}_\d+$")
    missing = sorted(
        item_id
        for item_id, other in base(kb)[1].items()
        if pool.match(item_id)
        and other.get("type") == "Capture"
        and other.get("authored") == "human"
        and other.get("status") != "retired"
        and item_id not in listed
    )
    if missing:
        problems.append(
            ("warning", f"note is behind its pool; not in `from`: {' '.join(missing)}")
        )


def check_file(path):
    """Return a list of (severity, message)."""
    problems = []
    with open(path, encoding="utf-8") as handle:
        raw = handle.read()

    block = split_frontmatter(raw)
    if block is None:
        return [("error", "no `---` frontmatter block")]
    try:
        meta = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        return [("error", f"frontmatter is not valid YAML: {exc}")]
    if not isinstance(meta, dict):
        return [("error", "frontmatter is not a mapping")]

    for key in REQUIRED:
        if key not in meta:
            problems.append(("error", f"missing required key `{key}`"))

    item_id = str(meta.get("id", ""))
    stem = os.path.basename(path)[: -len(".md")]
    if item_id and stem != item_id and not stem.endswith(f"_{item_id}"):
        problems.append(
            ("error", f"filename {stem!r} does not end in `id` {item_id!r}")
        )
    elif item_id and not ID_RE.match(item_id):
        problems.append(("error", "`id` is not `<slug>_<n>` or 12 base62 characters"))

    if meta.get("authored") not in AUTHORS:
        problems.append(("error", f"`authored` must be one of {sorted(AUTHORS)}"))
    if meta.get("status") not in STATUSES:
        problems.append(("error", f"`status` must be one of {sorted(STATUSES)}"))
    if "date" in meta and not DATE_RE.match(str(meta["date"])):
        problems.append(("error", "`date` is not a YYYY-MM-DD date"))
    if "code" in meta and not CODE_RE.match(str(meta["code"])):
        problems.append(("error", "`code` is not `<repository url>@<commit>`"))
    if "paths" in meta:
        check_strings(problems, meta, "paths")
        if "code" not in meta:
            problems.append(("error", "`paths` without `code`: paths of what?"))

    kb = base_of(path)
    if "from" in meta:
        check_from(problems, meta, kb)
    check_pool(problems, meta, kb)
    if kb and item_id and len(base(kb)[0].get(item_id) or []) > 1:
        problems.append(("error", f"`id` {item_id!r} is shared with another item"))

    lines = block.count("\n") + 1
    if lines > FRONTMATTER_LINES:
        problems.append(
            ("warning", f"frontmatter is {lines} lines (budget {FRONTMATTER_LINES})")
        )

    check_blocks(problems, raw[len(block) + 8:])

    return problems


def collect(targets):
    for target in targets:
        if os.path.isdir(target):
            for root, _, names in os.walk(target):
                for name in sorted(names):
                    if name.endswith(".md"):
                        yield os.path.join(root, name)
        else:
            yield target


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    failed = checked = 0
    for path in collect(argv):
        checked += 1
        problems = check_file(path)
        for severity, message in problems:
            print(f"{path}: {severity}: {message}")
        if any(severity == "error" for severity, _ in problems):
            failed += 1
    print(f"kb_check: {checked} file(s), {failed} with errors")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
