# Simplification proposal — 0.17

Everything humans and agents read is too long. This cuts it by about three
quarters without losing a capability the system is used for.

**Status: proposed, nothing implemented. Reconciled with `main` at 0.16.0**,
which removed `/kb-quiz`, the Quiz Log kind and the Understanding Card kind —
cuts in the same direction as this one, so what remains is six commands rather
than seven and four schema files rather than five.

| | now | after | |
|---|---|---|---|
| **agent-loaded** — `skills/`, `reference/schema/` | 709 | ~250 | −65% |
| **human-read** — `README`, `decisions`, `motivation`, `deferred`, the reviews | 1807 | ~255 | −86% |
| `reference/anki-setup.md`, read once, absorbs export's half | 137 | ~145 | — |
| **total** | 2653 | ~650 | −75% |

What an agent loads on one invocation — the skill, `kb-common`, and the schema
files that skill injects — falls from 350–470 lines to about 140:
`/kb-capture` 393 → 143, `/kb-redact` 433 → 157, `/kb-cards` 358 → 147,
`/kb-verify` 392 → 131, `/kb-export` 198 → 83, `/kb-update` 472 → dissolved.

Five changes, in order of what they pay.

---

## 1. Frontmatter: nine flat keys

### 1.1 `origin` + `generated` → `authored`

`origin` says *whose claims*; `generated.by` says *who typed*. Two keys for one
question, and the pair is what went false in Case B of `verification-gaps.md`
— a capture asserting `generated: { by: human:jan }` over text the agent had
partly composed.

**The byline names whose claims these are; there is no second key for who
typed, because typing is not authorship.** That is `motivation.md` §1.3 stated
in the schema rather than beside it. A note the agent worded from the user's
captures is `authored: human`, exactly as `origin: human` meant.

```yaml
authored: human      # human | agent
```

`human:<user>` and the model ID go with it. Nothing read either: `kb_user.sh`
exists only to fill the prefix, no script compares a model ID, and git records
which agent wrote a file. One user per base makes the name noise.

`generated.at` becomes `date:` — when the claims last changed, a scaffolding
fix not moving it, `date -u +%F`. ISO-to-the-second and its regex go; where two
items on one day need ordering, ID numbers already give it (numbers in a slug
pool only go up).

### 1.2 `verified` + `approved` → `status: confirmed`

Two `{by, at}` stamps, four lines, an enforcement rule each — for a distinction
the workflow never exercises. Every skill presents before it writes and works
one item per run, so the agent's check and the user's acceptance happen in the
same breath. They were split (`design-review.md` §2.8) to make carding
eligibility mean "approved" and so exclude machine material; `authored: agent`
already excludes it, wherever it sits.

```yaml
status: confirmed    # draft | confirmed | retired
```

- `draft` — unchecked, or claims changed since the user last saw them.
- `confirmed` — checked against the source and kept by the user. What
  `/kb-cards` and `/kb-export` gate on.
- `retired` — no longer true, or never pursued. `deprecated` and `abandoned`
  merge: both mean *don't drill this, don't delete it*, and only the reason
  differed, which nothing read.

Three reported problems go with them: no approval stamp to forget on a URL fix,
no unverified correction dictated mid-carding, no ceremony on a capture the
user cards directly.

### 1.3 `sources` → `from` / `code` / `paths`

The nested list is the longest thing in most files and carries three keys
nothing reads.

```yaml
# before                              # after
sources:                              from: [kb:retry-wrapper_1]
  - resource: kb:retry-wrapper_1      code: https://github.com/acme/backend@a1b2c3d
  - resource: https://github.com/…    paths: [src/queue/retry.py, src/queue/consumer.py]
    paths: [src/queue/retry.py, …]
    symbol: RetryWrapper
    commit: a1b2c3d
```

- **`from:`** — a flat list of what this was derived from: `kb:<id>`, or a URL
  for an external document. Derivation and citation answer one question.
