---
name: kb-cards
description: Make recall cards from an approved note or capture. Use when the user wants cards — "make cards", "card this note". Does not export.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh *), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
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
   the item says, at the scope set below; stands alone months later with
   one right answer.
   - **Scope**: ask at the most general level the claim holds — a fact
     about HTTP isn't asked as a fact about the vendor the note came from.
     That level may be wider than the item states; the blind check (step 4)
     tests it. A condition the answer needs — a platform, a version, a
     default — goes in the question as scope, so the answer stays short.
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
4. **Blind check** — one subagent for the whole batch, never one per card.
   It gets each card's question and answer and the evidence the item cites
   (repository and paths at their `commit`, URLs) — not the item, not this
   conversation: it reads each card the way the user will months later.
   Per card: is the answer true as stated, for the scope the question sets?
   Name a concrete case where it is wrong, checked against the evidence or
   the authoritative documentation, never from memory. One line per card —
   holds, wrong, or unverifiable — pointing at what is wrong, never at the
   fix. Every round after the first re-checks only the cards that changed.
5. **Show all drafts together**, numbered, each with its blind-check
   finding; the user approves, rewords or drops each. Turned down ⇒
   dropped; reworded ⇒ checked and shown again. Feedback on one card that
   applies to others (scope, length, wording) is applied to all of them
   before the next round. A finding is never applied silently: where the
   card says what the item says, the finding is against the item (step 6,
   the item turns out wrong); where the card went beyond it — a widened
   scope, a word the user added — narrow the card or let the user reword it.
6. **Draw IDs** once the cards are approved, for all of them in one call,
   never write one yourself:
   `${CLAUDE_PLUGIN_ROOT}/scripts/kb_randomid.sh <how-many>`.
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
