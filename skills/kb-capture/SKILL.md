---
name: kb-capture
description: Capture something the user has learned into their knowledge base, or a correction to what is already there, as a verified, dated capture. Use when the user dictates a piece of knowledge to keep — "capture this", "note that ...", "kb this", "add to my knowledge base" — or dictates a correction or addition to existing knowledge — "actually it's ...", "update the note about X" — typically while working inside a project repository. Repairs transcription against the real source, verifies the claims, reports discrepancies without fixing them. Also keeps agent-produced scaffolding (a diagram, a walkthrough) as an agent-authored capture, and suggests the general pattern under a project-specific one.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-capture

Writes a **Capture**: the user's words, transcription repaired, verified,
dated. Or your own output, `authored: agent`, when the user asks to keep it.

Invoke `/kb-common` skill if you haven't already.

1. **The dictation is the whole material** — the argument, or the message that
   invoked you. Never write a capture from the session, your analysis, or the
   code. Transcribe, don't summarise: keep their framing, emphasis and detail,
   hedges included.
2. **Glance at the base** — titles, a grep for the distinctive terms; a minute,
   not a survey. The same subject already there ⇒ the same slug, next free
   number, and offer `/kb-redact` afterwards to bring its note to the current
   state. An adjacent subject ⇒ its own slug. **Nothing dictated at all** —
   "check this against the code", "is this still true?" ⇒ `/kb-verify`, stop.
3. **Repair the transcription, verify at the requested effort, record `code`
   and `paths`** (`/kb-common`). `authored: human`.
4. **Write it** per the schema: title = the subject, not the claim. Don't list
   repairs or sources to the user. Until this session ends the capture stays
   open: a correction dictated now is edited into the text, repaired and
   verified like the rest. After it, it is closed (`/kb-common`).
5. **Asked to keep something you produced** — a diagram, a trace, a summary —
   write a second capture, `authored: agent`, same slug and next number, `from`
   the one it accompanies, verified against the code you read. Offer this when
   the session produced something worth keeping and the user did not ask.
6. **Suggest the general pattern** underneath, where the effort allows and you
   see one (`/kb-common`): one line, offered once, dropped if declined. A
   sentence dictated back is its own capture.
7. **Say what you left open** (`/kb-common`). Run the check.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md`
