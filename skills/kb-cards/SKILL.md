---
name: kb-cards
description: Make recall cards from a polished note. Use when the user wants cards — "make cards", "card this note". Quick cards in full; the deep card is a placeholder for now. Does not export.
allowed-tools: Read, Write, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-cards

One note in, cards out. You propose, the user approves. Export is separate.

## Bearings

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

Never copy an actor or a timestamp out of an example; re-sample with `date -u`.
No knowledge base means no cards: say so and offer `/kb-init`.

## Rules

- **A card asks only what the note says** — not its raw item, not the code, not
  what you know.
- **One fact, one quick card**, and the same fact never twice.
- **The user approves each card.** Unapproved is `status: draft` with no
  `verified` key; approval stamps the `human:` entry and makes it `stable`.
- **Card IDs are permanent.** `<note-id>-c<n>`, next free `n`, never reused or
  renumbered. Rewording an existing card keeps its ID; changing what it asks
  takes a new one.
- **A card's `sources` is the one note** — never a repo or a document.

## Procedure

**1. Pick a note.** Eligible: `origin: human`, has `verified`, `status: stable`.
A draft note produces nothing — offer `/kb-redact`. An `origin: machine` item
never produces cards. Take the one the user named, else the oldest with no
cards.

**2. Number from what exists.** Glob `<note-id>-c*` where the bearings show
cards live, and continue the sequence.

**3. Draft the quick cards.** One fact each, in the note's vocabulary. The
question must stand alone months later with one right answer. `title` names what
it asks about; the question lives in the body:

```markdown
**Q:** In what order do the ack and the retry happen for a failed message?

**A:** Ack first — the retry re-enqueues the message rather than holding it.
```

A note may yield several, one, or none.

**4. One placeholder deep card.** Rubrics are deferred, so the whole body is:

```markdown
This is a deep card for retry and ack ordering.
```

It is approved and exported like any other card, so this line is what the user
sees at review — it stands in as "explain this topic", with no rubric to grade
against yet. Filling it in later keeps the ID.

**5. Present, then write** the approved cards where cards live, per the schema.
`origin: human`, `verified` a single `human:` entry at approval, `status:
stable` when approved and `draft` otherwise. Leave the note's `cards:` alone —
export regenerates it.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```

**6. Report** the paths and what was approved.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
