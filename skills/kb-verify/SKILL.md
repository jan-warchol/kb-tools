---
name: kb-verify
description: Check an existing note against the current code and write what moved as a report, without touching the note. Use when the user asks whether something in the knowledge base is still true — "verify the note about X", "check this against the code", "is this still current?". Read-only on the note, its captures and its cards; the fix, if any, is /kb-capture then /kb-redact.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(git log *), Bash(git rev-parse *), Bash(git diff *), Bash(git show *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-verify

One note in, one report out. **You never edit the note, its captures or its
cards** — not the body, not `from`, not `status`, not `date`. The only file you
write is the report.

Invoke `/kb-common` skill if you haven't already.

1. **The note.** Named a capture ⇒ the note made from it (`--refs`). None ⇒ say
   captures are not re-verified, since they record what was checked then, offer
   `/kb-redact`, and stop. Several notes ⇒ one at a time, a report each.
2. **The chain**: the note's captures and their evidence, plus the note's own.
   The repository must be the one in the bearings; another ⇒ say which, stop.
3. **Cheap negative first**: `git log --oneline <commit>..HEAD -- <paths>` for
   each `code` in the chain. Nothing anywhere ⇒ say the note is current, write
   nothing, stop.
4. **Read what changed** and check the note against it at the requested effort
   — the note's sentences, not the captures': the note is the current state.
5. **Write the report**: an `authored: agent` capture in the note's pool, next
   free number, `from` the note, `code` at HEAD with the `paths` you read. Two
   sections, one line per finding, and nothing else:

   ```markdown
   ## Scaffolding that moved

   - `fetchState` → `loadState`, `src/state/load.go`

   ## Claims affected

   - "The value is fetched on demand." — `Sync.push` now stores it; the fetch
     is only called from `repair`.
   ```

   **Never the replacement wording**: that is the user's to say (`/kb-common`).
6. **Tell the user** in a few lines: scaffolding is applied through
   `/kb-redact` on their go-ahead, an affected claim waits for them to dictate
   the correction (`/kb-capture`). Run the check on the report.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md`
