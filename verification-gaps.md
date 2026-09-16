# Agent material keeps landing in the user's items — findings and remedies


A follow-up to `design-review.md`, from two observed failures in 0.13.1. Read
`design-review.md` §C1 and §2.1 (companion items, machine blocks) first; this
document assumes them.


**Status: proposed, nothing implemented.** Written 2026-09-16 to be carried to
another machine and implemented there. All knowledge-base content in the
examples is generalised — placeholders stand for the real subjects — while
skill, file and key names are the tooling's own and are literal.


Both incidents are the same fault: **an agent produced material about an
existing item and had nowhere to put it except inside that item.** They differ
only in which layer absorbed it.


## 1. What happened


### 1.1 Case A — verification rewrote the note it was checking


The user asked an agent to **verify an existing note against the current
code**. The note was `origin: human`, `status: stable`, derived from one
dictated capture, carrying a `verified` list whose last entry was
`human:<user>` — which `reference/frontmatter.md` reads as approval for items
written before the `verified`/`approved` split.


The subject had moved: a protocol field had been renamed throughout, and one
read path re-plumbed so a value previously fetched on demand was now pushed and
stored, the old fetch demoted to a repair path.


The agent found all of that correctly, then in one pass, unprompted:


1. Renamed the field throughout the user's prose, including the title, and
   added new paths, symbols and `commit` to `sources`.
2. Rewrote a five-step walkthrough to match the new read path, and added a
   bullet about two adjacent request types.
3. Appended a machine block narrating the rename and the read-path change.
4. Added its own `verified` entry and moved `generated.at`.


Only (1) was legitimate — `kb-common` ("Claims and scaffolding") lets the agent
supply identifiers, paths and call order.


What was wrong:


- **Machine claims in unfenced human prose.** The rewritten walkthrough and the
  new bullet contained statements of purpose and consequence — what a mechanism
  is *for*, why a value is never observable in one case. Nothing in the
  dictated capture said them.
- **The note both rewrote and narrated.** `/kb-update` step 5 says a note
  "never narrates its history", yet the body was brought to current state *and*
  given a delta block describing the change — duplicating raw-layer work in the
  layer the user reads for understanding.
- **Approval went stale silently.** The body changed substantially; the human
  `verified` entry, which reads as approval, was neither re-dated nor cleared.
  Nothing in any skill checks this.


### 1.2 Case B — a mixed-authorship append to a human capture


A different session, asked to check three related notes for cross-influence.
It got the hard parts right: it deprecated the note the change had overtaken,
opened a new note under a new slug, and wrote a proper `origin: machine`
capture whose `## Open / follow-ups` was accurate and useful.


Then it appended an update to the **human** capture. The user had dictated one
sentence:


> A recent change in the code enabled `<mechanism>`, which is the target
> authentication mechanism.


What landed under the user's byline was three claims:


> The recent `<mechanism>` work in `<component>` turned the target mechanism
> into the real one, **so the `<old approach>` is no longer what `<environment>`
> runs on. The `<artifact>` survives as a local override, not as the
> mechanism.**


The bold sentences are the agent's, and are not rewordings of anything the user
said: one is a consequence claim, the other concerns an artifact the user never
mentioned. Both are correct. Both are exactly the "causation, consequence, why"
that `kb-common` reserves to the user, always — and they are the sentences a
card would be drawn from.


The frontmatter then asserted `generated: { by: human:<user>, at: <now> }` over
text the agent had partly composed.


Note what this is **not**: it is not the polishing case. A note polished by the
agent from the user's claims is `origin: human` and correct by the schema's own
definition. Here the agent added claims of its own. No labelling scheme makes
that acceptable; the material belonged in the machine capture, which existed
and was open at the time.


## 2. Why


### 2.1 The requested operation does not exist (Case A)


"Verify this item against the current code" is revalidation, deferred in full
(`deferred.md`, first row). With no skill for it, the agent routed to the
nearest one, `/kb-update`.


`/kb-update` is shaped entirely around **a user-dictated claim as its input**:
step 2 splits claim from instruction, step 4 records the claim in the capture.
Given no dictation, steps 2 and 4 are no-ops and the agent arrives at step 5,
"fold it into the note". The observed behaviour is what that skill does when
its input is absent. **The interaction model is the primary fault, not the
prose.**


### 2.2 The prohibition is placed after the permission


The rule that should have stopped Case A — *"A code change that falsifies a
claim is reported, not fixed"* — is a clause in `/kb-update` **step 6**, after
step 5 has already said to fold. `kb-common`'s "Report, don't fix silently"
sits under Verification, away from the numbered flow. An agent reading
top-down folds first and reports afterwards, which is the order observed.


### 2.3 "Report" has no durable surface — C1 at an unenumerated stage


Report to whom, into what? Conversation evaporates, and `design-review.md` §C5
is explicit that redaction assumes no shared session context, so anything that
matters has to be in a file. At verification time the only writable surface in
reach is the item itself, so findings go into the item.


