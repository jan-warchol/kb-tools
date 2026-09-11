# Knowledge base frontmatter

The one description of the file format. Every other place that needs it — the
skills, the copy at `SCHEMA.md` in the knowledge base — either injects this file
or points at it. `scripts/kb_check.py` enforces it.

This describes frontmatter only. Where a file lives is not part of the format:
the directory names in the examples below are illustrative, and the knowledge
base is free to be arranged any way.

## Identity

An ID takes one of two forms, chosen by whether the item ever leaves the base:

| Scope | ID form | Example |
|---|---|---|
| stays in the base (raw item, note) | `<slug>_<n>` | `retry-wrapper_1` |
| leaves the base (e.g. a card) | 12 random base62 characters | `Xo1jycAlN4xQ` |

`<n>` is the lowest number free among items already sharing that slug — kind
is not part of identity, so a raw item and the note made from it share one
pool: a capture is usually `_1`, the note made from it `_2`.

Random IDs are drawn with `scripts/kb_randomid.sh [count]`, never invented.
Twelve base62 characters is 62^12 ≈ 3.2×10²¹ possible values, so collisions
stay unlikely even at scale: with ten million already drawn, the chance any
two of them collide is still only about one in 64 million.

**Filenames.** The filename must contain the full ID, and may carry a prefix
ahead of it, underscore-separated — a date, another slug, whatever helps
browsing. E.g. `2026-08-10_retry-wrapper_1.md`, `retry-wrapper_Xo1jycAlN4xQ.md`.
The ID is repeated in frontmatter so a moved or renamed file stays
identifiable.

## Common keys

Present on every item:

```yaml
id: retry-wrapper_2
type: Note        # kinds in use: Raw Capture, Note, Recall Card,
                  # Understanding Card, Quiz Log; not a closed set
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
timestamps that parse, an `id` the filename contains.

## `sources`

Every entry carries `resource`; the rest are optional. A leading `/` makes it
base-relative — that is how an item points at another item in the same knowledge
base.

```yaml
sources:
  - resource: /raw/2026-08-10_retry-wrapper_1.md   # another item in this base
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
id: retry-wrapper_1
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

**Note** — the slug of the raw item it came from, with the next free number.
`generated.by` is the agent (it wrote the text), `origin: human` (the
claims are the user's). `sources` begins with the raw item — with every one of
them, where the note draws on several — then every evidence source. `verified`
carries the raw item's entries plus a `human:` entry stamped at approval. A note
does not list its cards — references run from the derived item to what it came
from, so a note's cards are found by searching the cards for its path. A
back-reference would be a second copy of that fact, free to drift out of step
with the first.

```yaml
---
id: retry-wrapper_2
type: Note
title: Retry wrapper ordering
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:41:00Z }
status: stable
sources:
  - resource: /raw/2026-08-10_retry-wrapper_1.md
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
silently never exported. Two kinds are in use — `Recall Card` and
`Understanding Card`. A card's
`title` names what it asks about, so it can be identified in a listing without
being read; it is not the question, which lives in the body.

`importance` is `core` or `extra`, and splits the kind's deck again —
`Knowledge::Recall::Core`, `Knowledge::Recall::Extra` — so review load and
desired retention can be set separately for each. Absent, the card is **held
back from export**: undecided is a state of its own, not a default, because a
grade can only take effect before the card's first import. An unrecognised value
is fatal at export. It is the **initial placement, not a live
classification**: Anki does not move an existing card on re-import, and demoting
one there is the intended workflow, since whether a card has earned its place is
a judgement made during review from history this base cannot see. A card's deck
and its `importance` drifting apart is therefore expected, and not a defect to
reconcile — the same way the base records no interval or ease.

**Recall Card** — one fact, one answer. The body is `## Question` and
`## Answer`, and export reads those two headings. A body with neither is
exported whole as the front.

```yaml
---
id: Xo1jycAlN4xQ
type: Recall Card
title: Ack ordering on retry
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:42:00Z }
status: stable                         # deprecated ⇒ suspend, don't delete
importance: core                       # core | extra — initial deck only;
                                       # absent ⇒ held back from export
sources: [{ resource: /notes/2026-08-10_retry-wrapper_2.md }]
verified:
  - { by: human:jan, at: 2026-08-10T14:43:00Z }
---

## Question

In what order do the ack and the retry happen for a failed message?

## Answer

Ack first — the retry re-enqueues the message rather than holding it.
```

**Understanding Card** — asks whether the user can *reason* with a note, and is
graded by `/kb-quiz`, never in Anki's reviewer. It carries no question: **the
card is the note**, so at most one exists per note, and both fields Anki
receives are generated at export from the frontmatter — no body is read, or
needed. Rewriting the note therefore never obsoletes its card. Its `sources` is
the note it stands for, and that is what `/kb-quiz` resolves.

```yaml
---
id: 7bQr2mKp9xLd
type: Understanding Card
title: Retry wrapper ordering           # what it is about, not a question
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:42:00Z }
status: stable
importance: core                        # graded at export, as for any kind
sources: [{ resource: /notes/2026-08-10_retry-wrapper_2.md }]
verified:
  - { by: human:jan, at: 2026-08-10T14:43:00Z }
---
```

**Quiz log** — what `/kb-quiz` asked, what the user answered, and how each
answer was graded. `origin: machine`: what it asserts is the agent's grading,
not the user's knowledge. Anything the user says during a quiz that is worth
keeping leaves through `/kb-update` or `/kb-capture` instead, so a log is
written once and never revised.

`sources` lists **every note quizzed**, and that is how the next quiz finds it:
search the logs for the note's path, exactly as a note's cards are found. The
`verified` entry is the agent's, and says the grades were arrived at by reading
the note and its sources rather than from memory of them.

The ID is the note's slug with the next free number where one note was quizzed,
and `quiz-<date>` where the session spanned several — a scheduled review
usually does.

```yaml
---
id: retry-wrapper_3
type: Quiz Log
title: Quiz — retry wrapper ordering
origin: machine
generated: { by: claude-code/opus-5, at: 2026-08-14T09:20:00Z }
status: stable
sources:
  - resource: /notes/2026-08-10_retry-wrapper_2.md
verified:
  - { by: claude-code/opus-5, at: 2026-08-14T09:20:00Z }
---

## Retry wrapper ordering

**Q.** A message fails after the wrapper has run. What is in the queue?
**A.** "a copy of it, re-enqueued" — correct
**Q.** Why does the ack not wait for the retry to succeed?
**A.** "so the consumer doesn't block" — partial: missed that the broker would
redeliver it.
```

## Identity in Anki

Every exported card carries the tag `kb::<card id>` — the card ID is the `guid`
too, but no Anki interface reads a guid back out, so the tag is what traces a
card there back to the file here. It is written for every kind, not only the
one that needs it today.

An Understanding Card's generated front repeats its note's ID and its back says
to quiz on it. Both are a fallback for a human or an agent reading the card in
Anki; the tag is the mechanism, and `sources` stays the one authority.
