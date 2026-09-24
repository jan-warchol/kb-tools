# 0.17 — the settled design

What the simplification came to after review. This supersedes the first draft;
where the draft and this disagree, this is what holds.

**Nothing here is implemented yet except where marked.** Commit `d0269ad` on
this branch implements the *first draft*, so it diverges from this document in
the ways §7 names. The code has not been touched since.

## 1. Frontmatter — one format, every kind

The decision under everything else: **all kinds share one frontmatter format,
stated once.** Per-kind schema files did not merely duplicate, they drifted —
at 0.16 `core.md` still licensed agent blocks "inside an `origin: human` note
or card" although the only card kind that ever carried one had been removed,
and the `sources` rules were stated three times over. No single file was wrong
on its own, which is why nobody caught it.

```yaml
---
id: retry-wrapper_3
type: Note                       # Capture | Note | Recall Card
title: Retry wrapper ordering    # the subject, not a claim
authored: human                  # human | agent — whose claims these are
date: 2026-08-10                 # the item's last substantive change
confirmed: { by: human, at: 2026-08-11 }
sources:
  - kb:retry-wrapper_1
  - url: https://github.com/acme/backend
    at: a1b2c3d
    paths: [src/queue/retry.py]
    symbols: [RetryWrapper.handle]
---
```

Optional besides: `retired: <date>`, and `importance: core | extra` on a card.

**`authored`** replaces `origin` *and* `generated.by`. The byline names whose
claims these are, never who typed — typing is not authorship
(`motivation.md` §1.3), so a note the agent worded from the user's captures is
`authored: human`. A separate key for the typist went false in use: an agent
appended its own claims to a dictated capture while the byline still read as
the user's. Which model wrote a file is in git. The `human:<user>` actor prefix
goes — one base, one user.

**`date`** replaces `generated.at`, as a plain `YYYY-MM-DD`. It overlaps
`confirmed.at` for confirmed items but not for drafts, where it is the only
record of when something was captured; dictated Monday and redacted Tuesday is
a real gap, so both stay.

*(Implemented in `d0269ad`, both of them.)*

## 2. Sources — one field, several entries, mixed kinds

**Settled, and not what the draft said.** The draft collapsed evidence to a
single `code: <url>@<commit>` plus `paths:`, which foreclosed two things that
happen routinely: more than one source, and evidence that is not a repository.
A link to documentation is as good a source as a file.

One `sources:` field, in block style. A bare string where there is nothing more
to say; a mapping where there is:

```yaml
sources:
  - kb:retry-wrapper_1
  - url: https://github.com/acme/backend
    at: a1b2c3d
    paths: [src/queue/retry.py]
    symbols: [RetryWrapper.handle]
  - url: https://peps.python.org/pep-0492/
    at: 2026-08-11
```

- **One field, not two.** Splitting derivation from evidence was rejected: the
  identifier's own form says which it is, so a script projects whichever subset
  a caller wants, and the old "derived items list what they came from first"
  ordering convention stops mattering.
- **`at:` covers a commit and a retrieval date.** Both answer "which version
  did I read", and nothing ever compares them.
- **Plurals only** — `paths:` and `symbols:`. The singular/plural duality and
  its checker rule go.
- **Symbols stay.** For some claims a symbol locates better than a file.
- **Volume is capped instead**: about **three specifiers per source**, spent on
  paths or symbols, whichever locates the claim better. Guidance in the skill;
  `kb_check.py` warns only past something clearly excessive across the item,
  since occasionally five paths really do matter.
- **Consequence to know:** `/kb-verify`'s cheap negative is
  `git log <commit>..HEAD -- <paths>`, which consumes paths only. A source
  recorded purely as symbols cannot be change-detected that way. For a repo
  source where staleness matters, at least one path earns its place.

Dropped from the old format: `resource:` as a wrapper key, `retrieved:` as a
key of its own (now `at:`), and the singular forms.

## 3. Lifecycle — `confirmed:`, and what happens to `status`