That is C1 recurring — agent material with nowhere to go ends up in the user's
prose — at a stage §2.1 did not enumerate, because §2.1 gave agent material a
home when produced *during capture* and never when produced *about an existing
item*.


### 2.4 The capture layer is modelled as documents, but behaves as a log


Case B's defect is not in `origin`. `frontmatter.md` is explicit that `origin`
is *whose claims* and `generated.by` is *who produced the text*; the key that
went false was `generated.by`. The deeper problem is that
`generated: { by, at }` is a **single-event key on a file the design already
declares append-only**. One byline cannot describe a file written by two
authors on two dates, so the agent bumped the timestamp and nobody noticed the
byline had stopped being true. `verified` has the same problem in reverse: a
flat file-level list cannot say which entry checked which appended section.


**`/kb-update` already states the right principle and then contradicts it.**
Its preamble reads *"the raw layer is the log, the note is the current state"*
— and its step 4 appends to a capture, which edits the log, while its step 5
folds into the note without rebuilding it. The rules below mostly consist of
making the skills obey a sentence one of them already opens with.


## 3. Rules to state directly in the skills


These are the load-bearing part of this document. They belong in `kb-common`
as rules, not as prose scattered through the numbered steps, and several are
mechanically checkable.


**R1. The raw layer is the log; the note is the current state.** Already in
`/kb-update`'s preamble. Everything below follows from taking it literally.


**R2. A capture is never appended to and never edited after the session that
wrote it.** A later statement about the same subject is a **new capture**. The
existing in-session rule is unchanged: a misheard identifier or a claim the
user rewords a moment later is fixed in place, because that is still one event.


**R3. Every capture has exactly one author.** `generated.by` is whoever stated
the claims, and it is true by construction. Mixed authorship is not a labelling
problem to be solved with finer-grained metadata — it is an item that should
have been two.


**R4. The agent's own claims never enter a human capture** — not as prose, not
fenced, not "clearly attributed". They are a machine capture. Scaffolding
(identifiers, paths, call order) remains the agent's to supply in place, as
today.


**R5. A note is reconstructed from its captures, not edited toward the current
state.** Every sentence outside a fence must trace to a capture that has a
human author. This replaces "fold the update into the note".


**R6. Verification writes a report; it does not write to the item it
verified.** Not the body, not `sources`, not `verified`, not `generated.at`.


## 4. Remedies


### 4.1 Captures are only ever created, never appended to


The change that makes R2–R4 structural rather than aspirational.


- A correction, extension or agent finding about an existing subject is a new
  capture with the **same slug, next free number**: `<slug>_1` (user, Aug),
  `<slug>_5` (user, Sep), `<slug>_6` (agent, Sep).
- **The slug pool is the linkage; `sources` is not touched.** This matters
  because `frontmatter.md` forbids a human capture from citing another capture
  ("evidence only — never another capture"). Nothing in that rule needs to
  change: items sharing a slug are already one number pool and are found by
  globbing it. A machine capture may still cite the capture it accompanies, as
  today.
- **A superseded capture is not deprecated.** The log records what was believed
  then; the note carries the current state (R1). Leave it alone.
- `generated: { by, at }` becomes honest with no schema change, and each
  capture's `verified` unambiguously covers that capture.


What this buys over labelling: the agent **cannot** put its sentence in the
user's file, because the operation does not exist. Same mechanical-guarantee
argument as §4.2 below, and stronger than any prose rule.


**Superseded by this:** an earlier draft of this document proposed allowing
machine blocks inside captures to mark mixed appends. Do not implement that —
it patched the mixed file; this removes it.


### 4.2 A read-only verification skill, terminating in a capture


Add `/kb-verify` (name negotiable). Contract:


- Input: an existing item, plus effort.
- It checks the item's claims against the evidence in its `sources`, resolved
  at current HEAD rather than the recorded `commit`.
- **Output is a machine-origin `Capture`** — same slug, next free number,
  first source the item verified, then the evidence read, with `commit`.
  `frontmatter.md` already names "a delta report" as belonging there; no schema
  change is needed.
- Findings split under two headings: **scaffolding that moved** (renames,
  paths, call order — foldable without ceremony) and **claims affected** (the
  claim as it stands, what the code shows, and no proposed replacement wording,
  per `kb-common`, "Don't give the answer away").
- **It never edits the verified item** (R6).


Make this a **separate skill, not a mode of `/kb-update`**, for one mechanical
reason: a separate skill declares its own `allowed-tools` and can omit `Edit`
on knowledge-base items entirely. That turns "must not fold" from an
instruction an agent can reorder into something it cannot do. A mode inside
`/kb-update` inherits both `Edit` and the fold step sitting three lines above.


