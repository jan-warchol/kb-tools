---
name: kb-capture
description: Capture something the user has just said they learned into their knowledge base as a verified, timestamped raw item. Use when the user dictates a piece of knowledge to keep — "capture this", "note that ...", "kb this", "add to my knowledge base" — typically while working inside a project repository. Repairs transcription against the real source, verifies the claims, reports discrepancies without fixing them, and writes one raw item.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-capture

Writes **one raw item**: the user's own words, transcription repaired, verified,
timestamped. Notes and cards are separate steps.

## Bearings

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

Never copy an actor, a timestamp or a commit out of an example — that writes a
false provenance record.

## Rules that are not negotiable

- **The user articulates; you never substitute for that.** Capture what the
  user said. Never compose the knowledge on their behalf — not from this
  session's transcript, not from your own analysis, not from the code. If they
  say "capture what we just worked out", ask them to state it: articulating is
  the step that does the learning.
- **You report discrepancies; the user fixes them.** On finding a claim that
  conflicts with reality, stop and report. Never write a corrected version of
  their claim, however obvious the correction. Transcription repair is the one
  exception — recovering the identifier they meant to say does not change what
  they claimed.
- **A missing knowledge base never blocks a capture.** Write into the working
  directory and say so. Stopping to configure something loses the capture.

One capture writes one file. Raw items are normally left as written afterwards,
so a later correction is usually a new capture — but that is a default, not a
prohibition: edit or delete one when the user asks you to.

## Procedure

**1. Take the dictation.** If the skill was invoked with no text, ask for it and
wait. You are transcribing, not summarising: keep their framing, emphasis and
level of detail.

**2. Repair transcription — silently.** Dictation mangles exactly the words
carrying the meaning: identifiers whose casing was lost, `camelCase` /
`kebab-case` confusions, approximated paths, similar-sounding substitutions
(`ack` / `act`, `enqueue` / `and queue`).

Read the code to find the real spelling; never guess a plausible one, and ask if
you cannot tell what was meant. Repair only what was *meant* as an identifier:
"the config file" stays as spoken even where the parameter is called
`fileSettings`, because describing a thing in plain English is not a
mis-transcription of its name. These repairs are not recorded in the file — the
raw item holds what the user meant to say — but list them in your report so the
user can object, including when step 3 stops you before there is a file.

**3. Verify the claims.** Check what they said against evidence: the codebase
when the claim is about code, other sources otherwise. Verify each claim as
stated, including the parts that sound obviously right — read the code, do not
reason from identifier names. Two things this step is routinely under-read on:

- **A dictated sentence carries several claims**, and the `so` joining two of
  them asserts a third. Check each and report every outcome — a true fact glued
  to another by a false `because` is exactly the error worth catching.
- **Verification usually has to leave the symbol the user named.** Follow the
  behaviour: the ack they attribute to a wrapper may happen in its caller.

Three outcomes, per claim:

- **Confirmed** — proceed, recording what you actually read.
- **Contradicted** — **stop.** Report what you found, quote the source, and ask
  what they want to say instead; write nothing yet. Their correction is folded
  into the text — the raw item holds the user's words, not the exchange that
  produced them.
- **Not checkable** with what is available — say so and ask whether to record
  it unverified. Never mark something verified because it sounds right.

**4. Write the raw item** where the bearings show raw material lives, per the
schema below.

- **title**: short and specific — the subject, not the claim.
- **body**: their words, cleaned of transcription errors and nothing else.
  Dictation arrives unpunctuated, so sentence breaks are part of writing down
  what was said; changing the words is not. Keep repetition and asides —
  polishing belongs to redaction.
- **`generated`** is the user, **`verified`** is you: different actors doing
  different jobs, so rarely the same timestamp.
- **`sources`** records where verification actually looked. Record it now:
  revalidation reads exactly these fields, and they cannot be recovered once
  the verifying context is gone.
- If the dictation covers two unrelated subjects, split it into two raw items
  and say so in your report.

Then, optionally, check the frontmatter — it catches mechanical mistakes, and a
skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the file you wrote>
```

**5. Report** the path, the transcription repairs, and — where any are
outstanding — **how many raw items still have no note**: a note takes its raw
item's ID, so an ID present in raw material and absent from notes is one still
unredacted.

## Capturing without verification

When the user has no time to verify ("quick", "don't verify"), skip step 3 only.
Still repair transcription, still record any sources you touched, and write **no
`verified:` key** with `status: draft`. Tell them it cannot produce cards until
redaction verifies it. This defers the cost rather than removing it: do not
offer the mode unprompted, and do not fall back to it because verification is
turning out to be laborious.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