- **`code:` + `paths:`** — the evidence, one repository at one commit.
  `/kb-verify`'s `git log <commit>..HEAD -- <paths>` is the only mechanical
  reader of either, and needs exactly this.

Dropped: `symbol`/`symbols` (decoration — `paths` is what `git log` takes),
`retrieved` (decoration), the singular/plural duality and its check, and more
than one repository per item, which the bearings already forbid. An item is
checked in one run against one HEAD, so one commit per item is the honest
shape.

### 1.4 The whole of it

```yaml
---
id: retry-wrapper_3
type: Note                       # Capture | Note | Recall Card
title: Retry wrapper ordering
authored: human
date: 2026-08-10
status: confirmed
from: [kb:retry-wrapper_1, kb:retry-wrapper_2]
code: https://github.com/acme/backend@a1b2c3d
paths: [src/queue/retry.py]
---
```

Nine keys, none nested, worst case nine lines. `kb_check.py`'s budget drops
from 20 lines to 12.

### 1.5 Agent blocks lose their stamp

`<!-- agent -->` … `<!-- /agent -->` replaces
`<!-- machine: claude-code/opus-5, 2026-09-12, commit a1b2c3d -->`: the stamp
duplicates the item's own `date` and `code`, and nothing reads it. The fence
stays — without it a note can hold no diagram, which is `design-review.md` C1.

---

## 2. One schema file instead of five

`reference/schema/` is 260 lines across four files, and a skill injects two to
four of them — 217 lines for `/kb-redact`, 260 for `/kb-update`. Most is
rationale `decisions.md` also holds, plus four frontmatter examples differing
in three lines.

**`reference/schema.md`, about 50 lines**: identity, the nine keys, agent
blocks, one worked example, and a three-row table saying what each kind's
`from:` holds and what is special about it. Every skill injects that one file,
and `kb_init.sh` copies it instead of joining four. Drafted in the appendix.

---

## 3. Five commands instead of six

**`/kb-update` dissolves** into `/kb-capture` then `/kb-redact`:

- its step 4 (record the dictated claim as a new capture in the pool) is what
  `/kb-capture` does, and `/kb-capture` already glances at the base and finds
  the existing subject;
- its step 5 (bring the note to the current state of its pool) is what
  `/kb-redact` does;
- steps 6–8 — scaffolding across note and cards, card rewording, export —
  become three clauses in `/kb-redact`.

`verification-gaps.md` §5 left this open; `design-review-2.md` kept the skill
because it "has a clear job". Under §1.2 that job shrinks to a routing decision
the user has to make correctly — and Case A is what a wrong one costs. Two
commands that cannot be picked wrongly beat three. `/kb-capture`'s description
absorbs "actually it's…" and "correct the note about X".

**`/kb-verify` stays separate**, at about 16 lines: it is the only skill whose
value is what it may *not* do, it declares no `Edit`, and it prevents the
failure the project exists to prevent. What it restates comes from `kb-common`.

**`/kb-export` shrinks to about 18 lines** — run the script, grade what is
ungraded, tell the user to import. It keeps its command because grading `core`
against `extra` has to see every ungraded card at once. Its three import
consequences (editing in Anki does not survive, moving decks does, renaming
means renaming twice) move to `reference/anki-setup.md`, where someone looks
when they hit one.

**`/kb-cards` stays separate from `/kb-redact`**: they share almost no
instructions — note shape versus question quality — so merging saves a preamble
and costs a longer file and a longer run.

---

## 4. `kb-common`: 160 lines to about 65

- **The effort table** (17 lines, 18 cells) goes. Three sentences replace it —
  quick does the minimum and stops, normal is the default, thorough follows the
  code paths; effort is depth, never breadth — plus one clause in each skill
  where the difference is real (the outline step, how many cards, how far
  verification reaches). The cells mostly restated the skill they named.
- **Changing items** loses its edit/approval table with `approved`. Two lines
  survive: a claim change returns the item to `draft` until the user accepts
  it; a scaffolding fix changes nothing else.
