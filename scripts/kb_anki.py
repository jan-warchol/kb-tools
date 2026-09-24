#!/usr/bin/env python3
"""Talk to Anki through AnkiConnect: status, backup, sync.

Usage:
  kb_anki.py status                  what Anki has due, and how old the backup is
  kb_anki.py backup [--out DIR]      write a scheduling-preserving .apkg
  kb_anki.py sync                    sync with AnkiWeb

Nothing here writes to the knowledge base, nor grades or moves a card: review
is Anki's own. It writes, on request, a backup file. Anki being unreachable
exits 3, so a caller can tell that from a real failure.
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_export import INIT, deck_root, resolve_kb  # noqa: E402

ENDPOINT = os.environ.get("ANKI_CONNECT_URL", "http://127.0.0.1:8765")
TIMEOUT = 15
UNAVAILABLE = 3

BACKUP_DIR = "backups"


def call(action, **params):
    """One AnkiConnect request. Exits 3 when Anki cannot be reached at all."""
    payload = json.dumps(
        {"action": action, "version": 6, "params": params}
    ).encode("utf-8")
    request = urllib.request.Request(ENDPOINT, data=payload)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = json.load(response)
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        print(f"kb_anki: cannot reach Anki at {ENDPOINT} ({exc})")
        print("  start Anki, and check the AnkiConnect add-on is installed")
        sys.exit(UNAVAILABLE)
    if body.get("error"):
        raise AnkiError(body["error"])
    return body.get("result")


class AnkiError(Exception):
    pass


def base():
    kb = resolve_kb()
    if not kb:
        sys.exit(f"kb_anki: no knowledge base found ({INIT} makes one)")
    return kb


def newest_backup(kb):
    directory = os.path.join(kb, BACKUP_DIR)
    if not os.path.isdir(directory):
        return None
    files = [
        os.path.join(directory, n)
        for n in os.listdir(directory)
        if n.endswith(".apkg")
    ]
    return max(files, key=os.path.getmtime) if files else None


def cmd_status(argv):
    kb = base()
    root = deck_root(kb)
    call("version")
    decks = [d for d in call("deckNames") if d == root or d.startswith(root + "::")]
    stats = call("getDeckStats", decks=decks) if decks else {}
    print(f"anki: reachable at {ENDPOINT}")
    print(f"root: {root}")
    if not decks:
        print(f"  no deck named {root} yet — nothing has been imported")
    for entry in sorted(stats.values(), key=lambda e: e["name"]):
        print(
            f"  {entry['name']}: {entry['new_count']} new,"
            f" {entry['learn_count']} learning, {entry['review_count']} due"
            f" ({entry['total_in_deck']} total)"
        )
    latest = newest_backup(kb)
    if latest is None:
        print(f"backup: none in {os.path.join(kb, BACKUP_DIR)} — none has been made")
    else:
        age = (
            datetime.datetime.now()
            - datetime.datetime.fromtimestamp(os.path.getmtime(latest))
        ).days
        print(f"backup: {os.path.basename(latest)}, {age} day(s) old")
    return 0


def cmd_backup(argv):
    kb = base()
    directory = os.path.join(kb, BACKUP_DIR)
    if argv[:1] == ["--out"] and len(argv) > 1:
        directory = os.path.abspath(os.path.expanduser(argv[1]))
    elif argv:
        return usage()
    root = deck_root(kb)
    os.makedirs(directory, exist_ok=True)
    stamp = datetime.date.today().isoformat()
    # includeSched is the point: cards regenerate from the markdown, review
    # history does not.
    out = os.path.join(directory, f"anki-{stamp}.apkg")
    if not call("exportPackage", deck=root, path=out, includeSched=True):
        print(f"kb_anki: Anki refused to export {root}")
        return 1
    size = os.path.getsize(out) // 1024 if os.path.isfile(out) else 0
    print(f"backup: {out} ({size} KiB, scheduling included)")
    return 0


def cmd_sync(argv):
    call("sync")
    print("sync: requested")
    return 0


COMMANDS = {
    "status": cmd_status,
    "backup": cmd_backup,
    "sync": cmd_sync,
}


def usage():
    print(__doc__.strip())
    return 2


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        return usage()
    try:
        return COMMANDS[argv[0]](argv[1:])
    except AnkiError as exc:
        print(f"kb_anki: Anki refused the request: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