This pulls forward only the affordable half of deferred revalidation — the
**manual, single-item entry point**, not the change- or time-triggered sweeps
and not `stale_after`. `deferred.md` names the revisit condition as "a claim is
first found to have quietly stopped being true", which has now happened twice.


### 4.3 Changes to `/kb-update`


- **Step 1 precondition:** no user-dictated claim ⇒ this is not an update.
  Route to `/kb-verify` and stop.
- **Step 4 becomes "write a new capture"**, not "append to the existing one"
  (R2). The in-session edit case stays.
- **Move "report, don't fix" ahead of the fold step**, as its own numbered
  step, stated as a precondition on writing anything rather than as a remark
  about machine blocks.
- **State the scaffolding/claim split for code-driven deltas**, which currently
  appears only for user-dictated ones: scaffolding folds silently; a falsified
  claim stops and waits for a dictated sentence, which becomes a new capture
  and only then reaches the note.
- **Approval hygiene:** when a note's body changes, `approved` is re-stamped at
  the user's say-so or cleared — never left standing over text the user has not
  read. Consider enforcing the weak half in `scripts/kb_check.py`: warn where
  `generated.at` is later than `approved.at`.


### 4.4 Notes are reconstructed, not patched


Under R5, bringing a note up to date means **rebuilding it from the full set of
captures sharing its slug**, not editing the existing prose toward the new
state.


**This reverses an earlier draft's recommendation**, which argued against
re-deriving on the grounds that it risks drifting from the user's wording. That
objection loses its force once captures are a complete, append-only, singly
authored log: the note becomes a projection of the captures, reconstruction is
the normal operation rather than a risky one, and drift is now *checkable* —
every sentence must trace to a capture with a human author.


Consequences to handle during implementation:


- `/kb-update`'s note half largely collapses into `/kb-redact`, which already
  builds a note from captures. See §5 for whether the two should merge.
- The redactor now reads several captures where it read one. That is already
  true for human/machine pairs, and is the thorough row of the `kb-common`
  effort table; the effort table needs its rows restated for the new default.
- Reconstruction must preserve `approved` semantics — a rebuilt note is
  unapproved until the user says otherwise.


### 4.5 Repairing the two damaged items


Separate from the tooling change, done wherever the affected base lives.


Case A's note: move the delta block into a new machine-origin capture; remove
from the prose every statement of purpose or consequence that does not trace to
a capture; keep the renames, paths and call order; clear or re-stamp approval.


Case B's capture: cut the `## Update — <date>` section out of the human
capture; restore its `generated` to the original author and timestamp; write
the user's one dictated sentence as a new human capture under the same slug;
write the agent's two consequence claims into the machine capture that already
exists, or a new one.


Run `scripts/kb_check.py` over everything touched.


## 5. Open decisions — do not pre-resolve these


**Should machine blocks stay in notes?** Genuinely undecided.


- *Keep them.* §2.1 called marked regions load-bearing: without them a note can
  hold no agent material at all, and agent diagrams go back to being
  unaffordable, which is C1.
- *Drop them.* Under R5 every note sentence traces to a capture, so machine
  material in a note is just a projection of a machine capture and the fence
  duplicates what the source chain already says. Carding gets simpler:
  everything in a note is cardable, because everything in it is the user's.
- *Middle option, worth costing.* The fence stays but is only ever a
  **rendering** of a machine capture's content — regenerated on reconstruction,
  never authored in place. The fence then marks provenance rather than
  authorship, and R5 holds without losing diagrams.


**Should the `## Open / follow-ups` ledger remain a capture?** It is a
worklist, not knowledge: never mined by `/kb-redact`, never quizzed, and the
one thing in the base meant to be re-read and crossed off. §4.1 sharpens the
question, because if nothing is ever appended, a never-append rule yields one
fresh ledger per session per subject.


Argue it rather than assume it: `design-review.md` §2.3 already tried pulling
follow-ups out and dropped it, because a global `<kb>/open.md` "reinvented the
stray `inbox/inbox.md` of C2, with no format behind it". A per-subject typed
item with a slug and a format is not the same thing, but it is close enough to
deserve the argument.


**Should `/kb-update` and `/kb-redact` merge?** §4.4 leaves `/kb-update`
owning little beyond recording a new capture and carrying changes to cards. If
the note half is reconstruction, "update" may be `/kb-capture` followed by
`/kb-redact`, with only the card-carrying step unaccounted for.


## 6. What this does not change


- **No new item kind for agent captures.** `decisions.md` §6 holds: `origin`
  already gates carding everywhere, so a second type would be a duplicate
  switch to keep in step. The ledger in §5 is the one place this is reopened,
  and for a different reason.
- **No schema change is required** by §4.1–§4.3. `origin: machine` captures,
  the slug pool, and the `verified`/`approved` split already do what is needed.
- **Revalidation stays deferred as a sweep.** Only the manual single-item entry
  point is pulled forward.