- **The general pattern**: 12 lines to 4. The harvest and the written-to-travel
  rule stay — they answer a structural bias (`motivation.md` §1.4) — the worked
  reasoning does not.
- **Bearings** loses the `KB user` line (§1.1).
- **Claims and scaffolding**, **Verification**, **Dictation**, **Stopping**
  keep their rules, lose their argumentation, and roughly halve.

---

## 5. The design-history documents go

`design-review.md` (750), `design-review-2.md` (171), `verification-gaps.md`
(401) and `Problems2.txt` (10) are 1332 lines of narrative about releases that
shipped — much of it about a quiz that no longer exists. A human reads them to
find out why something is the way it is — which
is `decisions.md`'s job, in a twentieth of the space.

Delete all four; git keeps them. Carry into `decisions.md`, as short entries,
only what would otherwise be re-litigated. Most is already there (§6 the fence
and no conversion, §8 read-only verification, one item per run, closed
captures). Two entries are new: **the two observed failures** — a verify pass
that rewrote its note, an agent appending its own claims under the user's
byline — as why the byline is the only authorship signal and why `/kb-verify`
cannot edit; and **the note layer is a projection of its slug pool**, with a
rebuild from the whole pool as thorough effort, not the default.

`decisions.md` 186 → ~90: §§1–5 (the Anki boundary) compress; §7's entries on
`verified`-as-a-list and on evidence-copying die with the keys they explain.

`motivation.md` 128 → ~85: §3 (Karpathy, OKF) becomes four lines naming what
was taken. §1 and §2 keep their argument — this is the one document that should
read like one.

`deferred.md` 80 → ~30: the table stays, its cells lose their second and third
sentences, and the appendix keeps only what cannot be re-derived — a repository
URL needs some way to be resolved to a checkout, and staleness must reach a
card through its note.

`README.md` 81 → ~50: one row fewer, the 0.14 upgrade section replaced by the
0.17 one, and "Reading" without the deleted files.

---

## 6. Scripts

Not cut, but they follow the format:

- **`kb_check.py`** — `authored` in `{human, agent}`, `status` in
  `{draft, confirmed, retired}`, `date` a `YYYY-MM-DD`, `from` a flat list
  resolving `kb:` entries, `code` matching `<url>@<commit>`. The actor-stamp
  checks, the `human:` rule, the legacy-list warning and the
  `generated.at > approved.at` warning all go. Net: shorter.
- **One check gained, worth more than the one lost.** §1.2 removes the
  stale-approval warning; replace it with one the new shape makes computable:
  **a `confirmed` note whose slug pool holds an `authored: human` capture not
  named in its `from:` is behind its pool.** That catches staleness the old
  pair never saw: a dictated correction that never reached the note.
- **`kb_export.py`** — gate on `status: confirmed`; drop the legacy
  `verified`-list path.
- **`kb_migrate.py`** — a 0.17 pass: `origin`+`generated` → `authored`+`date`,
  `verified`/`approved` → `status`, `sources` → `from`/`code`/`paths`,
  `deprecated`|`abandoned` → `retired`, `<!-- machine: … -->` → `<!-- agent -->`.
  The 0.14 pass goes once the one base is migrated.
- **`kb_user.sh`** — unused after §1.1; delete it and its bearings line.
- **`kb_find.py`** — prints `authored`/`status`/`date`.

---

## 7. What this gives up

1. **No mechanical guard on stale approval.** `kb_check.py` can no longer
   compare a claims timestamp against an approval timestamp. Mitigated by the
   pool check in §6 — strictly better at the case that actually occurred — and
   by the return-to-`draft` rule; but an agent that changes a claim and leaves
   `confirmed` standing is now uncatchable. This is the one place the old shape
   was doing work.
2. **No record of which model wrote a file**, outside git.
3. **No sub-day ordering**, and no cross-pool "what did I capture on Tuesday".
4. **One repository, one commit per item, no `symbol`.** An item spanning two
   repositories becomes two items.
5. **`retired` does not say why.** A card retired at project exit and a capture
   the user declined look alike.
