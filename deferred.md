# Personal learning system — deferred

Capabilities the design accepts and does not yet build. Each records why, and
what should trigger revisiting it.

| Deferred | Why not now | Revisit when |
|---|---|---|
| **Revalidation as a sweep** — change- and time-triggered passes over the whole base, `stale_after` | A sweep is `/kb-verify` over every note, and its shape is worth deciding only once the manual check has been used a few times | `/kb-verify` has been run by hand a few times, or the oldest confirmed note is months old |
| **Relating an item to what is already known** — the overlap check, a `related:` graph | `/kb-capture` glances at the base, which covers the case that hurts; the general check needs a corpus large enough for a new note to plausibly duplicate an old one | A capture turns out to restate an existing note and nothing catches it |
| **A generated index** | Its only consumer is the overlap check, and cataloguing a corpus you can read in one sitting earns nothing | Overlap detection is built, or reading the corpus whole stops being feasible |
| **Restructuring the corpus** — a whole-corpus findings pass | A pass over a corpus this small finds nothing, and its shape is unknown until revalidation has run by hand | Revalidation exists and has been run manually a few times |
| **Synthesis / wiki layer** | Reorganising the user's claims across notes is what the note layer already allows; genuine synthesis is agent material at corpus scale — same fence, same rules — and needs volume to say anything | Overlap between notes becomes a felt problem |
| **Cards derived from the wiki** | Blocked on telling reorganisation from genuine synthesis, and on overlap with cards already drawn from the same notes | The wiki exists and note-derived cards are numerous enough to test against |
| **A card for understanding a whole note**, the kind removed in 0.16 | Reasoning through a whole note costs far more to review than a recall card and did not return it, so the cards went unreviewed; the quiz that graded them had already gone in 0.15 | The rest of the pipeline has settled, and a design makes the review worth its cost |
| **Machine-graded free recall** | Adds friction where the habit is weakest, and phone review is most of what keeps it going. The first attempt, `/kb-quiz`, was removed in 0.15 | Self-graded review has been unbroken for a month, and a design addresses why the quiz fell short |
| **A `visibility` key and a sanitisation check** | Only a general pattern leaves for another base, and it is written to travel from the start | Something else needs to leave, or a pattern is found to have carried a project identifier out |
| **Checklists offered by the agent** — naming a task's shape and its closed questions, as a stopping rule | Working-session behaviour, not knowledge-base design; needs no mechanism | The open items a run reports turn out to be mostly unanswered checklist questions |
| **A drill skill** — predict-then-run, break-and-read, specify-then-diff | Any session with an agent can run these on request, and a wrong prediction is just a capture | The user runs these regularly and wants the record across sessions |
| **Knowledge authored by the agent** at scale | It has a place already — an `authored: agent` capture, or an agent block — and may never become a card; the open half is only whether it accumulates enough to need cataloguing | After the wiki layer settles |
| **Deletion reconciliation with the scheduler** | Nothing has been retired yet | The first card is retired |

Deferring these costs nothing structurally, with one exception: **revalidation
cannot be retrofitted onto material that did not record what it was checked
against.** That is why `code` and `paths` are written at capture now, although
only `/kb-verify` reads them.

## Notes for future work

Two things worked out before they were deferred, so they need not be
re-derived:

- **Change detection is a cheap negative.** `git log <commit>..HEAD -- <paths>`
  in the repository the item's `code` names; an empty result means still
  current, at no cost, which is what would make a sweep over the whole base
  affordable. **Resolving that URL to a checkout on this machine is the unbuilt
  half** — an item deliberately records no local path, so the pass needs some
  way to be told where the repository is. Decide it with the pass.
- **Staleness reaches a card through its note.** Do not add `code` or a check
  date to a card when building this: it would be a second copy of the same
  fact, free to drift. A card's `from` stays the item it was drawn from.

A hit means *recheck*, never *wrong*: the pass re-reads only the flagged items,
reports, and on confirmation marks them `retired` and suspends their cards.
**Retirement is the cheaper sibling** and needs no change detection at all — at
project exit, the cards whose chain ends in that repository are suspended and
their items retired. The chain identifies them, so no item needs a key saying
which lane it is in.

The scheduler setup a working system depends on is
[`reference/anki-setup.md`](reference/anki-setup.md).