**Settled: one `confirmed: { by, at }` key**, where `by` is `human` or `agent`
— verification when the agent did it, approval when the user did. Same actor
vocabulary as `authored`, so there is one vocabulary rather than two.

This reverses the 0.13 split of `verified` and `approved`, knowingly. That
split existed so carding eligibility could mean "approved" and thereby exclude
the whole machine layer without a second rule (`design-review.md` §2.8).
**`authored: agent` already delivers that**, so the constraint that forced the
split is gone and this is now a free choice. What made the old pair painful was
plausibly the growing *list* rather than the split itself — untested, and
untestable until the corpus is bigger.

**Open — my recommendation, not yet agreed.** Whether `status` survives
alongside it. `status: confirmed` and a `confirmed:` stamp would mean the same
thing in two places.

My view: **drop the enum.** Retirement is not a third point on the
draft→confirmed axis — an item is retired *after* having been confirmed — so
one enum cramming both loses the record that a retired item was ever true. Two
optional keys carry it instead:

| state | keys |
|---|---|
| draft | neither |
| confirmed | `confirmed: { by, at }` |
| abandoned before it was ever settled | `retired: <date>` |
| was true, stopped being true | both |

Export gates on "`confirmed` present, `retired` absent". A draft carries
neither key, so the commonest early state is the shortest. And the distinction
the `deprecated`/`abandoned` merge lost comes back for free.

Cost: "is this live?" is a two-key test rather than one word; `kb_find.py`'s
status column becomes derived; presence/absence is marginally more error-prone
for an agent than an enum, though the checker catches nonsense combinations.

**Fallback if you want an enum:** `status` stays the single vocabulary,
`confirmed:` is its detail, and `kb_check.py` enforces that the two imply each
other — redundant, but undriftable.

## 4. Claims may enter without a capture

**Settled.** "Every sentence outside an agent block traces to a human capture"
is a *mechanism*; the principle behind it (`motivation.md` §1.3) is that the
user articulated it. Those came apart, and the mechanism is what was limiting.

Restated: **every claim in an `authored: human` item is one the user
articulated — in a capture, or in the conversation at hand.** What stays
forbidden is the agent composing a claim nobody said, which is what actually
went wrong in the Case B failure; text that skipped a capture was never the
problem.

That allows all three things the mechanism was blocking: a note with no capture
behind it when the subject is simple enough, a card drawn directly, and a claim
entering through `/kb-redact` without a round trip. "If it is substantial, it
should be recorded" becomes guidance with a threshold rather than a gate.

**What it costs:** the trace rule was mechanically checkable — point at the
sentence's source — and `verification-gaps.md` §4.4 leaned on it precisely
because prose rules about authorship had already failed once. This trades a
check for a judgement. Partly covered: `kb_check.py` still warns when a note
*has* captures in its pool and skips one; a note with no pool is not checked.

## 5. Commands — five, `/kb-update` dissolved

**Settled, conditional on §4.** `/kb-update` becomes `/kb-capture` then
`/kb-redact`: its step 4 is what capture does, its step 5 what redact does, and
its scaffolding/cards/export steps are clauses in redact. This removes a
routing decision the user had to make correctly, and a wrong one is what caused
the Case A failure.

The residual risk the draft named — a dictated correction landing in
`/kb-redact` instead of `/kb-capture`, leaving a claim with no capture behind
it — is largely defused by §4: that is now a legal state rather than a
corruption.

`/kb-verify` stays its own skill. Its value is what it may *not* do, it
declares no `Edit`, and it prevents the failure the project exists to prevent.

*(Implemented in `d0269ad`.)*

## 6. Batching reads

**Settled, and wanted from the start.** Not the originally-floated "strip
metadata" script: frontmatter is short and flat now, and the agent usually
needs `authored`, `confirmed` and `sources` to decide what is cardable and
whose claims it is handling — strip them and it reads twice.

