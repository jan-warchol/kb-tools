#!/usr/bin/env python3
"""Export approved cards as an Anki-importable text file, one deck per kind.

Usage:  kb_export.py [--out PATH] [--dry-run]

Reads every card in the knowledge base and writes one importable file. It
reads only: nothing here writes back into a note or a card.

- Only approved cards are exported: `status: stable` plus an `approved` stamp
  by a `human:` actor (a `human:` entry in a legacy `verified` list is read
  the same way, for cards written before the two were split). A proposal awaiting the user is
  `status: draft` and stays out.
- `status: deprecated` cards are omitted and listed. **Omission does not
  suspend them** — a package can only add and update, so a card already in the
  scheduler stays active until it is suspended there by hand.
- A card with no `importance:` is held back too — undecided is a state, not a
  default, and the grade can only take effect before the card's first import.
- A duplicate card ID is fatal and nothing is written: two cards sharing an ID
  share an identity in the scheduler, and one would overwrite the other.

Anki identity derives from the guid column, which carries the card ID, so
re-importing updates an existing card rather than duplicating it (decisions.md
for why identity sits there). That contract breaks if the deck or notetype is
renamed in Anki's own interface — rename here and re-export instead.

Card bodies are markdown; fields are rendered to HTML on the way out, because
Anki renders neither markdown nor a bare newline as structure. The subset
rendered is what cards actually use: paragraphs, bullet lists, fenced and
inline code, bold and italic. Everything else is escaped and passed through.

Every card also carries the tag `kb::<card id>` — the ID is the guid too, but
no Anki interface reads a guid back out, so the tag is the only thing on that
side leading back to the file.

An Understanding Card is the one exception to reading the body: it has no
question of its own, so both fields are generated here from the frontmatter,
and a card naming no note in this base is held back. Its body, where it has
one, is never exported.

Cards land in a subdeck per kind, then per importance, under `anki_deck_name:`
from the optional `<kb>/knowledge-base.yaml` (or `.yml`), falling back to
Knowledge — so a Recall Card graded `core` goes to Knowledge::Recall::Core, and
a kind added later needs no change here. An unknown grade is fatal — a typo
would silently create a deck and split the collection in two.

Importance is the *initial* placement and nothing more. Anki does not move an
existing card on re-import, so a grade has effect only on a card the scheduler
has not yet seen — which is why an ungraded card waits here instead of being
defaulted somewhere: a grade written after the first import would silently do
nothing at all. Once placed, a card's deck and its `importance:` are free to
disagree and neither is wrong; demoting during review is the intended workflow.

Requires PyYAML. Unlike kb_check.py this is a gate, not an aid, so a missing
dependency is an error rather than a skip.
"""

import os
import re
import sys

INIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kb_init.sh")

try:
    import yaml
except ImportError:
    sys.exit("kb_export: PyYAML is required to read frontmatter")

# A card kind is a type ending in "Card", and lands in a subdeck named after
# what precedes that, split again by importance — so a kind added later needs
# nothing here, and a kind that never grades a card `extra` never creates the
# deck, since a text import makes decks lazily. Deck names are
# stable by contract: the scheduler keys review history off them, and a rename
# in Anki's interface does not round-trip. Change the root in the base's config,
# re-export, and rename in Anki to match.
CONFIG = ("knowledge-base.yaml", "knowledge-base.yml")
DECK_KEY = "anki_deck_name"
DEFAULT_DECK = "Knowledge"
SUFFIX = " Card"
NOTETYPE = "Basic"
IMPORTANCE_KEY = "importance"
IMPORTANCE = ("core", "extra")

# Written for every kind, not only the one that needs it, so nothing here
# dispatches on kind to produce it.
TAG_PREFIX = "kb::"

# How `sources` names another item: by ID, which survives the file moving.
ID_SCHEME = "kb:"

UNDERSTANDING = "Understanding"

