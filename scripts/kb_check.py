#!/usr/bin/env python3
"""Check knowledge-base frontmatter against ../reference/frontmatter.md.

Usage:  kb_check.py <file-or-directory>...

Reports one line per problem and exits 1 if any is an error. Warnings do not
affect the exit code. Requires PyYAML; without it the check is skipped rather
than failed, since it is an aid and never a gate.

Deliberately mechanical. It checks the shape of the frontmatter — keys that
must be present, values that must parse — and nothing that depends on what kind
of item this is or where it lives. Types are open (OKF permits any) and the
layout is free to change, so a checker that enumerated either would be wrong
before it was useful. Everything about meaning is the reader's job.
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

STATUSES = {"draft", "stable", "deprecated"}
# Two accepted shapes, kind-agnostically: a date and a slug, or a slug and a
# random tail — the latter is how a card ID is built (see the schema).
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
ID_RE = re.compile(rf"^(?:\d{{4}}-\d{{2}}-\d{{2}}-{SLUG}|{SLUG}-[A-Za-z0-9]{{10}})$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    return None if end < 0 else text[4:end]


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


def check_sources(problems, sources):
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
    if item_id and item_id != stem:
        problems.append(("error", f"`id` {item_id!r} does not match filename {stem!r}"))
    elif item_id and not ID_RE.match(item_id):
        problems.append(
            ("error", "`id` is neither `<date>-<slug>` nor `<slug>-<10 random>`")
        )

    if meta.get("origin") not in {"human", "machine"}:
        problems.append(("error", "`origin` must be `human` or `machine`"))
    if meta.get("status") not in STATUSES:
        problems.append(("error", f"`status` must be one of {sorted(STATUSES)}"))
    if "generated" in meta:
        check_actor_stamp(problems, "generated", meta["generated"])

    verified = meta.get("verified")
    if verified is not None:
        if not isinstance(verified, list):
            problems.append(("error", "`verified` must be a list of { by, at }"))
            verified = None
        else:
            for i, entry in enumerate(verified):
                check_actor_stamp(problems, f"verified[{i}]", entry)

    # The one rule with teeth: nothing unverified may claim to be settled.
    # A draft is how anything not yet checked or not yet approved is spelled.
    if not verified and meta.get("status") != "draft":
        problems.append(("error", "unverified item must carry `status: draft`"))

    if "sources" in meta:
        check_sources(problems, meta["sources"])

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
