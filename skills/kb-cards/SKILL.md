---
name: kb-cards
description: Make recall cards from a polished note. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_cardid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-cards

One note in, cards out. You propose, the user approves. Export is separate.
Invoke `/kb-common` skill if you haven't already.

## Bearings

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

No knowledge base means no cards: say so and offer `/kb-init`.

## Rules

- **A card asks only what the note says** — not its raw item, not the code, not
  what you know.
- **One fact, one card**, and the same fact never twice. A fact split across
  two cards is reviewed twice for one piece of knowledge, and each showing
  primes the other.
- **The user approves each card**, one at a time — approval is per card, not
  per batch.
- **Card IDs are permanent**, and never invented — `kb_cardid.sh` draws them.
  Rewording an existing card keeps its ID; changing what it asks takes a new
  one, from a fresh draw.
- **A card's `sources` is the one note** — never a repo or a document.

## Procedure

**1. Pick a note.** Eligible: `origin: human`, has `verified`, `status: stable`.
A draft note produces nothing — offer `/kb-redact`. An `origin: machine` item
never produces cards. Take the one the user named, else the oldest with no
cards. **Nothing points from a note to its cards** — a note has cards if some
card names its path in `sources`, so grep the cards for `<note-id>.md`. Never
glob the slug instead: that sweeps in the cards of every note whose slug this
one is a prefix of.

**2. Draw the IDs.** One per card, in one call:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/kb_cardid.sh <note-id> <how-many>
```

Never write one yourself or adapt one from an example — the ID is also the
card's identity in Anki, where a repeat overwrites another card's history.

**3. Draft the cards.** `type: Recall Card` — one fact each, in the note's
vocabulary. The question must stand alone months later with one right answer.
`title` names what it asks about; the question lives in the body, under these
two headings — export reads them:

```markdown
## Question

In what order do the ack and the retry happen for a failed message?

## Answer

Ack first — the retry re-enqueues the message rather than holding it.
```

A note may yield several, one, or none.

The body is markdown, not HTML, and export joins soft-wrapped lines back into
one — blank lines, list items and fenced blocks are kept as structure, anything
else in a paragraph is run together. So wrap the file at 80 columns as usual,
and use a list where the answer needs line breaks in Anki.

**4. Present, then write** the approved cards where cards live, per the schema.
`origin: human`, `verified` a single `human:` entry at approval, `status:
stable` when approved and `draft` otherwise. The note is not touched: the card
cites it and nothing points back.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```

**5. Report** the paths and what was approved.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
