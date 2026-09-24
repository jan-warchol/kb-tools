#!/usr/bin/env python3
"""Find items in the knowledge base by identity, never by path.

Usage:
  kb_find.py <id>...           the file each ID names
  kb_find.py --pool <slug>     every item sharing the slug, oldest number first
  kb_find.py --refs <id>       every item whose `from` names that item

Pool and refs print one item per line:
  <path>  <id>  <type>  <authored>  <status>  <date>

A slug pool is one subject's history — its captures, note and verify reports —
and `--refs` is how a note's cards are found. Both read
frontmatter, so they work however the base is arranged. Exits 1 when an ID
names no item, or more than one.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_export import (  # noqa: E402
    INIT,
    items_by_id,
    read_items,
    resolve_kb,
    resolve_resource,
)


def row(kb, path, meta):
    fields = [
        os.path.relpath(path, kb),
        meta.get("id", ""),
        meta.get("type", ""),
        meta.get("authored", ""),
        meta.get("status", ""),
        meta.get("date", ""),
    ]
    return "  ".join(str(f) for f in fields)


def number(meta):
    match = re.search(r"_(\d+)$", str(meta.get("id", "")))
    return int(match.group(1)) if match else 0


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    kb = resolve_kb()
    if not kb:
        print(f"kb_find: no knowledge base found ({INIT} makes one)")
        return 1
    items = list(read_items(kb))
    by_id = items_by_id(items)

    if argv[0] == "--pool" and len(argv) == 2:
        pool = re.compile(rf"^{re.escape(argv[1])}_\d+$")
        found = sorted(
            ((p, m) for p, m, _ in items if pool.match(str(m.get("id", "")))),
            key=lambda pm: number(pm[1]),
        )
        for path, meta in found:
            print(row(kb, path, meta))
        return 0

    if argv[0] == "--refs" and len(argv) == 2:
        paths = by_id.get(argv[1]) or []
        if len(paths) != 1:
            print(f"kb_find: {argv[1]!r} names {len(paths)} items")
            return 1
        for path, meta, _ in items:
            origins = meta.get("from")
            if not isinstance(origins, list):
                continue
            if any(resolve_resource(kb, o, by_id) == paths[0] for o in origins):
                print(row(kb, path, meta))
        return 0

    status = 0
    for item_id in argv:
        paths = by_id.get(item_id) or []
        if len(paths) == 1:
            print(os.path.relpath(paths[0], kb))
        else:
            print(f"kb_find: {item_id!r} names {len(paths)} items", file=sys.stderr)
            for path in paths:
                print(f"  {os.path.relpath(path, kb)}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
