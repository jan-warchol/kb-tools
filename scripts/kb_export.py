#!/usr/bin/env python3
"""Export approved cards as an Anki-importable text file, one deck per kind.

Usage:  kb_export.py [--out PATH] [--dry-run]

Reads every card in the knowledge base and writes one importable file. It
reads only: nothing here writes back into a note or a card.

- Only approved cards are exported: `status: stable` plus a `human:` entry in
  `verified`. A proposal awaiting the user is `status: draft` and stays out.
- `status: deprecated` cards are omitted and listed. **Omission does not
  suspend them** — a package can only add and update, so a card already in the
  scheduler stays active until it is suspended there by hand.
- A duplicate card ID is fatal and nothing is written: two cards sharing an ID
  share an identity in the scheduler, and one would overwrite the other.

Anki identity derives from the guid column, which carries the card ID, so
re-importing updates an existing card rather than duplicating it (decisions.md
for why identity sits there). That contract breaks if the deck or notetype is
renamed in Anki's own interface — rename here and re-export instead.

Fields are markdown, not HTML. Anki turns a newline inside a quoted field into a
line break, so soft wrapping is joined up on the way out.

Cards land in a subdeck per kind under `anki_deck_name:` from the optional
`<kb>/knowledge-base.yaml` (or `.yml`), falling back to Knowledge — so a Recall
Card goes to Knowledge::Recall, and a kind added later needs no change here.

Requires PyYAML. Unlike kb_check.py this is a gate, not an aid, so a missing
dependency is an error rather than a skip.
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("kb_export: PyYAML is required to read frontmatter")

# A card kind is a type ending in "Card", and lands in a subdeck named after
# what precedes that — so a kind added later needs nothing here. Deck names are
# stable by contract: the scheduler keys review history off them, and a rename
# in Anki's interface does not round-trip. Change the root in the base's config,
# re-export, and rename in Anki to match.
CONFIG = ("knowledge-base.yaml", "knowledge-base.yml")
DECK_KEY = "anki_deck_name"
DEFAULT_DECK = "Knowledge"
SUFFIX = " Card"
NOTETYPE = "Basic"

HEADER = [
    "#separator:tab",
    "#html:false",
    f"#notetype:{NOTETYPE}",
    "#deck column:3",
    "#guid column:4",
]

SKIP_DIRS = {".git"}
QA_RE = re.compile(
    r"^#+[ \t]*Question[ \t]*$(.*?)^#+[ \t]*Answer[ \t]*$(.*)",
    re.DOTALL | re.MULTILINE | re.IGNORECASE,
)


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


def config_path(kb):
    """The base's config file under either spelling, or None.

    Both at once is refused rather than resolved: the deck name is part of the
    identity contract, and guessing which file meant it could move a deck.
    """
    found = [n for n in CONFIG if os.path.isfile(os.path.join(kb, n))]
    if len(found) > 1:
        sys.exit(f"kb_export: {' and '.join(found)} both exist — keep one")
    return os.path.join(kb, found[0]) if found else None


def deck_root(kb):
    """The deck everything hangs under, from the base's config or the default."""
    path = config_path(kb)
    if path is None:
        return DEFAULT_DECK
    with open(path, encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        sys.exit(f"kb_export: {os.path.basename(path)} is not a mapping")
    return str(config.get(DECK_KEY) or DEFAULT_DECK)


def deck_of(item_type, root):
    """`Recall Card` under `Knowledge` is `Knowledge::Recall`; None if not a card."""
    if not isinstance(item_type, str) or not item_type.endswith(SUFFIX):
        return None
    return f"{root}::{item_type[: -len(SUFFIX)]}"


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


def unwrap(text):
    """Join soft wrapping; blank lines, list items and fences are structure."""
    out, fenced = [], False
    for line in text.strip().split("\n"):
        line = line.replace("\t", " ").rstrip()
        alone = fenced or not out or not out[-1] or not line
        if line.lstrip().startswith("```"):
            fenced, alone = not fenced, True
        elif re.match(r"[ ]{0,3}(?:[-*+]|\d+[.)])[ \t]", line) or line.startswith("    "):
            alone = True
        if alone:
            out.append(line)
        else:
            out[-1] += " " + line.lstrip()
    return "\n".join(out).strip()


def to_field(text):
    """A markdown fragment as one import field, quoted when it has to be."""
    field = unwrap(text)
    if '"' in field or "\n" in field:
        return '"' + field.replace('"', '""') + '"'
    return field


def split_qa(body):
    """`## Question` / `## Answer` if present, else the body as the front."""
    match = QA_RE.search(body)
    if match:
        return to_field(match.group(1)), to_field(match.group(2))
    return to_field(body), ""


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
    root = deck_root(kb)

    cards, seen = [], {}
    for path, meta, body in read_items(kb):
        deck = deck_of(meta.get("type"), root)
        if deck is None:
            continue
        card_id = str(meta.get("id", ""))
        if card_id in seen:
            print(f"kb_export: error: duplicate card id {card_id!r}")
            print(f"  {seen[card_id]}\n  {path}")
            return print("kb_export: nothing written") or 1
        seen[card_id] = path
        cards.append((path, meta, body, deck))

    rows, deprecated, held_back = [], [], []
    for path, meta, body, deck in cards:
        if meta.get("status") == "deprecated":
            deprecated.append(str(meta.get("id")))
            continue
        if not is_approved(meta):
            held_back.append(str(meta.get("id")))
            continue
        front, back = split_qa(body)
        rows.append(
            [front, back, deck, str(meta.get("id", ""))]
        )

    if not dry_run:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as handle:
            handle.write("\n".join(HEADER) + "\n")
            for row in rows:
                handle.write("\t".join(row) + "\n")

    per_deck = {}
    for row in rows:
        per_deck[row[2]] = per_deck.get(row[2], 0) + 1
    prefix = "would write" if dry_run else "wrote"
    print(f"kb_export: {prefix} {len(rows)} card(s) to {out}")
    for deck, count in sorted(per_deck.items()):
        print(f"  {deck}: {count}")
    if held_back:
        print(f"kb_export: {len(held_back)} unapproved, held back: {' '.join(held_back)}")
    if deprecated:
        print(f"kb_export: {len(deprecated)} deprecated, omitted: {' '.join(deprecated)}")
        print("  omission does not suspend them — suspend in the scheduler by hand")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
