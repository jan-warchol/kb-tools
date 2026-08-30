---
name: kb-redact
description: Turn captured raw items in the knowledge base into polished notes. Use when the user wants to redact, process, or work through their capture backlog — "redact", "process my captures", "turn these into notes". Polishes without altering any claim, verifies anything captured unverified, and never marks a note approved without the user's say-so. Does not make cards.
allowed-tools: Read, Write, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-redact

Turns raw items into polished notes: **one raw item, one note**.

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Rules

- **Polish; never alter a claim.** The note must assert exactly what the raw
  item asserts — no hedge added, no qualifier dropped, nothing sharpened. If
  polishing seems to require changing a claim, stop and ask.
- **Redaction reads raw items; it does not rewrite them.**
- **A contradiction stops you.** 
- **No knowledge base, no redaction.** Unlike capture, this reads raw material
  and writes notes, so it has no working-directory fallback: say so and offer
  `/kb-init`.

## Procedure

**1. Verify, if capture did not.** An item with no `verified:` key is not
machine-confirmed — check its claims now, per `/kb-common`. Otherwise read only
what you need in order to polish accurately.

**2. Polish.** Rewrite the body to read well in six months to someone who has
forgotten the context. Cut repetition, false starts and digression. Reorder if
appropriate. Add structure - bullet lists, paragraphs, subheadings.
Keep the user's framing and vocabulary.

**3. Ask for approval.**

**4. On approval, write the note** alongside the existing notes, taking the raw
item's ID, per the schema below. Points the schema leaves to this step:

- `verified` carries every entry the raw item had, plus your own if step 1
  verified it, plus a `human:` entry stamped at the user's approval.
- `status: stable` on an approved note; it stays `draft` while unapproved.

Then check the frontmatter — it catches mechanical mistakes, and a skip when
PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the file you wrote>
```

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
