---
name: kb-update
description: Correct or extend something already in the knowledge base and carry the change downstream. Use when the user dictates a correction or addition to existing knowledge — "update the note about X", "actually it's ..." — or asks for a scaffolding change across a note and its cards (a URL, a renamed identifier, a redrawn diagram), including applying a verify report. Without a dictated claim or instruction, checking an item against the code is /kb-verify.
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-update

The subject is already in the base: the slug pool is the log, the note is the
current state. One note per run.

Invoke `/kb-common` skill if you haven't already.

1. **Find the chain** with `kb_find.py`: the note, its slug pool, its cards
   (`--refs`). Nothing covers it ⇒ `/kb-capture`. **No claim dictated and no
   instruction given** — "check this against the code", "is this still
   true?" ⇒ `/kb-verify`, and stop.
2. **Split claim from instruction.** "Make that a table and add that it fires
   on shutdown" is both: the claim is recorded, the instruction carried out
   and never recorded. Ask where a fragment could be either.
3. **Report before writing.** Anything in the chain the code now contradicts
   — beyond what the user just said — stops you here: quote it, let the user
   dictate the correction or drop the claim. Nothing is written until that is
   settled.
4. **Record the claim in a new capture** — same slug, next free number;
   edited in place only if this session wrote it. Repaired, and **verified on
   the spot** whatever the effort; `generated.by` the user. Quick ⇒ stop here.
5. **Bring the note to the current state.** Normal: edit the sections the
   claim affects. Thorough: rebuild the note from its whole slug pool, newer
   captures winning. Either way the note loses what became false, never
   narrates its history, and every sentence outside a machine block traces to
   a human capture. Re-read it whole: one document written today, or a
   document with a postscript? Add the new capture to `sources`.
6. **Scaffolding** — a URL, a path, a renamed identifier, a diagram redrawn
   against the current code, a verify report's "Scaffolding that moved" —
   applies across the note and its cards directly: no capture, `approved` and
   `generated.at` untouched.
7. **Cards**: reword freely keeping the ID; one the note no longer supports is
   `status: deprecated` on the user's say-so. New cards are `/kb-cards`.
8. **Present, then write on approval.** A claim or a requested rewording ⇒
   `approved` and `generated.at` move to now; scaffolding only ⇒ neither moves
   (`/kb-common`, Changing items). Run the check, then the export whenever a
   card changed, and tell the user to import. Say what you left open.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/capture.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/note.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/card.md`
