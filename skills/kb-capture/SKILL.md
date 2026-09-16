---
name: kb-capture
description: Capture something the user has learned into their knowledge base as a verified, timestamped capture. Use when the user dictates a piece of knowledge to keep — "capture this", "note that ...", "kb this", "add to my knowledge base" — typically while working inside a project repository. Repairs transcription against the real source, verifies the claims, reports discrepancies without fixing them. Also keeps agent-produced scaffolding (a diagram, a walkthrough) as a machine-origin capture, and suggests the general pattern under a project-specific one.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-capture

Writes a **Capture**: the user's words, transcription repaired, verified,
timestamped. Or, with `origin: machine`, your own output — when the user asks
to keep it.

Invoke `/kb-common` skill if you haven't already.

1. **The dictation is the whole material** — the argument, or the message
   that invoked you. Never write a capture from the session, your analysis,
   or the code. Transcribe, don't summarise: keep their framing, emphasis and
   detail, hedges included.
2. **Glance at the base** — titles, a grep for the distinctive terms; a
   minute, not a survey. The same subject already there ⇒ `/kb-update`. An
   adjacent one ⇒ its own capture, with its own slug.
3. **Repair the transcription, verify at the requested effort, record the
   sources** (`/kb-common`). `generated` is the user, `verified` is you.
4. **Write it** per the schema: title = the subject, not the claim. Don't
   list repairs or sources to the user. Until this session ends the capture
   stays open: a correction or addition the user dictates now is edited into
   the text, repaired and verified like the rest. After it, it is closed
   (`/kb-common`, Changing items).
5. **Asked to keep something you produced** — a diagram, a trace, a summary —
   write a second capture with `origin: machine`, citing the one it
   accompanies (same slug, next number), verified against the code you read.
   Offer this when the session produced something worth keeping and the user
   did not ask.
6. **Suggest the general pattern** underneath, where the effort allows and
   you see one (`/kb-common`): one line, offered once. A sentence dictated
   back is its own capture, verified against the code in front of you and
   written to travel. Declined, it is not raised again.
7. **Say what you left open** (`/kb-common`, Stopping). Run the check.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/capture.md`
