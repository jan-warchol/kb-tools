---
name: kb-cards
description: Make recall cards from a polished note. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
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
  per batch. Approval settles the wording and nothing else.
- **Importance is not graded here.** An approved card is written with no
  `importance:` and waits: export holds it back until it has one. Grading a card
  beside the note that produced it is the worst vantage available — everything
  looks important there. The grade wants several notes' cards side by side,
  which is where `/kb-export` reports them.
- **Card IDs are permanent.** A card ID doubles as its Anki guid, where a
  repeat silently overwrites another card's review history — rewording a card
  keeps its ID; changing what it asks takes a new one.
- **Cards must be short,** especially answers. Don't use full sentences. Less
  than 10 words is ideal, more than 20 should be avoided. Bullets are ok (up to
  4). If explanation/example is necessary for understanding, make sure it's
  visually separate from the answer.

## Procedure

**1. Check the note** the user named — ask which one where they named none.
Eligible: `origin: human`, has `verified`, `status: stable`. An unverified note
is not allowed to produce cards — offer `/kb-redact`.

**2. Draw the IDs.** One per card, understanding cards counted, in one call — never write one yourself, and
never adapt one from an example:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh <how-many>
```

**3. Draft the cards.** `type: Recall Card` — one fact each, in the note's
vocabulary. The question must stand alone months later with one right answer. A
note may yield several, one, or none.

Offer an `Understanding Card` too where a note is worth understanding and not
merely knowing — at most one, often none. No question and no body: `sources`
names the note, export generates the fields, `/kb-quiz` grades it.

**4. Present, then write** the approved cards where cards live, per the schema.
`origin: human`, `verified` a single `human:` entry at approval, `status:
stable` when approved and `draft` otherwise, and no `importance:` — that is graded later. The note is not touched: the card
cites it and nothing points back. A card ID is opaque, so name the file
`<slug>_<id>.md` — a short slug of what the card asks, as a prefix ahead of
the ID — to keep a directory listing legible; the slug is decoration, the ID
is what identifies the file.

**5. Report** the paths and what was approved.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
