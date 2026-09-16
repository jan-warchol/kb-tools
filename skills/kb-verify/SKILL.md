---
name: kb-verify
description: Check an existing note against the current code and write what moved as a report, without touching the note. Use when the user asks whether something in the knowledge base is still true — "verify the note about X", "check this against the code", "is this still current?". Read-only on the note, its captures and its cards; the fix, if any, is /kb-update.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(git log *), Bash(git rev-parse *), Bash(git diff *), Bash(git show *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-verify

One note in, one report out. **You never edit the note, its captures or its
cards** — not the body, not `sources`, not `verified`, not `generated.at`. The
only file you write is the report.

Invoke `/kb-common` skill if you haven't already.

1. **The note.** Named a capture ⇒ the note made from it (`kb_find.py --refs`).
   None ⇒ say captures are not re-verified — they record what was checked
   then — offer `/kb-redact`, and stop. Several notes ⇒ one at a time, a
   report each.
2. **The chain**: the note's captures and their evidence, plus any evidence
   the note lists itself. The repository must be the one in the bearings;
   another ⇒ say which, and stop.
3. **Cheap negative first**: `git log --oneline <commit>..HEAD -- <paths>` per
   evidence entry. Empty ⇒ unchanged. Everything unchanged ⇒ say the note is
   current, write nothing, stop.
4. **Read what changed** and check the note against it, at the requested
   effort (`/kb-common`) — the note's sentences, not the captures': the note is
   the current state.
5. **Write the report** — a machine capture in the note's slug pool, next
   free number: first source `kb:<note id>`, then the evidence you read, with
   `commit` at HEAD. Two sections, one line per finding, and nothing else:
   - **Scaffolding that moved** — old → new, and where.
   - **Claims affected** — the note's sentence, quoted; what the code shows,
     pointed at. **Never the replacement wording**: that is the user's to say
     (`/kb-common`, Don't give the answer away).
6. **Tell the user** in a few lines, and offer `/kb-update`: scaffolding is
   applied on their go-ahead without touching approval; an affected claim
   waits for them to dictate the correction. Run the check on the report.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/capture.md`
