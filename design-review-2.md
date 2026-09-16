# Design review 2 — September 2026

Written after 0.13 was in use for a few days, from three inputs: the user's
second list of problems, `verification-gaps.md` (two observed failures where
agent material landed in the user's items), and a session settling the plan
below. Read `design-review.md` first; this document assumes it.

**Status: implemented in 0.14.0**, except two steps that act on a knowledge
base rather than on the tooling: running `scripts/kb_migrate.py` on each base,
and the repair of the two damaged items (§3, W8) on the machine where they
live.

## 1. Symptoms

| Reported | Cause |
|---|---|
| captures too strictly append-only; the writing session should be free to edit | A |
| an agent appended its own claims to a dictated capture (verification-gaps Case B) | A |
| a URL fixed across note and card, then "approval not stamped" | A |
| approval left standing over a substantially rewritten note (Case A) | A |
| a correction dictated while carding was written unverified | A |
| references go stale as items move between directories | A |
| verification rewrote the note it was checking (Case A) | B |
| re-verification should be about notes; captures are a record | B |
| cross-note operations are slow and hard to review | C |
| the quiz stopped asking a note's questions together | D |
| no automatic re-export after a card changes | D |
| frontmatter is exploding; the schema every skill loads is large | D |
| the quiz could ask about what changed since last time | follows from A |

## 2. Diagnosis

### A. There is no rule for how an item changes

When to edit and when to append, what an edit does to `approved` and
`generated.at`, who may write into whose file, what a reference points at — each
skill answered these locally, and differently. The failures in Case B and the
URL fix are the same gap seen from two ends: one edit changed claims and kept
approval, the other changed no claim and asked for it.

### B. Checking an existing item had no operation

"Verify this note against the code" routed to `/kb-update`, which is shaped
around a dictated claim; with none, it arrives at "fold into the note" and does.
Its "report, don't fix" came a step later than the fold. And the report had
nowhere to go but the item.

### C. Effort was allowed to mean scope

Thorough meant "sibling notes too", "cross-item cards". A run touching several
notes produces a diff nobody can review in one sitting, and doing the notes one
at a time gives the same result.

### D. Losses and weight

The quiz rewrite dropped a working rule; export was never chained; the note
layer copied its captures' evidence and verification history, and the schema
injected into five skills grew to 387 lines, most of it rationale.

## 3. The plan

### W1. Quick fixes

- `/kb-quiz` asks all of a note's questions together: one AskUserQuestion call
  in quick mode, one numbered list otherwise.
- Export runs automatically after a skill changes an approved card, and after
  `/kb-cards` writes new ones (which then wait for a grade in `/kb-export`).

### W2. How items change — `kb-common`, "Changing items"

- **A capture is open during the session that wrote it, and closed after — both
  origins.** Open: the agent adds to it and rewords it. Closed: anything later
  is a new capture, same slug, next free number. *Session*, not *day*: the agent
  can know whether it wrote a file in this conversation, and a same-day rule
  would let a session with no memory of the file edit it — which is Case B.
- **One author per capture.** The agent's claims go into a machine capture,
  never into the user's.
- **Three edit classes:**

  | Edit | `approved` | `generated.at` |
  |---|---|---|
  | scaffolding — URL, path, identifier, diagram, formatting | stays | stays |
  | rewording the user asked for | moves to now (asking is approving) | moves |
  | a claim change | only from a dictated claim, re-stamped on acceptance | moves |

  `kb_check.py` warns when `generated.at` is later than `approved.at`.
- **A dictated correction is verified on the spot**, whatever the running
  skill's effort: it is one claim. It stays `draft` only if it cannot be checked.
- **One item per run.** A note, its cards, a verify report — one at a time, each
  reviewed on its own. A note may still draw on several captures of its subject.
  Effort means depth, never breadth.
- **A note never narrates its history.** A delta report is a verify report, not
  a machine block.
- **No to-do lists in captures.** `## Open / follow-ups` is dropped. A machine
  capture holds the agent's material — a diagram, a walkthrough, a verify
  report — and nothing anyone is meant to cross off. What a run skipped is
  reported in the conversation, and that is the end of it: the design's answer
  to C2 was being allowed to stop, and a ledger is an obligation in another
  form. Existing sections stay as history and are not read.

### W3. `/kb-verify` — read-only, notes only

Input a note; captures are never re-verified, since they record what was checked
then. It follows the note to its captures' evidence, runs `git log
<commit>..HEAD -- <paths>` first so an untouched path costs nothing, and reads
what changed. Output is a new machine capture in the note's slug pool with two
sections: **Scaffolding that moved** and **Claims affected** (the claim as it
stands, what the code shows, no replacement wording). Nothing changed ⇒ it says
so and writes nothing. It never edits the note; `/kb-update` then applies the
scaffolding with approval untouched, and an affected claim waits for the user to
dictate the correction. No `Edit` in its tools — a nudge, not a guarantee, since
it needs `Write`.

`/kb-update` with no dictated claim hands off to `/kb-verify`; "report, don't
fix" is its own step before anything is written.

### W4. References by ID

`resource: kb:<id>` replaces a base-relative path. Filenames contain the ID, so
resolution is a glob and survives any move. `scripts/kb_find.py` resolves an ID,
lists a slug pool, and lists what refers to an item (a note's cards and quiz
logs). `kb_check.py` errors on an unresolved reference and a duplicate ID;
`kb_export.py` and `kb_anki.py` resolve both forms during migration.

### W5. Less frontmatter

- **Items.** `verified` is a single `{ by, at }` — the latest check; a verify
  report carries history. A note carries no evidence or verification copied from
  its captures. Evidence is what the claims turn on, grouped under one entry per
  repository. `kb_check.py` warns on frontmatter over 20 lines.
- **Schema.** `reference/frontmatter.md` is split into `reference/schema/`:
  `core.md` plus one file per kind. Each skill loads core and the kinds it
  writes; rationale moves to `decisions.md`. `kb_init.sh` joins them into the
  base's `SCHEMA.md`.
- **Migration.** `scripts/kb_migrate.py`, dry-run by default: path references
  to IDs, `verified` lists to one entry (a `human:` entry becomes `approved`),
  evidence a note duplicates from its captures dropped.

### W6. Quiz on what changed

A note's changes are the human captures in its slug pool newer than its last
quiz log. `/kb-quiz` gathers them and leads with them; "what changed" is a topic
of its own.

### W7. Updating a note — an experiment

`verification-gaps.md` R5 proposed rebuilding a note from its captures on every
update. Adopted in part: the invariant holds everywhere (every sentence outside a
machine block traces to a human capture), but the default operation edits the
affected sections, and a rebuild from the slug pool is thorough effort. A
rebuilt note means re-reviewing all of it, which is the cost C was about.
**Revisit** if edited notes start reading as patched.

### W8. Repairs (on the work machine)

Case A's note: delta block to a machine capture; prose that does not trace to a
capture removed; renames kept; approval cleared or re-stamped. Case B's capture:
the `## Update` section cut; `generated` restored; the dictated sentence as a
new human capture; the agent's claims into a machine capture. Run the check.

## 4. Decided against

- **Machine captures as to-do lists, carried forward session to session** — a
  capture is a record, not a worklist (W2).
- **Same-day instead of same-session editing** (W2).
- **Rebuilding a note on every update** as the default (W7).
- **Merging `/kb-update` into `/kb-redact`** — with W2 and W3 `/kb-update` has a
  clear job: dictated claim → new capture → affected sections → cards → export.
- **Dropping machine blocks from notes** — nothing observed calls for it; Case
  A's fault was narration, which W2 forbids.
- **Clearing approval on any body change** — the URL fix shows the cost (W2).
