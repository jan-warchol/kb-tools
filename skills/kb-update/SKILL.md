---
name: kb-update
description: Correct or extend something already in the knowledge base and carry the change downstream. Use when the user amends or corrects existing knowledge — "update the note about X", "actually it's ..." — when a capture has an appended section nothing has processed yet, or when a note's diagrams need redrawing against changed code.
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-update

The subject is already in the base: the raw layer is the log, the note is the
current state.

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

1. **Find the chain**: the capture above what was named, the note and cards
   below (search for the path; there are no back-references). Nothing covers
   it ⇒ `/kb-capture`.
2. **Split claim from instruction.** "Make that a table and add that it fires
   on shutdown" is both: the claim is recorded, the instruction carried out
   and never recorded. Ask where a fragment could be either.
3. **Repair, verify at the requested effort** (`/kb-common`).
4. **Append the claim to the capture** under `## Update — <date>` (or
   `## Correction`); `generated.at` moves, `generated.by` stays the user; add
   your `verified` entry and sources. Quick ⇒ heading `## Update (unverified)`
   and **stop here**: a note must not mix checked and unchecked claims.
5. **Fold it into the note.** The note loses whatever the update made false and
   never narrates its history. Then re-read the whole note: does it read as
   one document written today, or as a document with a postscript? Reordering
   and rewording the user's claims is not altering them.
6. **Machine blocks you redraw freely** — against the current code, new stamp,
   no approval needed. A code change that falsifies a *claim* is reported, not
   fixed: the user states the correction, or the claim is dropped on their
   say-so.
7. **Cards**: reword freely keeping the ID; one the note no longer supports is
   `status: deprecated` on the user's say-so. New cards are `/kb-cards`.
8. Write on approval (`approved` moves to now), record what you left open in
   the machine-origin capture (`/kb-common`), and run the check.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