HEADER = [
    "#separator:tab",
    "#html:true",
    f"#notetype:{NOTETYPE}",
    "#deck column:3",
    "#guid column:4",
    "#tags column:5",
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


def kind_of(item_type):
    """`Recall Card` is the `Recall` kind; None if the item is not a card."""
    if not isinstance(item_type, str) or not item_type.endswith(SUFFIX):
        return None
    return item_type[: -len(SUFFIX)]


def deck_of(kind, importance, root):
    """`Recall` and `core` under `Knowledge` is `Knowledge::Recall::Core`."""
    return f"{root}::{kind}::{importance.capitalize()}"


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


def is_human(entry):
    return isinstance(entry, dict) and str(entry.get("by", "")).startswith("human:")


def is_approved(meta):
    if meta.get("status") != "stable":
        return False
    verified = meta.get("verified")
    legacy = verified if isinstance(verified, list) else []
    return is_human(meta.get("approved")) or any(is_human(e) for e in legacy)


def items_by_id(items):
    """Every item's path by ID, as a list: more than one is a duplicate."""
    out = {}
    for path, meta, _ in items:
        out.setdefault(str(meta.get("id", "")), []).append(path)
    return out


def resolve_resource(kb, resource, by_id):
    """The file a `sources` resource names in this base, or None.

    `kb:<id>` is the form written now; a base-relative `/path` is the legacy
    form, still read until `kb_migrate.py` has run.
    """
    resource = str(resource or "")
    if resource.startswith(ID_SCHEME):
        paths = by_id.get(resource[len(ID_SCHEME):]) or []
        return paths[0] if len(paths) == 1 else None
    if resource.startswith("/"):
        candidate = os.path.join(kb, resource.lstrip("/"))
        return candidate if os.path.isfile(candidate) else None
    return None


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


BULLET_RE = re.compile(r"[ ]{0,3}(?:[-*+])[ \t]+(.*)")
ORDERED_RE = re.compile(r"[ ]{0,3}\d+[.)][ \t]+(.*)")
CODE_RE = re.compile(r"`([^`]+)`")
STRONG_RE = re.compile(r"\*\*(\S(?:.*?\S)?)\*\*")
EM_RE = re.compile(r"(?<![*\w])[*_](\S(?:.*?\S)?)[*_](?![*\w])")
SENTINEL = "\x00"


def escape(text):
    """HTML-escape, leaving the code-span sentinel alone."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text):
    """Inline markdown to HTML. Code spans are lifted out before escaping so
    their contents are never read as emphasis."""
    spans = []

    def stash(match):
        spans.append(escape(match.group(1)))
        return f"{SENTINEL}{len(spans) - 1}{SENTINEL}"

    text = CODE_RE.sub(stash, text)
    text = escape(text)
    text = STRONG_RE.sub(r"<strong>\1</strong>", text)
    text = EM_RE.sub(r"<em>\1</em>", text)
    for index, span in enumerate(spans):
        text = text.replace(f"{SENTINEL}{index}{SENTINEL}", f"<code>{span}</code>")
    return text


def blocks(lines):
    """Group unwrapped lines into (kind, lines) blocks."""
    out, fenced = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            if fenced:
                fenced = False
            else:
                fenced = True
                out.append(("code", []))
            continue
        if fenced:
            out[-1][1].append(line)
            continue
        if not line.strip():
            continue
        for kind, pattern in (("ul", BULLET_RE), ("ol", ORDERED_RE)):
            match = pattern.match(line)
            if match:
                if not out or out[-1][0] != kind:
                    out.append((kind, []))
                out[-1][1].append(match.group(1))
                break
        else:
            out.append(("p", [line]))
    return out


def render(text):
    """The markdown subset cards use, as HTML on a single line.

    Newlines are spent on nothing: Anki collapses them, so a code block carries
    its own <br>s and every block is a real element.
    """
    html = []
    for kind, lines in blocks(unwrap(text).split("\n")):
        if kind == "code":
            body = "<br>".join(escape(line) for line in lines)
            html.append(f"<pre><code>{body}</code></pre>")
        elif kind == "p":
            html.append(f"<p>{inline(lines[0])}</p>")
        else:
            items = "".join(f"<li>{inline(line)}</li>" for line in lines)
            html.append(f"<{kind}>{items}</{kind}>")
    return "".join(html)


def to_field(text):
    """A markdown fragment as one import field, quoted when it has to be."""
    field = render(text)
    if '"' in field or "\n" in field:
        return '"' + field.replace('"', '""') + '"'
    return field


def split_qa(body):
    """`## Question` / `## Answer` if present, else the body as the front."""
    match = QA_RE.search(body)
    if match:
        return to_field(match.group(1)), to_field(match.group(2))
    return to_field(body), ""


def note_of(kb, meta, by_id, id_of):
    """The ID of the note a card stands for, or None where it names none."""
    sources = meta.get("sources") or []
    if not sources or not isinstance(sources[0], dict):
        return None
    path = resolve_resource(kb, sources[0].get("resource"), by_id)
    return id_of.get(path) if path else None


def render_understanding(meta, note_id):
    """The two fields of an Understanding Card, generated from frontmatter.

    The kind carries no question of its own, so the body is not read. The
    front asks for the note from memory; the back sends the reviewer to the
    note to check, and the grade is theirs.
    """
    title = escape(str(meta.get("title", "")))
    front = (
        f"<p>{title}</p>"
        "<p>Explain it: what the note says, and why it holds.</p>"
    )
    back = f"<p>Check against note <code>{escape(note_id)}</code>.</p>"
    return front, back


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
        return print(f"kb_export: no knowledge base found ({INIT} makes one)") or 1
    out = out or os.path.join(kb, "export", "kb-export.txt")
    root = deck_root(kb)

    items = list(read_items(kb))
    by_id = items_by_id(items)
    id_of = {path: str(meta.get("id", "")) for path, meta, _ in items}

    cards, seen, misgraded, ungraded = [], {}, [], []
    for path, meta, body in items:
        kind = kind_of(meta.get("type"))
        if kind is None:
            continue
        card_id = str(meta.get("id", ""))
        if card_id in seen:
            print(f"kb_export: error: duplicate card id {card_id!r}")
            print(f"  {seen[card_id]}\n  {path}")
            return print("kb_export: nothing written") or 1
        seen[card_id] = path
        grade = meta.get(IMPORTANCE_KEY)
        if grade is None:
            ungraded.append(card_id)
            continue
        if str(grade) not in IMPORTANCE:
            misgraded.append((path, grade))
            continue
        cards.append((path, meta, body, deck_of(kind, str(grade), root), kind))

    if misgraded:
        expected = " | ".join(IMPORTANCE)
        print(f"kb_export: error: unknown {IMPORTANCE_KEY} ({expected} expected)")
        for path, grade in misgraded:
            print(f"  {grade!r} in {path}")
        return print("kb_export: nothing written") or 1

    rows, deprecated, held_back, unresolved = [], [], [], []
    for path, meta, body, deck, kind in cards:
        if meta.get("status") == "deprecated":
            deprecated.append(str(meta.get("id")))
            continue
        if not is_approved(meta):
            held_back.append(str(meta.get("id")))
            continue
        if kind == UNDERSTANDING:
            note_id = note_of(kb, meta, by_id, id_of)
            # Held back rather than fatal: it makes one card useless and
            # corrupts nothing, unlike a repeated ID.
            if note_id is None:
                unresolved.append(str(meta.get("id")))
                continue
            front, back = render_understanding(meta, note_id)
        else:
            front, back = split_qa(body)
        rows.append(
            [front, back, deck, str(meta.get("id", "")), TAG_PREFIX + str(meta.get("id", ""))]
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
    if ungraded:
        print(f"kb_export: {len(ungraded)} ungraded, held back: {' '.join(ungraded)}")
    if unresolved:
        print(f"kb_export: {len(unresolved)} naming no note, held back: {' '.join(unresolved)}")
        print("  an understanding card's first source must be a note in this base")
    if deprecated:
        print(f"kb_export: {len(deprecated)} deprecated, omitted: {' '.join(deprecated)}")
        print("  omission does not suspend them — suspend in the scheduler by hand")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
