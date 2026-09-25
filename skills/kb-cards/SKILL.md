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
   full sweep. Never cards across items.
3. **Draft**: one fact, one card, never the same fact twice; asks only what
   the item says; stands alone months later with one right answer.
   - **Scope**: ask at the most general level the claim holds — a fact
     about HTTP isn't asked as a fact about the vendor the note came from.
     Keep the specific name only where the item says it is specific.
   - **Open questions**: the question names the subject, never the answer
     or its category. No hints, no parts of the answer in the
     setup, no judgement to confirm ("why is X better") — ask "what is the
     difference" instead.
   - **Short answers**: under 10 words ideally, never over 20, up to 4
     bullets; count before showing. Keep the item's own load-bearing
     phrase rather than paraphrasing it. An example is visually separate.
   - **Coverage**: a "what is it" card for each central term the item
     defines; avoid cards from asides or parentheticals; a what and its why
     sharing one answer are one card.
4. **Show all drafts together**, numbered; the user approves, rewords or
   drops each. Turned down ⇒ dropped; reworded ⇒ shown again. Feedback on
   one card that applies to others (scope, length, wording) is applied to
   all of them before the next round.
5. **Draw IDs** once the cards are approved, for all of them in one call,
   never write one yourself:
   `${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh <how-many>`.
   Write only approved cards: `sources` the item by `kb:<id>`, `approved` at
   approval, `status: stable`, no `importance` (graded at export). Filename
   `<slug>_<id>.md`.
   **The item turns out wrong** while you draft ⇒ stop carding it. The user's
   correction is a claim: a new capture, verified on the spot, the note's
   section edited and re-approved (`/kb-common`, Changing items) — then carry
   on from the corrected note.
6. **IDs are permanent**: rewording keeps the ID, changing what is asked takes
   a new one.
7. Report paths and what you left open (`/kb-common`), run the check, then
   the export: new cards wait there for a grade (`/kb-export`), changed ones
   need an import.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/card.md`
