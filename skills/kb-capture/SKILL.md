---
name: kb-capture
description: Capture something the user has learned into their knowledge base as a verified, timestamped raw item. Use when the user dictates a piece of knowledge to keep — "capture this", "note that ...", "kb this", "add to my knowledge base" — typically while working inside a project repository. Repairs transcription against the real source, verifies the claims, reports discrepancies without fixing them.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-capture

Writes a **raw item**: the user's own words, transcription repaired, verified,
timestamped.

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Rules

- **The user articulates; you never substitute for that** (`/kb-common`).
  Never write a capture from the session transcript, your own analysis, or the
  code.
- **You are transcribing, not summarising:** keep user's framing, emphasis and
  level of detail.

## Procedure

**1. Take the dictation.** 

**2. Check whether the base already holds this subject.** Glance over the item
titles, grep the distinctive terms — a minute, not a survey; friction here loses
captures. An item on the same subject makes this an update to it: `/kb-update`.
An adjacent subject is still its own capture, citing that item.

**3. Repair the transcription** (`/kb-common`).

**4. Verify the claims** (`/kb-common`).

**5. Record the sources** (`/kb-common`).

**6. Write the raw item** per the schema below.

- **title**: short and specific — the subject, not the claim.
- **body**: their words, cleaned of transcription errors and nothing else.
- **`generated`** is the user, **`verified`** is you: different actors doing
  different jobs.

Don't list transcription repairs and verification sources to the user.

## Capturing without verification

When the user has no time to verify ("quick", "don't verify"), skip step 4 only.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
