#!/usr/bin/env python3
"""Export approved cards as an Anki-importable text file, one deck per kind.

Usage:  kb_export.py [--out PATH] [--dry-run]

Reads every card in the knowledge base, writes one importable file, and
regenerates each note's `cards:` list from the cards that cite it — the only
pass that writes back into a note, and it touches frontmatter, never prose.

- Only approved cards are exported: `status: stable` plus a `human:` entry in
  `verified`. A proposal awaiting the user is `status: draft` and stays out.
- `status: deprecated` cards are omitted and listed. **Omission does not
  suspend them** — a package can only add and update, so a card already in the
  scheduler stays active until it is suspended there by hand.
- A duplicate card ID is fatal and nothing is written: two cards sharing an ID
  share an identity in the scheduler, and one would overwrite the other.

Anki identity derives from the guid column, which carries the card ID, so
re-importing updates an existing note rather than duplicating it. That contract
breaks if the deck or notetype is renamed in Anki's own interface — rename here
and re-export instead.

Requires PyYAML. Unlike kb_check.py this is a gate, not an aid, so a missing
dependency is an error rather than a skip.
"""

import html
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("kb_export: PyYAML is required to read frontmatter")

# Stable by contract: the scheduler keys review history off these names, and a
# rename in Anki's interface does not round-trip. Change them here, re-export,
# and rename in Anki to match.
DECKS = {"Quick Card": "Knowledge::Quick", "Deep Card": "Knowledge::Deep"}
NOTETYPE = "Basic"

HEADER = [
    "#separator:tab",
    "#html:true",
    f"#notetype:{NOTETYPE}",
    "#deck column:3",
    "#guid column:4",
]

SKIP_DIRS = {".git", ".repository-mapping"}
FM_CARDS = re.compile(r"^cards:.*(?:\n[ \t].*|\n-.*)*\n?", re.MULTILINE)


def resolve_kb():
    """$KB_HOME, then the pointer file, then an enclosing base."""
    candidates = []
    if os.environ.get("KB_HOME"):
        candidates.append(os.path.expanduser(os.environ["KB_HOME"]))
    pointer = os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        "kb-tools",
        "kb-home",
    )
    if os.path.isfile(pointer):
        with open(pointer, encoding="utf-8") as handle:
            candidates.append(os.path.expanduser(handle.readline().strip()))
    path = os.getcwd()
    while path != os.path.dirname(path):
        candidates.append(path)
        path = os.path.dirname(path)
    for candidate in candidates:
        if candidate and os.path.isfile(os.path.join(candidate, "SCHEMA.md")):
            return candidate
    return None


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    body = text[end + 4 :]
    return text[4:end], body.split("\n", 1)[1] if "\n" in body else ""


def read_items(kb):
    for root, dirs, names in os.walk(kb):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as handle:
                block, body = split_frontmatter(handle.read())
            if block is None:
                continue
            try:
                meta = yaml.safe_load(block)
            except yaml.YAMLError:
                continue
            if isinstance(meta, dict):
                yield path, meta, body.strip()


def is_approved(meta):
    entries = meta.get("verified") or []
    return meta.get("status") == "stable" and any(
        isinstance(e, dict) and str(e.get("by", "")).startswith("human:")
        for e in entries
    )


def to_field(text):
    """Markdown fragment to a single-line HTML field."""
    out = html.escape(text.replace("\t", " ").strip())
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    return re.sub(r"\n{2,}", "<br><br>", out).replace("\n", "<br>")


def split_qa(body):
    """`**Q:** … **A:** …` if present, else the whole body as the front."""
    match = re.search(r"\*\*Q:\*\*(.*?)\*\*A:\*\*(.*)", body, re.DOTALL)
    if match:
        return to_field(match.group(1)), to_field(match.group(2))
    return to_field(body), ""


def note_of(meta):
    """A card's sources are notes only; the first one is its note."""
    sources = meta.get("sources") or []
    if sources and isinstance(sources[0], dict):
        return str(sources[0].get("resource", ""))
    return ""


def rewrite_cards(block, ids):
    """Replace, insert or drop the `cards:` key. Frontmatter text only."""
    line = "cards: [" + ", ".join(ids) + "]\n" if ids else ""
    body = block if block.endswith("\n") else block + "\n"
    if FM_CARDS.search(body):
        body = FM_CARDS.sub(line, body, count=1)
    else:
        body += line
    return body.rstrip("\n")


def update_note(path, ids, dry_run):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    end = text.find("\n---", 3)
    if not text.startswith("---\n") or end < 0:
        return False
    block, rest = text[4:end], text[end:]
    updated = rewrite_cards(block, ids)
    if updated == block:
        return False
    if not dry_run:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("---\n" + updated + rest)
    return True


def main(argv):
    dry_run = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]
    out = None
    if argv[:1] == ["--out"] and len(argv) > 1:
        out = argv[1]
    elif argv:
        return print(__doc__.strip()) or 2

    kb = resolve_kb()
    if not kb:
        return print("kb_export: no knowledge base found (/kb-init makes one)") or 1
    out = out or os.path.join(kb, "export", "kb-export.txt")

    cards, notes, seen = [], {}, {}
    for path, meta, body in read_items(kb):
        if meta.get("type") not in DECKS:
            continue
        card_id = str(meta.get("id", ""))
        if card_id in seen:
            print(f"kb_export: error: duplicate card id {card_id!r}")
            print(f"  {seen[card_id]}\n  {path}")
            return print("kb_export: nothing written") or 1
        seen[card_id] = path
        cards.append((path, meta, body))
        # The note's index lists its real cards; a draft is still a proposal.
        if meta.get("status") != "draft":
            notes.setdefault(note_of(meta), []).append(card_id)

    rows, deprecated, held_back = [], [], []
    for path, meta, body in cards:
        if meta.get("status") == "deprecated":
            deprecated.append(str(meta.get("id")))
            continue
        if not is_approved(meta):
            held_back.append(str(meta.get("id")))
            continue
        front, back = split_qa(body)
        rows.append(
            [front, back, DECKS[meta["type"]], str(meta.get("id", ""))]
        )

    if not dry_run:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(HEADER) + "\n")
            for row in rows:
                handle.write("\t".join(row) + "\n")

    touched = 0
    for resource, ids in notes.items():
        if not resource.startswith("/"):
            continue
        path = os.path.join(kb, resource.lstrip("/"))
        if os.path.isfile(path) and update_note(path, sorted(ids), dry_run):
            touched += 1

    per_deck = {deck: sum(1 for r in rows if r[2] == deck) for deck in DECKS.values()}
    prefix = "would write" if dry_run else "wrote"
    print(f"kb_export: {prefix} {len(rows)} card(s) to {out}")
    for deck, count in sorted(per_deck.items()):
        print(f"  {deck}: {count}")
    print(f"kb_export: {prefix} `cards:` on {touched} note(s)")
    if held_back:
        print(f"kb_export: {len(held_back)} unapproved, held back: {' '.join(held_back)}")
    if deprecated:
        print(f"kb_export: {len(deprecated)} deprecated, omitted: {' '.join(deprecated)}")
        print("  omission does not suspend them — suspend in the scheduler by hand")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
