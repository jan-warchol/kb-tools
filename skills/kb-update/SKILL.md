---
name: kb-update
description: Correct or extend something already in the knowledge base and carry the change downstream. Use when the user amends or corrects existing knowledge — "update the note about X", "actually it's ..." — or when a raw item has an appended section nothing has processed yet.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-update

The subject is already in the base: what the user just said belongs on the
item that holds it.

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Rules

- **Raw items are append-only** — a section at the end, never an edit to what is
  there. A default, not a prohibition: asked to change or drop one, do it.
- **The raw layer is the log; the note is the current state.** The note absorbs
  the update and **loses whatever it made false**; it never narrates its own
  change history.
- **Never fold a human claim into an `origin: machine` item** — a remark about
  an ingested source is a new capture citing it.

## Procedure

**1. Find the chain** — the raw item above whatever the user named, and the
notes and cards below it (search for the path; there are no back-references).
Nothing covers the subject? Not an update: `/kb-capture`.

**2. Split the prompt into claim and instruction.** "Make that a bullet list and
add that it fires on shutdown" is both: the claim is recorded, the instruction
carried out and never recorded. Where a fragment could be either, ask.

**3. Repair the transcription** of the claim (`/kb-common`).

**4. Verify the claim** (`/kb-common`).

**5. Append to the raw item**: their words under `## Update — 2026-08-31`, or
`## Correction` where they are overturning themselves. `generated.at` moves to
now (the last meaningful change), `generated.by` stays the user; add your
`verified` entry and the `sources` you read, rewriting none.

**6. Carry it downstream.** Fold the update into the note — the instruction half
of the prompt applies here, shape being the note's business. Present it, write
on approval (`/kb-redact`). Then its cards: reword freely, **keeping the ID**;
one the note no longer supports is `status: deprecated` on the user's say-so,
suspended by hand in the scheduler. New cards are `/kb-cards`, not you.

**7. Report** paths, what was verified, what was deprecated, what is left.

## Without verification

"Quick" skips step 4, marks the heading `## Update (unverified) — …` and **stops
after step 5**: a note mixing checked and unchecked claims cannot say which is
which. Nothing else records that — `generated.at` now sits later than the last
`verified` entry, exactly "changed since last checked". Leave `status` alone.

That comparison is also how the leftovers are found, and they resume at step 4:
a raw item ahead of its last `verified` entry holds unchecked material, and a
note behind its raw item's `generated.at` has not caught up.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
