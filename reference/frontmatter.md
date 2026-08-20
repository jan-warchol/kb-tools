# Knowledge base frontmatter

The one description of the file format. Every other place that needs it — the
spec, the skills, the copy at `SCHEMA.md` in the knowledge base — either injects
this file or points at it. `scripts/kb_check.py` enforces it.

This describes frontmatter only. Where a file lives is not part of the format:
the directory names in the examples below are illustrative, and the knowledge
base is free to be arranged any way.

## Identity

| Kind | ID form | Example |
|---|---|---|
| raw item | `<YYYY-MM-DD>-<slug>` | `2026-08-10-retry-wrapper` |
| note | same ID as its raw item | `2026-08-10-retry-wrapper` |
| card | `<note-slug>-<10 random>` | `retry-wrapper-DXo1jycAlN` |
| source transcript | `<YYYY-MM-DD>-<slug>` | `2026-08-16-cap-theorem` |
| source summary | `<slug-id>-summary` | `2026-08-16-cap-theorem-summary` |

The filename is `<id>.md`, and the ID is repeated in frontmatter so a moved file
stays identifiable. A raw item and the note derived from it share an ID —
identity is the pair of kind and ID. Within a kind, a second item that would
take an ID already in use gets a numeric suffix (`-2`, `-3`).

A card ID is the odd one out: no date, and a random tail in place of a counter.
Draw it with `scripts/kb_cardid.sh <note-id> [count]` and never invent one — a
card ID doubles as the card's identity in the scheduler, where a repeat silently
overwrites another card's review history. **Card IDs are permanent**: rewording
a card keeps its ID, changing what it asks takes a new one.

## Common keys

Present on every item:

```yaml
id: 2026-08-10-retry-wrapper
type: Note        # the kinds in use: Raw Capture, Note, Recall Card,
                  # Source Transcript, Source Summary — not a closed set
title: Retry wrapper ordering    # required on every item, cards included
origin: human                    # human | machine
generated: { by: claude-code/opus-5, at: 2026-08-10T14:35:00Z }
status: stable                   # draft | stable | deprecated
```

`origin` says **whose claims these are**, and is never inferred: `human` means
the content asserts what the user asserted. It is a different question from
`generated.by`, which records who produced the *text* — a polished note is
written by the agent and still carries `origin: human`, while an ingested
article is transcribed verbatim and is still `origin: machine`.

Actors follow OKF §7: `human:jan`, `claude-code/opus-5`, `process:export`.
Timestamps are UTC, from `date -u +%Y-%m-%dT%H:%M:%SZ`, never invented.

## `verified`

A list of `{ by, at }`, kept separate from `generated` because whoever wrote
something need not be whoever checked it. Three tiers follow (OKF §5.3):

| Tier | Condition |
|---|---|
| unverified | no `verified` key — must carry `status: draft` |
| machine-confirmed | entries present, none from a `human:` actor |
| human-reviewed | at least one `human:` actor entry |

A note must be machine-confirmed or better *and* out of `status: draft` before
it can produce cards — a draft note is one the user has not approved, or one
nothing has verified. A card
must be human-reviewed before it is exported, because that entry *is* the
user's approval — a card that has been proposed and not yet approved is
`status: draft` and carries no `verified` key.

On an ingested source the entry means the text is faithful to the original, not
that the original is correct.

**Unverified means draft**, for everything. That is the one rule `kb_check.py`
enforces about meaning; the rest of what it checks is shape — required keys,
timestamps that parse, an `id` matching the filename. It deliberately knows
nothing about item kinds or where files live, so neither can be changed by
editing the script.

## `sources`

Every entry carries `resource`; the rest are optional. A leading `/` makes it
base-relative — that is how an item points at another item in the same knowledge
base.

```yaml
sources:
  - resource: /raw/2026-08-10-retry-wrapper.md   # another item in this base
  - resource: https://github.com/acme/backend    # repository
    path: src/queue/retry.py                     # or paths: [a.py, b.py]
    symbol: RetryWrapper                         # optional; or symbols: [...]
    commit: a1b2c3d                              # what it was verified against
  - resource: https://peps.python.org/pep-0492/  # document
    author: human:gvanrossum                     # only if the source names one
    retrieved: 2026-08-10
```

