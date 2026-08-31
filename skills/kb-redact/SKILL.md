---
name: kb-redact
description: Turn captured raw items in the knowledge base into short, dense notes. Use when the user wants to redact, process, or work through their capture backlog — "redact", "process a capture", "turn these into notes". Compresses without altering any claim or losing the user's voice, verifies anything captured unverified, and never marks a note approved without the user's say-so. Does not make cards.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-redact

Turns raw items into short, dense notes: **one raw item, one note** by default. A
note may draw on several raw items where they are about the same thing; it then
cites every one of them.

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Rules

- **Compress; never alter a claim.** The note must assert exactly what the raw
  item asserts — no hedge added, no qualifier dropped, nothing sharpened beyond
  what verification settled (step 2). If compressing seems to require changing a
  claim, stop and ask.
- **Redaction reads raw items; it does not rewrite them.**
- **A contradiction stops you.** 

## Procedure

**1. Verify if capture did not.** An item with no `verified:` key is not
machine-confirmed — check its claims now, per `/kb-common`. Otherwise read only
what you need in order to compress accurately.

**2. Compress.** The note is what is left of the capture once everything
carrying no claim has been struck out — as short as that leaves it, in the
user's own words. It stands on its own: the user must never have to open the
raw item or the sources to understand it.

- **Cut words rather than replacing them.** The note should be reachable by
  striking things out of the capture rather than by writing new text. Where a
  sentence must be recast, recast it in the user's own words from elsewhere in
  the capture.
- **What goes:** false starts, digression, filler, scaffolding like "the thing
  to keep in mind is". Restatement — dictation says a thing vaguely and then
  precisely, so keep the precise one, their own better articulation. Of each
  surviving sentence ask which claim is lost if it goes; if none, it goes.
- **A hedge that verification settled goes.** "Probably", "I think", "if I
  remember right" record how sure the user was as they spoke, not what is true.
  Once confirmed, the `verified` entry carries that precisely and the hedge only
  understates what the item knows. Unconfirmed, or never checked, and it stays.
  A scope qualifier is not a hedge — "usually", "only when CORS is involved" are
  about the subject, not the speaker, and no checking removes one.
- **Bullets over prose** wherever the material is a list of facts: a bullet
  drops the connective tissue prose needs and nothing else. Reorder freely; add
  subheadings once there is enough to need them.
- **The test is recognition.** The user should read the note and think *that is
  what I said, tidied*. "A good summary of what I said" is a failure: accurate,
  and not theirs.

**3. Ask for approval.**

**4. On approval, write the note** alongside the existing notes, under the raw
item's date and slug with the next free number (`-2` where the raw item is
`-1`), per the schema below. Points the schema leaves to this step:

- `verified` carries every entry the raw item had, plus your own if step 1
  verified it, plus a `human:` entry stamped at the user's approval.
- `status: stable` on an approved note; it stays `draft` while unapproved.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
