#!/usr/bin/env python3
"""Drive Anki through AnkiConnect: review understanding cards, grade, back up.

Usage:
  kb_anki.py status                  what Anki has due, and how old the backup is
  kb_anki.py session [deck]          open the reviewer on the understanding deck
  kb_anki.py next                    the card the reviewer is showing, resolved
  kb_anki.py grade <ease> <card-id>  grade the card the reviewer is showing
  kb_anki.py grade-card <kb-id> <ease>   grade one card by its kb ID
  kb_anki.py backup [--out DIR]      write a scheduling-preserving .apkg
  kb_anki.py sync                    sync with AnkiWeb

`ease` is again | hard | good | easy.

**Reviewing goes through Anki's own reviewer, not a search.** `session` is the
Study Now button, so limits, orders and steps stay the scheduler's and none of
them are reimplemented here; an exhausted queue announces itself. A search
would have ignored every one of them.

A card is traced back to its file through the `kb::<card id>` tag the export
writes — the ID is also the guid, but no Anki interface reads a guid back out.
The card file's first source names the note.

Nothing here writes to the knowledge base. It writes a grade to Anki (only the
one asked for, and only while the reviewer still shows that card) and, on
request, a backup file. Anki being unreachable exits 3, so a caller can tell
that from a real failure.
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_export import TAG_PREFIX, deck_root, read_items, resolve_kb  # noqa: E402

ENDPOINT = os.environ.get("ANKI_CONNECT_URL", "http://127.0.0.1:8765")
TIMEOUT = 15
UNAVAILABLE = 3

# `hard` is deliberately available here: the rule against it belongs to
# self-graded recall. See reference/anki-setup.md.
EASE = {"again": 1, "hard": 2, "good": 3, "easy": 4}

UNDERSTANDING_DECK = "Understanding"
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
        sys.exit("kb_anki: no knowledge base found (/kb-init makes one)")
    return kb


def cards_by_id(kb):
    """Every card in the base by its ID, as (path, meta)."""
    out = {}
    for path, meta, _ in read_items(kb):
        item_type = meta.get("type")
        if isinstance(item_type, str) and item_type.endswith(" Card"):
            out[str(meta.get("id", ""))] = (path, meta)
    return out


def note_path(kb, meta):
    """The file the card's first source names, or None."""
    sources = meta.get("sources") or []
    if not sources or not isinstance(sources[0], dict):
        return None
    resource = str(sources[0].get("resource", ""))
    if not resource.startswith("/"):
        return None
    candidate = os.path.join(kb, resource.lstrip("/"))
    return candidate if os.path.isfile(candidate) else None


def kb_tag(tags):
    for tag in tags or []:
        if str(tag).startswith(TAG_PREFIX):
            return str(tag)[len(TAG_PREFIX) :]
    return None


def resolve_card(kb, card_id):
    """An Anki card ID to everything the quiz needs, or a reason it cannot be."""
    info = call("cardsInfo", cards=[card_id])
    if not info:
        return None, f"Anki knows no card {card_id}"
    info = info[0]
    notes = call("notesInfo", notes=[info["note"]])
    tag = kb_tag(notes[0].get("tags") if notes else None)
    if tag is None:
        return None, (
            f"card {card_id} in {info['deckName']} carries no {TAG_PREFIX} tag "
            "— it was not exported from this knowledge base"
        )
    entry = cards_by_id(kb).get(tag)
    if entry is None:
        return None, (
            f"card {tag} is in Anki but no longer in the knowledge base "
            "— it may have been deleted; suspend it in Anki"
        )
    path, meta = entry
    return {
        "card": card_id,
        "kb_card": tag,
        "deck": info["deckName"],
        "title": str(meta.get("title", "")),
        "card_file": path,
        "note": note_path(kb, meta),
        "next": [strip_marks(x) for x in info.get("nextReviews") or []],
    }, None


def strip_marks(text):
    """Anki wraps interval labels in bidi isolates; they are noise here."""
    return "".join(c for c in str(text) if c not in "⁦⁧⁨⁩")


def report(fields):
    for key, value in fields.items():
        if isinstance(value, list):
            value = " ".join(value)
        print(f"{key}: {value if value is not None else '-'}")


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
    print(f"reviewer: {'active' if call('guiReviewActive') else 'not active'}")
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


def cmd_session(argv):
    kb = base()
    deck = argv[0] if argv else f"{deck_root(kb)}::{UNDERSTANDING_DECK}"
    if deck not in call("deckNames"):
        print(f"kb_anki: no deck named {deck} — nothing to review")
        return 1
    call("guiDeckReview", name=deck)
    print(f"reviewing: {deck}")
    return cmd_next([])


def cmd_next(argv):
    kb = base()
    if not call("guiReviewActive"):
        print("card: none   # the queue is finished, or no session is open")
        return 0
    try:
        current = call("guiCurrentCard")
    except AnkiError:
        print("card: none   # the queue is finished, or no session is open")
        return 0
    if not current:
        print("card: none   # the queue is finished")
        return 0
    resolved, problem = resolve_card(kb, current["cardId"])
    if problem:
        print(f"card: {current['cardId']}")
        print(f"problem: {problem}")
        return 1
    report(resolved)
    return 0


def cmd_grade(argv):
    if len(argv) != 2 or argv[0] not in EASE:
        return usage()
    ease, card_id = EASE[argv[0]], int(argv[1])
    current = call("guiCurrentCard") if call("guiReviewActive") else None
    # If the reviewer has moved on, the grade would land on whatever is
    # showing now. Refuse rather than guess.
    if not current or current["cardId"] != card_id:
        showing = current["cardId"] if current else "nothing"
        print(f"kb_anki: the reviewer is showing {showing}, not {card_id}")
        print("  nothing graded — re-run `next` and quiz on what it reports")
        return 1
    call("guiShowAnswer")
    call("guiAnswerCard", ease=ease)
    print(f"graded: {card_id} {argv[0]}")
    return 0


def cmd_grade_card(argv):
    if len(argv) != 2 or argv[1] not in EASE:
        return usage()
    kb_id, ease = argv[0], EASE[argv[1]]
    found = call("findCards", query=f"tag:{TAG_PREFIX}{kb_id}")
    if not found:
        print(f"kb_anki: no card tagged {TAG_PREFIX}{kb_id} in Anki")
        print("  it may not have been imported yet")
        return 1
    if len(found) > 1:
        print(f"kb_anki: {len(found)} cards tagged {TAG_PREFIX}{kb_id} — nothing graded")
        return 1
    results = call("answerCards", answers=[{"cardId": found[0], "ease": ease}])
    if not (results and results[0]):
        print(f"kb_anki: Anki refused the grade for {kb_id}")
        return 1
    print(f"graded: {kb_id} {argv[1]}")
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
    "session": cmd_session,
    "next": cmd_next,
    "grade": cmd_grade,
    "grade-card": cmd_grade_card,
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
