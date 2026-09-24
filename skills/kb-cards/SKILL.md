---
name: kb-cards
description: Make recall cards from a confirmed note or capture. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-cards

One item in, cards out. You propose, the user approves.

Invoke `/kb-common` skill if you haven't already.

1. **Eligible**: `authored: human` and `status: confirmed` — a note, or a
   capture the user points at directly, where asking for cards is itself the
   confirmation: stamp it then. Still `draft` ⇒ offer `/kb-redact` instead.
   Agent blocks are invisible here: nothing inside one becomes a card. Existing
   cards: `kb_find.py --refs <id>`.
2. **How many is the effort** (`/kb-common`) — the obvious one or two, or a
   full sweep. Never cards across items.
3. **Draw IDs** for every card in one call, never writing one yourself:
   `${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh <how-many>`.
4. **Draft**: one fact, one card, never the same fact twice; asks only what the
   item says, in its vocabulary; stands alone months later with one right
   answer. Short — answers under 10 words ideally, never over 20, up to 4
   bullets; an example is visually separate from the answer.
5. **Approve one at a time.** Turned down ⇒ dropped; reworded ⇒ shown again.
   Write only approved cards: `from` the item by `kb:<id>`, `status:
   confirmed`, no `importance` (graded at export). Filename `<slug>_<id>.md`.
   **The item turns out wrong** while you draft ⇒ stop carding it. The user's
   correction is a claim: a new capture (`/kb-capture`), the note's section
   edited and re-confirmed — then carry on from the corrected note.
6. **IDs are permanent**: rewording keeps the ID, changing what is asked takes
   a new one.
7. Report paths and what you left open (`/kb-common`), run the check, then the
   export: new cards wait there for a grade (`/kb-export`).

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md`
