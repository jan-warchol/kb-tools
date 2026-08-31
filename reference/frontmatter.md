# Knowledge base frontmatter

The one description of the file format. Every other place that needs it — the
skills, the copy at `SCHEMA.md` in the knowledge base — either injects this file
or points at it. `scripts/kb_check.py` enforces it.

Kinds belonging to a separable capability live in a `frontmatter-*.md` fragment
beside this file; `/kb-init` appends every fragment to `SCHEMA.md`.

This describes frontmatter only. Where a file lives is not part of the format:
the directory names in the examples below are illustrative, and the knowledge
base is free to be arranged any way.

## Identity

An ID is `[<date>-]<slug>-<suffix>`: an optional `YYYY-MM-DD`, a slug, and a
suffix that is either a number or a random string. The suffix is always there —
it is what makes **every ID unique across the base**, kind included: kind is not
part of identity.

| Kind | ID form | Example |
|---|---|---|
| raw item | `<date>-<slug>-<n>` | `2026-08-10-retry-wrapper-1` |
| note | its raw item's date and slug, next free `<n>` | `2026-08-10-retry-wrapper-2` |
| card | `<note-slug>-<10 random>` | `retry-wrapper-DXo1jycAlN` |

The filename is `<id>.md`, and the ID is repeated in frontmatter so a moved file
stays identifiable. `<n>` is the lowest number free among the items already
sharing that date and slug, so a capture is normally `-1` and the note made from
it `-2`. That shared prefix is a convenience when reading a directory listing
and nothing more: what pairs a note with its raw item is the `sources` entry —
which is why a note may draw on several raw items and cite each of them.

A card ID is the odd one out: no date, and a random tail in place of a number.
Draw it with `scripts/kb_cardid.sh <note-id> [count]` and never invent one — a
card ID doubles as the card's identity in the scheduler, where a repeat silently
overwrites another card's review history. **Card IDs are permanent**: rewording
a card keeps its ID, changing what it asks takes a new one.

## Common keys

Present on every item:

```yaml
id: 2026-08-10-retry-wrapper-2
type: Note        # kinds in use: Raw Capture, Note, Recall Card;
                  # not a closed set
title: Retry wrapper ordering    # required on every item, cards included
origin: human                    # human | machine
generated: { by: claude-code/opus-5, at: 2026-08-10T14:35:00Z }
status: stable                   # draft | stable | deprecated
```

`origin` says **whose claims these are**, and is never inferred: `human` means
the content asserts what the user asserted. It is a different question from
`generated.by`, which records who produced the *text* — a polished note is
written by the agent and still carries `origin: human`. `machine` is the mirror
image: material whose claims are not the user's, however it was produced.

`generated.at` marks the content's **last meaningful change**, not when the
file was first written: appending an update to an item moves it. Read against
`verified`, that is what says whether an item has changed since it was last
checked — a `generated.at` later than the last `verified.at` means it has — and
a derived item whose `generated.at` is older than its source's is behind it.

Actors follow OKF §7: `human:jan`, `claude-code/opus-5`, `process:export`. The
ones in this file are illustrative: take the human actor from the `user:` the
bearings report and the machine actor from your own model ID, never from an
example here.
Timestamps are UTC, ISO 8601 — `date -u +%Y-%m-%dT%H:%M:%SZ` produces them.

## `verified`

A list of `{ by, at }`, kept separate from `generated` because whoever wrote
something need not be whoever checked it.

**Unverified means draft**, for everything. That is the one rule `kb_check.py`
enforces about meaning; the rest of what it checks is shape — required keys,
timestamps that parse, an `id` matching the filename.

## `sources`

Every entry carries `resource`; the rest are optional. A leading `/` makes it
base-relative — that is how an item points at another item in the same knowledge
base.

```yaml
sources:
  - resource: /raw/2026-08-10-retry-wrapper-1.md   # another item in this base
  - resource: https://github.com/acme/backend    # repository
    path: src/queue/retry.py                     # or paths: [a.py, b.py]
    symbol: RetryWrapper                         # optional; or symbols: [...]
    commit: a1b2c3d                              # what it was verified against
  - resource: https://peps.python.org/pep-0492/  # document
    author: human:gvanrossum                     # only if the source names one
    retrieved: 2026-08-10
```

A repository is named by URL, never by a local path: where the checkout sits is
machine-local, so an item naming it would be false on the next machine — and an
item survives the checkout moving precisely because it never named the place.
`path` is relative to the root of the repository named by `resource`, never to
the working directory the item was written from. `path` and `symbol` each have a
plural form taking a list; use whichever fits what verification actually
touched, never both forms of the same key in one entry.

`commit` and `retrieved` record *what the claim was checked against* and are
written at capture — revalidation reads them, and they cannot be recovered
once the verifying context is gone.

The **first** source of a derived item is the item it was derived from — a note
cites its raw item. That link is what marks the original as processed.

Frontmatter is authoritative. Prose may name a file inline where it aids
reading; those mentions are decorative and are not maintained.

## Per kind

**Raw item** — `origin: human`, `generated.by` is the user (they dictated it),
`verified` entries are the agent's. Normally not rewritten once written — a
later correction is a section appended to the end of it.

```yaml
---
id: 2026-08-10-retry-wrapper-1
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

**Note** — the date and slug of the raw item it came from, with the next free
number. `generated.by` is the agent (it wrote the text), `origin: human` (the
claims are the user's). `sources` begins with the raw item — with every one of
them, where the note draws on several — then every evidence source. `verified`
carries the raw item's entries plus a `human:` entry stamped at approval. A note
does not list its cards — references run from the derived item to what it came
from, so a note's cards are found by searching the cards for its path. A
back-reference would be a second copy of that fact, free to drift out of step
with the first.

```yaml
---
id: 2026-08-10-retry-wrapper-2
type: Note
title: Retry wrapper ordering
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:41:00Z }
status: stable
sources:
  - resource: /raw/2026-08-10-retry-wrapper-1.md
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
there. **A card kind is a `type` ending in `Card`** — export dispatches on that
and names the subdeck after what precedes it, so a kind spelled otherwise is
silently never exported. One kind is in use — `Recall Card`, one fact and one
answer. A card's
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
sources: [{ resource: /notes/2026-08-10-retry-wrapper-2.md }]
verified:
  - { by: human:jan, at: 2026-08-10T14:43:00Z }
---

## Question

In what order do the ack and the retry happen for a failed message?

## Answer

Ack first — the retry re-enqueues the message rather than holding it.
```