`path` and `symbol` each have a plural form taking a list; use whichever fits
what verification actually touched, never both forms of the same key in one
entry. `commit` and `retrieved` record *what the claim was checked against* and
are written at capture — revalidation reads them, and they cannot be recovered
once the verifying context is gone.

The **first** source of a derived item is the item it was derived from: a note
cites its raw item, a summary cites its transcript. That link is what marks the
original as processed. A summary written where no transcription was possible has
nothing internal to cite, and names the original directly.

Frontmatter is authoritative. Prose may name a file inline where it aids
reading; those mentions are decorative and are not maintained.

## Per kind

**Raw item** — `origin: human`, `generated.by` is the user (they dictated it),
`verified` entries are the agent's. Normally left as written.

```yaml
---
id: 2026-08-10-retry-wrapper
type: Raw Capture
title: Retry wrapper ordering
origin: human
generated: { by: human:jan, at: 2026-08-10T14:32:00Z }
verified:
  - { by: claude-code/opus-5, at: 2026-08-10T14:35:00Z }
status: stable
sources:
  - resource: https://github.com/acme/backend
    path: src/queue/retry.py
    symbol: RetryWrapper
    commit: a1b2c3d
---

`RetryWrapper` is applied inside `Consumer.handle`, so the message is acked
first and the retry re-enqueues it rather than holding it.
```

**Note** — same ID as its raw item. `generated.by` is the agent (it wrote the
text), `origin: human` (the claims are the user's). `sources` begins with the
raw item, then every evidence source. `verified` carries the raw item's entries
plus a `human:` entry stamped at approval. A note does not list its cards —
references run from the derived item to what it came from, so a note's cards are
found by searching the cards for its path.

```yaml
---
id: 2026-08-10-retry-wrapper
type: Note
title: Retry wrapper ordering
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:41:00Z }
status: stable
sources:
  - resource: /raw/2026-08-10-retry-wrapper.md
  - resource: https://github.com/acme/backend
    path: src/queue/retry.py
    symbol: RetryWrapper
    commit: a1b2c3d
verified:
  - { by: claude-code/opus-5, at: 2026-08-10T14:35:00Z }
  - { by: human:jan, at: 2026-08-10T14:41:00Z }
---
```

**Card** — `sources` are notes only, never a repository or a document directly:
a card is a question about a note, and where the claim came from is recorded
there. One kind is in use — `Recall Card`, one fact and one answer. A card's
`title` names what it asks about, so it can be identified in a listing without
being read; it is not the question, which lives in the body.

The body is `## Question` and `## Answer`, and export reads those two headings.
A body with neither is exported whole as the front.

```yaml
---
id: retry-wrapper-DXo1jycAlN
type: Recall Card
title: Ack ordering on retry
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:42:00Z }
status: stable                         # deprecated ⇒ suspend, don't delete
sources: [{ resource: /notes/2026-08-10-retry-wrapper.md }]
verified:
  - { by: human:jan, at: 2026-08-10T14:43:00Z }
---

## Question

In what order do the ack and the retry happen for a failed message?

## Answer

Ack first — the retry re-enqueues the message rather than holding it.
```

**Source transcript and summary** — both `origin: machine`. The transcript cites
the original; the summary cites the transcript first, then the original, so it
stays traceable on its own.

```yaml
---
id: 2026-08-16-cap-theorem
type: Source Transcript
title: CAP theorem revisited
origin: machine
generated: { by: claude-code/opus-5, at: 2026-08-16T09:12:00Z }
status: stable
sources:
  - resource: https://codahale.com/you-cant-sacrifice-partition-tolerance/
    author: human:codahale
    retrieved: 2026-08-16
verified:
  - { by: claude-code/opus-5, at: 2026-08-16T09:12:00Z }
---
```
