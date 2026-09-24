# Knowledge base format

`scripts/kb_init.sh` copies this into the base as `SCHEMA.md`;
`scripts/kb_check.py` enforces the shape. Why it is this way is in
`decisions.md`. Where a file lives is not part of the format.

## Identity

An item that stays in the base is `<slug>_<n>`, where `<n>` is the lowest free
number in **the slug pool** — one subject's captures, its note and its verify
reports, whatever their kind. A card leaves the base and is 12 random base62
characters from `scripts/kb_randomid.sh`, never invented. The filename ends in
the ID, optionally after a prefix (`2026-08-10_retry-wrapper_1.md`). Find items
with `scripts/kb_find.py` — by ID, by pool, or by what refers to them — never by
guessing a path.

## Keys

```yaml
---
id: retry-wrapper_3
type: Note                           # Capture | Note | Recall Card
title: Retry wrapper ordering        # the subject, not a claim
authored: human                      # human | agent — whose claims these are
date: 2026-08-10                     # when the claims last changed
status: confirmed                    # draft | confirmed | retired
from: [kb:retry-wrapper_1, kb:retry-wrapper_2]
code: https://github.com/acme/backend@a1b2c3d
paths: [src/queue/retry.py]
---
```

- **`authored`** — whose claims, never who typed: a note you worded from the
  user's captures is `human`. **Nothing `authored: agent` is ever carded.**
- **`date`** — `date -u +%F`. It moves when the claims change, not on a
  scaffolding fix.
- **`status`** — `draft` until checked against the source and kept by the user;
  `retired` once no longer true, or not worth pursuing. Never delete. A claim
  that changes returns the item to `draft` until the user accepts it.
- **`from`** — what this was derived from: `kb:<id>` for an item in this base,
  a URL for an outside document. Derived items list what they came from first.
- **`code` / `paths`** — the evidence: one repository at one commit, paths
  relative to its root, written when the claims are checked. A handful of
  paths — what the claims turn on, not everything opened. Recorded once, where
  it was read, never copied down the chain.

| Kind | `from` | |
|---|---|---|
| Capture | evidence only; the item it concerns when `authored: agent` | one session, one author; open while the session that wrote it runs, closed after |
| Note | its captures, then other notes | the current state of one subject; every sentence outside an agent block traces to a human capture |
| Recall Card | the one item it is drawn from | never evidence; body `## Question` and `## Answer`; `importance: core \| extra`, absent ⇒ held back at export; the ID is permanent, so rewording keeps it |

## Agent blocks

Inside an `authored: human` note, your own material is fenced:

```markdown
<!-- agent -->
a diagram, a walkthrough — scaffolding for the current state, never history
<!-- /agent -->
```

Nothing inside is carded; the file stays `authored: human`; you redraw a block
freely. A delta report is not one — that is a verify report, an
`authored: agent` capture. Captures need no blocks: `authored` covers the file.
