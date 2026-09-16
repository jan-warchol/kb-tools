#!/usr/bin/env python3
"""Check knowledge-base frontmatter against ../reference/schema/.

Usage:  kb_check.py <file-or-directory>...

Reports one line per problem and exits 1 if any is an error. Warnings do not
affect the exit code. Requires PyYAML; without it the check is skipped rather
than failed, since it is an aid and never a gate.

Deliberately mechanical. It checks the shape of the frontmatter — keys that
must be present, values that must parse — plus that machine blocks in the body
open and close in turn, and nothing that depends on what kind of item this is
or where it lives. Types are open (OKF permits any) and the
layout is free to change, so a checker that enumerated either would be wrong
before it was useful. Everything about meaning is the reader's job.

The one thing it looks beyond a file for is identity: a `kb:<id>` in `sources`
must name exactly one item in the enclosing base, and no other item may share
the file's own `id`. Warnings flag legacy forms `kb_migrate.py` converts, a
frontmatter block past its budget, and approval older than the claims it
covers.
"""

import datetime
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("kb_check: PyYAML not installed — frontmatter check skipped")
    sys.exit(0)

STATUSES = {"draft", "stable", "deprecated", "abandoned"}
# Two shapes (see the schema): an item that stays in the base is
# `<slug>_<n>`, no date — a card, which leaves the base, is twelve random
# base62 characters instead. A slug ending in a number is indistinguishable
# from a suffix here, which is why the check is a shape and not a guarantee
# of uniqueness.
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
ID_RE = re.compile(rf"^(?:{SLUG}_\d+|[A-Za-z0-9]{{12}})$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A soft budget: past it, frontmatter is usually carrying copied evidence or
# history that belongs elsewhere.
FRONTMATTER_LINES = 20

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_export import ID_SCHEME, items_by_id, read_items  # noqa: E402

_indexes = {}


def base_of(path):
    """The knowledge base enclosing a file — the nearest SCHEMA.md above it."""
    directory = os.path.dirname(os.path.abspath(path))
    while directory != os.path.dirname(directory):
        if os.path.isfile(os.path.join(directory, "SCHEMA.md")):
            return directory
        directory = os.path.dirname(directory)
    return None


def index_of(kb):
    if kb not in _indexes:
        _indexes[kb] = items_by_id(read_items(kb))
    return _indexes[kb]


def as_time(value):
    if isinstance(value, datetime.datetime):
        return value if value.tzinfo else value.replace(tzinfo=datetime.timezone.utc)
    if isinstance(value, str) and TS_RE.match(value):
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    return None if end < 0 else text[4:end]


def check_blocks(problems, body):
    """Machine blocks must open and close in turn; an unclosed one would
    swallow the user's claims, a stray close would leak the agent's."""
    depth = 0
    for match in re.finditer(r"^<!-- (machine:.*|/machine) -->\s*$", body, re.M):
        if match.group(1).startswith("machine:"):
            if depth:
                problems.append(("error", "machine block opened inside another"))
            depth = 1
        else:
            if not depth:
                problems.append(("error", "machine block closed but never opened"))
            depth = 0
    if depth:
        problems.append(("error", "machine block never closed"))


def is_timestamp(value):
    if isinstance(value, datetime.datetime):
        return True
    return isinstance(value, str) and bool(TS_RE.match(value))


def check_actor_stamp(problems, label, value):
    if not isinstance(value, dict):
        problems.append(("error", f"{label} must be a mapping with `by` and `at`"))
        return
    for key in ("by", "at"):
        if key not in value:
            problems.append(("error", f"{label} is missing `{key}`"))
    if "at" in value and not is_timestamp(value["at"]):
        problems.append(("error", f"{label}.at is not an ISO 8601 timestamp"))


def check_sources(problems, sources, kb):
    if not isinstance(sources, list):
        problems.append(("error", "`sources` must be a list"))
        return
    for i, entry in enumerate(sources):
        label = f"sources[{i}]"
        if not isinstance(entry, dict):
            problems.append(("error", f"{label} must be a mapping"))
            continue
        if not entry.get("resource"):
            problems.append(("error", f"{label} is missing `resource`"))
            continue
        for singular, plural in (("path", "paths"), ("symbol", "symbols")):
            if singular in entry and plural in entry:
                problems.append(
                    ("error", f"{label} carries both `{singular}` and `{plural}`")
                )
        if "retrieved" in entry and not DATE_RE.match(str(entry["retrieved"])):
            problems.append(("error", f"{label}.retrieved is not a YYYY-MM-DD date"))
        resource = str(entry["resource"])
        if resource.startswith(ID_SCHEME) and kb:
            found = len(index_of(kb).get(resource[len(ID_SCHEME):]) or [])
            if found != 1:
                problems.append(("error", f"{label} `{resource}` names {found} items"))
        elif resource.startswith("/"):
            problems.append(
                ("warning", f"{label} names an item by path; use `{ID_SCHEME}<id>`")
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

    for key in ("id", "type", "title", "origin", "generated", "status"):
        if key not in meta:
            problems.append(("error", f"missing required key `{key}`"))

    item_id = str(meta.get("id", ""))
    stem = os.path.basename(path)[: -len(".md")]
    if item_id and stem != item_id and not stem.endswith(f"_{item_id}"):
        problems.append(
            ("error", f"filename {stem!r} does not end in `id` {item_id!r}")
        )
    elif item_id and not ID_RE.match(item_id):
        problems.append(
            ("error", "`id` is not `<slug>_<n>` or 12 base62 characters")
        )

    if meta.get("origin") not in {"human", "machine"}:
        problems.append(("error", "`origin` must be `human` or `machine`"))
    if meta.get("status") not in STATUSES:
        problems.append(("error", f"`status` must be one of {sorted(STATUSES)}"))
    if "generated" in meta:
        check_actor_stamp(problems, "generated", meta["generated"])

    verified = meta.get("verified")
    if isinstance(verified, list):
        problems.append(("warning", "`verified` is a legacy list; keep the latest check only"))
        for i, entry in enumerate(verified):
            check_actor_stamp(problems, f"verified[{i}]", entry)
    elif verified is not None:
        check_actor_stamp(problems, "verified", verified)

    approved = meta.get("approved")
    if approved is not None:
        check_actor_stamp(problems, "approved", approved)
        by = str(approved.get("by", "")) if isinstance(approved, dict) else ""
        if isinstance(approved, dict) and not by.startswith("human:"):
            problems.append(("error", "`approved.by` must be a `human:` actor"))

    # The one rule with teeth: nothing unverified may claim to be settled.
    # A draft is how anything not yet checked is spelled. A card carries no
    # `verified` of its own — its claim was checked where it came from — so
    # approval stands in for it there.
    if not verified and not approved and meta.get("status") != "draft":
        problems.append(("error", "unverified item must carry `status: draft`"))

    kb = base_of(path)
    if "sources" in meta:
        check_sources(problems, meta["sources"], kb)
    if kb and item_id and len(index_of(kb).get(item_id) or []) > 1:
        problems.append(("error", f"`id` {item_id!r} is shared with another item"))

    # Approval covers claims; `generated.at` moves only when claims change, so
    # a later one means the user approved text that has since changed.
    generated = meta.get("generated")
    if isinstance(approved, dict) and isinstance(generated, dict):
        changed, stamped = as_time(generated.get("at")), as_time(approved.get("at"))
        if changed and stamped and changed > stamped:
            problems.append(("warning", "claims changed after `approved.at`; re-approve"))

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