The version that pays is batching. **`kb_find.py --pool <slug> --bodies`**
prints, in one call, a metadata line plus the frontmatter-stripped body for
every item in the pool; `--refs <id> --bodies` does the same for what refers to
an item. The saving is N−1 round trips and the agent's own path-guessing.
`/kb-redact` opens a subject with one call instead of N — and this is where the
content-without-metadata idea actually pays, since the metadata line already
carries what is needed.

## 7. Where `d0269ad` diverges from this

The branch implements the first draft. To match this document it needs:

1. `code:` + `paths:` reverted to `sources:` (§2), in `reference/schema.md`,
   `kb_check.py`, `kb_migrate.py`, `kb_find.py`, and the skills that mention
   evidence. `kb_export.py` is unaffected.
2. `status:` replaced by `confirmed:` / `retired:` (§3) — pending the open
   question — in the same places plus `kb_export.py`'s gate.
3. The capture-trace rule restated (§4) in `reference/schema.md`,
   `kb-common`, `/kb-cards` (eligibility) and `/kb-redact`.
4. `--bodies` added to `kb_find.py` (§6), and `/kb-redact` told to use it.
5. The quiz lessons preserved (§8).

Everything else in `d0269ad` stands: the unified schema file, `authored`,
`date`, the dissolved `/kb-update`, the deleted design-history documents, and
the move of the Anki import mechanics into `reference/anki-setup.md`.

## 8. The quiz lessons, which the draft deleted carelessly

Understanding cards and quizzing are coming back once the rest settles. The
deleted `design-review.md` and `design-review-2.md` held the accumulated
lessons about how to quiz *well*, and git is a poor home for something you will
want again. Preserve these as entries under the two `deferred.md` rows that
already point at the subject:

- **Write the expected answer first**, and discard the question if the answer
  exceeds the mode's length. An agent cannot check a question against a length
  constraint, because it is evaluating the question while the constraint is on
  the answer; making it generative fixes that.
- **Quick mode measures recognition** — four-for-four on multiple choice over
  notes the user wrote themselves — so recommend one grade lower than the score
  suggests.
- **Ask all of a note's questions together**, then move to the next note. A
  rewrite silently dropped this once already.
- **"What changed" is the human captures in a note's slug pool newer than its
  latest quiz log.** Still computable: ID numbers within a pool are monotone,
  so day-granularity `date` does not break the ordering.
- **The quiz may ask about an agent block**, and the claim the user states in
  answering is theirs — the one route out of agent material.
- **Report, never delete**: a card missing from the markdown is reported, not
  removed. A parser bug must not reach review history.
- **The grade is proposed, never sent unasked.**

Two notes on restoring the kind itself: `kb_export.py` still dispatches on any
`type` ending in `Card` and names the deck from the prefix, so
`Understanding Card` needs no export change beyond its generated fields; and
`reference/schema.md` currently says agent blocks live inside a *note*, which
was where understanding cards kept their suggested questions — one word to
widen when the kind returns.

## 9. Parked

- **Whether sources pay for themselves.** Worth measuring — strip `sources:`
  from copies of real notes, have a fresh agent verify both versions, compare
  which files it reads and whether it reaches the same verdict. Parked until
  the corpus is around ten updated notes; at two it would measure noise.
  Nothing needs building for it, since `at:` and paths are recorded anyway.

## 10. Superseded from the first draft

Recorded so they are not re-proposed:

- **`code:` + `paths:`, one repository at one commit per item** — foreclosed
  multiple and non-repository sources (§2).
- **Splitting derivation from evidence into two fields** — the identifier's
  form already says which (§2).
- **Flow-style one-line source entries** — saves punctuation, not content, and
  costs readability and clean diffs.
- **Dropping `symbols:`** — sometimes a better locator than a path (§2).
- **`status: draft | confirmed | retired` as a single enum** — conflates two
  orthogonal axes (§3).
- **"Every sentence traces to a human capture"** — a mechanism mistaken for the
  principle (§4).
- **A script that strips metadata from item content** — break-even at best;
  batching is the win (§6).
