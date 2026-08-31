# Personal learning system — deferred

Capabilities the design accepts and does not yet build. Each records why, and
what should trigger revisiting it.

| Deferred | Why not now | Revisit when |
|---|---|---|
| **Revalidation** — material verified at capture rechecked as its subject changes: the change- and time-triggered passes, `stale_after`, `reviewed`, and `status: deprecated` on confirmation | Nothing captured is old enough to have gone stale, and correctness *at* capture is the harder half. Until it exists, the staleness obligation rests on remembering to look, which is exactly what does not work | The oldest verified item is a few months old, or a claim is first found to have quietly stopped being true |
| **Relating an item to what is already known** (the overlap check, the `related:` graph) | `/kb-capture` now glances at the existing items so a restatement becomes an update rather than a second capture, which covers the case that hurts; the general check needs a corpus large enough for a new note to plausibly duplicate an old one, and needs the index below to be affordable | A capture turns out to restate an existing note and nothing catches it |
| **The generated index** | Its only consumer is the overlap check; cataloguing a corpus you can still read in one sitting earns nothing | Overlap detection is built, or reading the corpus whole stops being feasible |
| **Restructuring the corpus** — a whole-corpus findings pass, and a log with it | A pass over a corpus this small finds nothing, and its shape is unknown until revalidation has run by hand a few times. Scheduling either pass automatically comes after that | Revalidation exists and has been run manually a few times |
| **Synthesis / wiki layer** | Needs volume to say anything; regeneration is unsolved | Overlap between notes becomes a felt problem |
| **Cards derived from the wiki** | Not forbidden — the wiki reorganises claims the user already articulated. Blocked on telling reorganisation from genuine synthesis, and on overlapping cards already drawn from the same notes. Free-recall cards especially may belong here, since causation, ordering and tradeoff emerge *across* notes rather than within one | The wiki exists, and note-derived cards are numerous enough to test the overlap against |
| **Machine-graded free recall** | Adds friction where the habit is weakest | Self-graded review has been unbroken for a month |
| **Knowledge authored by the agent** (answers worth keeping from asking the corpus questions) | Where it lives is unresolved, and whether it may ever become a card sits exactly on the articulation boundary | After the wiki layer settles |
| **Deletion reconciliation with the scheduler** | Nothing has been retired yet | The first card is retired |
| **Reasoning cards** — a card that asks for an explanation and is graded against a 3–6 bullet self-grading rubric | Writing a rubric a person can grade themselves against is the hard half, and it is unclear which notes deserve one. The kind is deferred whole rather than shipped as a placeholder: a card reaching review as a bare "explain this" has nothing to grade against, and nothing downstream can compensate — the scheduler does not grade, it consumes a grade the human produces, so there is no correctness checking to hook into anywhere in the pipeline. `/kb-quiz` covers some of the same ground conversationally, and needs no rubric written down to do it | Recall cards have been in review long enough to show what they fail to test |
| **Card kinds beyond recall** | One kind has not yet failed to fit anything, and `type` is open, so a second costs no format change | Something demonstrably doesn't fit |

Deferring these costs nothing structurally, with one exception worth naming:
revalidation cannot be retrofitted onto material that did not record what it was
checked against. That is why `commit` and `retrieved` are written at capture
now, although nothing reads them yet.

## Notes for future work

Guidance for the deferred pieces, so it need not be re-derived.

### Revalidation

The mechanism was worked out before it was deferred. Two triggers, and the
frontmatter for both is already being written.

- **Change-triggered.** `git log <commit>..HEAD -- <path>` in the repo the
  item's `resource` URL names. Empty result ⇒ still current, at no cost. This is
  what makes a sweep affordable: most items are untouched, so most of a pass is
  a cheap negative. Only entries carrying `commit` participate. **Resolving that
  URL to a checkout on this machine is the unbuilt half** — an item deliberately
  records no local path (`reference/frontmatter.md`), so the pass needs some
  way to be told where the repo is. Decide it with the pass; anything decided
  now would be a convention kept ready rather than a mechanism.
- **Time-triggered.** `stale_after: <YYYY-MM-DD>` on the item, measured against
  `reviewed`. An absolute date rather than a relative TTL, so staleness is a
  plain date comparison (OKF §5.5). Both keys arrive with this work.

**A hit does not mean "wrong" — it means "recheck."** The pass re-reads only the
flagged items, reports, and on confirmation sets `status: deprecated` and
suspends the card in the scheduler. Never deletes.

**Staleness reaches a card through its notes.** Do not add `commit` or a check
date to a card when building this: it would create a second copy of the same
fact, free to drift out of step with the first. A card's `sources` stay notes
only.

### The scheduler integration

Suspension of deprecated cards, deletion reconciliation, and machine-graded
free recall are all the same integration. Build it once, when the first of them
is actually needed.

- **Report, do not delete.** A card missing from the markdown is reported, never
  removed — a parser bug must not be able to reach review history.
- **Grade strictly** if grading is built. Require each rubric bullet to appear
  explicitly and fail the card when one is missing. Lenient grading reproduces
  exactly the weakness that self-grading already has, at greater cost.

## Appendix: scheduler setup

Review is out of scope, but four configuration facts are load-bearing for
decisions made *here*, and have nowhere else to live. They are the kind that get
lost and then quietly stop working.

**Separate presets per deck — mandatory, not cosmetic**, once there is more
than one deck. Daily limits are a property of the preset, not the deck, so two
kinds sharing one preset makes the split between them unenforceable. Review load
is controlled by per-deck new-card limits, and that mechanism does not exist
without separate presets.

**FSRS is global; its parameters are not.** The enable toggle applies to the
whole collection and cannot differ per preset. Parameters and desired retention
*are* per-preset, which is the real reason presets matter — forgetting curves
belong to the material, and each preset optimises from its own history. Leave
desired retention at its default, and do not run optimisation until several
hundred reviews exist; defaults are good until then. Learning and relearning
steps must stay shorter than one day.

**Press Again on failure, never Hard.** Hard means "recalled, with effort."
Using it for a failure inflates every subsequent interval, and the temptation
will peak on reasoning cards, where producing three of five rubric points feels
like partial success. It is a failure — grade it Again. This single habit
degrades scheduling silently and irreversibly if it slips.

**Review reasoning before recall when both are due.** Overlapping cards prime
each other, and priming flows forward; spending it on the frequently-repeated
recall cards, where a mis-grade self-corrects, is much cheaper than spending it
on sparse reasoning cards where each grade carries real weight. Clicking a
parent deck does **not** guarantee this — the scheduler gathers across subdecks
by card state, not by subdeck order. Open the reasoning deck directly, finish
it, then the recall one.

**Two things never done in the scheduler's own interface:** renaming decks or
note types, and editing card text. Both break the stable-identity contract the
export depends on — renames do not round-trip, and edited text is overwritten
on the next import. Edit the markdown and re-export instead.
