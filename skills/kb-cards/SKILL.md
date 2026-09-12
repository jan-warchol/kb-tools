---
name: kb-cards
description: Make recall cards from an approved note or capture. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-cards

One item in, cards out. You propose, the user approves. Export is separate.

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

1. **Eligible**: `origin: human`, `status: stable`, and `approved` — a note,
   or a capture the user points at directly, where asking for cards is itself
   the approval: stamp it then. Unverified ⇒ offer `/kb-redact` instead.
   Machine blocks are invisible here: nothing inside one becomes a card.
2. **How many is the effort** (`/kb-common`) — the obvious one or two, a full
   sweep, or a sweep plus cross-item cards.
3. **Draw IDs** for every card in one call, never write one yourself:
   `${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh <how-many>`.
4. **Draft**: one fact, one card, never the same fact twice; asks only what
   the item says, in its vocabulary; stands alone months later with one right
   answer. Short — answers under 10 words ideally, never over 20, up to 4
   bullets; an example is visually separate from the answer.
5. **An Understanding Card asks nothing itself**: `sources` names the note and
   export generates its two fields. Put the questions worth asking about the
   note — and follow-ups the note deserves — in a **machine block** in its
   body, for `/kb-quiz` to draw on. They are suggestions, not claims: the user
   approves the card, not them, and nothing there is ever exported.
6. **Approve one at a time.** Turned down ⇒ dropped; reworded ⇒ shown again.
   Write only approved cards: `approved` at approval, `status: stable`, no
   `importance` (graded at export). Filename `<slug>_<id>.md`.
7. **IDs are permanent**: rewording keeps the ID, changing what is asked takes
   a new one.
8. Report paths and what you left open (`/kb-common`), and run the check.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
