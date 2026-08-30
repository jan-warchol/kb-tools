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

## Rules that are not negotiable

- **The user articulates; you never substitute for that** (`/kb-common`).
  Never write a capture from the session transcript, your own analysis, or the
  code.
- **Transcription repair is the one exception** to reporting rather than
  fixing: recovering the identifier they meant to say does not change what they
  claimed.
- You are transcribing, not summarising: keep user's framing, emphasis and level
  of detail.

## Procedure

**1. Take the dictation.** 

**2. Repair transcription.** Dictation mangles exactly the words
carrying the meaning: identifiers whose casing was lost, `camelCase` /
`kebab-case` confusions, approximated paths, similar-sounding substitutions
(`ack` / `act`, `enqueue` / `and queue`).

Read the code to find the real spelling; never guess a plausible one, and ask if
you cannot tell what was meant. Repair only what was *meant* as an identifier:
"the config file" stays as spoken even where the parameter is called
`fileSettings`, because describing a thing in plain English is not a
mis-transcription of its name.

**3. Verify the claims**, per `/kb-common`. Fold whatever correction the user
gives into the text — the raw item holds the user's words, not the exchange that
produced them.

**4. Write the raw item** per the schema below.

- **title**: short and specific — the subject, not the claim.
- **body**: their words, cleaned of transcription errors and nothing else.
  Dictation arrives unpunctuated, so sentence breaks are part of transcription.
- **`generated`** is the user, **`verified`** is you: different actors doing
  different jobs.

## Capturing without verification

When the user has no time to verify ("quick", "don't verify"), skip step 3 only.
Still repair transcription, and still record any sources you touched.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
