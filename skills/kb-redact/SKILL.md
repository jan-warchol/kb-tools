---
name: kb-redact
description: Turn captured raw items in the knowledge base into polished notes. Use when the user wants to redact, process, or work through their capture backlog — "redact", "process my captures", "turn these into notes". Polishes without altering any claim, verifies anything captured unverified, and never marks a note approved without the user's say-so. Does not make cards.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-redact

Turns raw items into polished notes: **one raw item, one note**. Cards are a
separate step.

## Bearings

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

Never copy an actor or a commit out of an example, and re-sample the time with
`date -u` rather than reusing one. Redaction needs a knowledge base: if there is
none, say so and offer `/kb-init`.

## Rules

- **Polish; never alter a claim.** The note must assert exactly what the raw
  item asserts — no hedge added, no qualifier dropped, nothing sharpened. If
  polishing seems to require changing a claim, stop and ask.
- **Approval is the user's to give.** You may write the note as a draft before
  they have seen it, but never stamp the `human:` entry that marks it approved,
  and never let an unapproved note out of `status: draft`.
- **Redaction reads raw items; it does not rewrite them.** Change one only if
  the user asks you to.
- **A contradiction stops you.** Report it, quote the source, write nothing. The
  user decides what to say instead — usually as a new capture.

## Procedure

**1. Pick from the backlog.** The backlog is the raw items with no note — a note
takes its raw item's ID, so the difference between the two sets is the worklist.
Take the ones the user named, else the oldest. One at a time reads best, but
work through a batch if that is what they asked for.

**2. Verify, if capture did not.** An item with no `verified:` key is not
machine-confirmed and cannot produce cards: check its claims as `/kb-capture`
would, and record what you read as fully as capture would have — the
repo-relative `path`, the `symbol` where meaningful, and the `commit`, which
cannot be recovered later. The absent key is the test, not the raw item's
`status`.

Otherwise read only what you need in order to polish accurately. Re-verifying
what capture already checked is not this step's job.

**3. Polish.** Rewrite the body to read well in six months to someone who has
forgotten the context. Cut repetition, false starts and digression. Impose
structure only where the material has it. Keep the user's framing and
vocabulary, and fold in nothing you learned while verifying — that belongs in
`sources`, not in the prose, because the claims in a note are the user's.

**4. Present.** Show the note and ask for approval. Writing it first is fine —
as `status: draft`, with no `human:` entry, which is inert until step 5.

**5. On approval, write the note** alongside the existing notes, taking the raw
item's ID, per the schema below. Points the schema leaves to this step:

- `verified` carries every entry the raw item had, plus your own if step 2
  verified it, plus a `human:` entry stamped at the user's approval.
- `status: stable` on an approved note. It stays `draft` while it is unapproved,
  and when step 2 could not verify it — an unverified note is not allowed to
  produce cards.
- Leave `cards:` alone — it is generated on export.

Then optionally `kb_check.py` the file, and say how many items remain on the
worklist:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the file you wrote>
```

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
