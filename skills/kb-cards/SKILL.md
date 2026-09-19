---
name: kb-cards
description: Make recall cards from an approved note or capture. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-cards

One item in, cards out. You propose, the user approves.

Invoke `/kb-common` skill if you haven't already.

1. **Eligible**: `origin: human`, `status: stable`, and `approved` — a note,
   or a capture the user points at directly, where asking for cards is itself
   the approval: stamp it then. Unverified ⇒ offer `/kb-redact` instead.
   Machine blocks are invisible here: nothing inside one becomes a card.
   Existing cards: `kb_find.py --refs <id>`.
2. **How many is the effort** (`/kb-common`) — the obvious one or two, or a
   full sweep. Never cards across items. **The understanding card is always
   proposed** for a note that has none, at every effort, alongside the recall
   cards.
3. **Draw IDs** for every card in one call, never write one yourself:
   `${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh <how-many>`.
4. **Draft**: one fact, one card, never the same fact twice; asks only what
   the item says, in its vocabulary; stands alone months later with one right
   answer. Short — answers under 10 words ideally, never over 20, up to 4
   bullets; an example is visually separate from the answer.
5. **An Understanding Card asks nothing itself**: `sources` names the note,
   export generates its two fields, and it has no body.
6. **Approve one at a time.** Turned down ⇒ dropped; reworded ⇒ shown again.
   Write only approved cards: `sources` the item by `kb:<id>`, `approved` at
   approval, `status: stable`, no `importance` (graded at export). Filename
   `<slug>_<id>.md`.
   **The item turns out wrong** while you draft ⇒ stop carding it. The user's
   correction is a claim: a new capture, verified on the spot, the note's
   section edited and re-approved (`/kb-common`, Changing items) — then carry
   on from the corrected note.
7. **IDs are permanent**: rewording keeps the ID, changing what is asked takes
   a new one.
8. Report paths and what you left open (`/kb-common`), run the check, then
   the export: new cards wait there for a grade (`/kb-export`), changed ones
   need an import.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/card.md`