6. **The routing risk moves.** Without `/kb-update`, a dictated correction must
   reach `/kb-capture`; sent to `/kb-redact` it would be a claim with no capture
   behind it. `/kb-redact` stops and hands back — one more sentence there.
7. **The reviews' reasoning survives only in git.** Anything not carried into
   `decisions.md` has to be re-derived if it comes up.

## 8. Not doing

- **Dropping agent blocks from notes** (`verification-gaps.md` §5 leaves it
  open). It would make everything in a note cardable, and agent diagrams
  unaffordable again — the problem the first review called load-bearing.
- **Merging `/kb-cards` into `/kb-redact`** (§3).
- **Dropping `importance`** — one key, written once, and per-deck limits and
  retention are settable nowhere else (`decisions.md` §3).
- **Dropping `type`** — `kb_export.py` dispatches on it and names decks from it.
- **Rebuilding a note from its whole pool by default** — `design-review-2.md`
  W7's reason stands: a rebuilt note has to be re-reviewed whole.

## 9. Sequence

One release, 0.17.0, because the format touches every file. Inside it:
`reference/schema.md` first (everything quotes it), then `kb_check.py` and
`kb_migrate.py`, then `kb-common`, then the skills, then the prose. Migrate the
base, then delete this file — its conclusions are in `decisions.md` by then,
which is the point of §5.

---

## Appendix: `reference/schema.md`, drafted

````markdown
# Knowledge base format

`scripts/kb_init.sh` copies this into the base as `SCHEMA.md`;
`scripts/kb_check.py` enforces the shape. Why it is this way is in
`decisions.md`. Where a file lives is not part of the format.

## Identity

An item that stays in the base is `<slug>_<n>`, where `<n>` is the lowest free
number in **the slug pool** — one subject's captures, its note, its verify
reports, whatever their kind. A card leaves the base and is 12
random base62 characters from `scripts/kb_randomid.sh`, never invented. The
filename ends in the ID, optionally after a prefix
(`2026-08-10_retry-wrapper_1.md`). Find items with `scripts/kb_find.py` — by
ID, by pool, or by what refers to them — never by guessing a path.

## Keys

```yaml
---
id: retry-wrapper_3
type: Note                  # Capture | Note | Recall Card
title: Retry wrapper ordering        # the subject, not a claim
authored: human                      # human | agent — whose claims these are
date: 2026-08-10                     # when the claims last changed
status: confirmed                    # draft | confirmed | retired
from: [kb:retry-wrapper_1, kb:retry-wrapper_2]
code: https://github.com/acme/backend@a1b2c3d
paths: [src/queue/retry.py]
---
```

- **`authored`** — whose claims, never who typed. A note the agent worded from
  the user's captures is `human`. **Nothing `authored: agent` is ever carded.**
- **`status`** — `draft` until checked against the source and kept by the user;
  `retired` once no longer true or not worth pursuing. Never delete. A claim
  that changes returns the item to `draft` until the user accepts it.
- **`from`** — what this was derived from: `kb:<id>`, or a URL for an external
  document. Derived items list what they came from first.
- **`code` / `paths`** — the evidence: one repository at one commit, paths
  relative to its root. Written when the claim is checked; `/kb-verify` reads
  them later. Evidence is recorded once, where it was read, never copied down
  the chain. Naming an item in prose is free; `from` is about derivation.

| Kind | `from` | |
|---|---|---|
| Capture | evidence only; the item it concerns when `authored: agent` | one session, one author; open while the session that wrote it runs, closed after |
| Note | its captures, then other notes | the current state of one subject; every sentence outside an agent block traces to a human capture |
| Card | the one item it is drawn from | never evidence directly; `importance: core \| extra`; the ID is permanent |

## Agent blocks

Inside an `authored: human` note, agent-written material is fenced:

<!-- agent -->
a diagram, a walkthrough — never history
<!-- /agent -->

Nothing inside is carded; the file stays `authored: human`; the agent redraws a
block freely. A delta report is not one — that is a verify report, an
`authored: agent` capture.
````
