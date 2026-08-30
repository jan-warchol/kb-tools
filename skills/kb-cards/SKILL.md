---
name: kb-cards
description: Make recall cards from a polished note. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_cardid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-cards

One note in, cards out. You propose, the user approves. Export is separate.

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Rules

- **A card asks only what the note says** — not its raw item, not the code, not
  what you know.
- **One fact, one card**, and the same fact never twice. A fact split across
  two cards is reviewed twice for one piece of knowledge, and each showing
  primes the other.
- **The user approves each card**, one at a time — approval is per card, not
  per batch.

## Procedure

**1. Pick a note.** Eligible: `origin: human`, has `verified`, `status: stable`.
A draft note produces nothing — offer `/kb-redact`. An `origin: machine` item
never produces cards. Take the one the user named, else the oldest with no
cards — grep the cards for `<note-id>.md`, and never glob the slug instead:
that sweeps in the cards of every note whose slug this one is a prefix of.

**2. Draw the IDs.** One per card, in one call — never write one yourself, and
never adapt one from an example:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/kb_cardid.sh <note-id> <how-many>
```

**3. Draft the cards.** `type: Recall Card` — one fact each, in the note's
vocabulary. The question must stand alone months later with one right answer. A
note may yield several, one, or none.

Export joins soft-wrapped lines back into one, keeping blank lines, list items
and fenced blocks as structure. So wrap the file at 80 columns as usual, and use
a list where the answer needs line breaks in Anki.

**4. Present, then write** the approved cards where cards live, per the schema.
`origin: human`, `verified` a single `human:` entry at approval, `status:
stable` when approved and `draft` otherwise. The note is not touched: the card
cites it and nothing points back.

**5. Report** the paths and what was approved.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
