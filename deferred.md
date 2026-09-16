# Personal learning system — deferred

Capabilities the design accepts and does not yet build. Each records why, and
what should trigger revisiting it.

| Deferred | Why not now | Revisit when |
|---|---|---|
| **Revalidation as a sweep** — the change- and time-triggered passes over the whole base, `stale_after`, `reviewed`. The manual single-note check exists: `/kb-verify` | A sweep is `/kb-verify` run over every note, and its shape is worth deciding only once the manual check has been used a few times; until then staleness rests on remembering to look | `/kb-verify` has been run by hand a few times, or the oldest verified note is a few months old |
| **Relating an item to what is already known** (the overlap check, the `related:` graph) | `/kb-capture` now glances at the existing items so a restatement becomes an update rather than a second capture, which covers the case that hurts; the general check needs a corpus large enough for a new note to plausibly duplicate an old one, and needs the index below to be affordable | A capture turns out to restate an existing note and nothing catches it |
| **The generated index** | Its only consumer is the overlap check; cataloguing a corpus you can still read in one sitting earns nothing | Overlap detection is built, or reading the corpus whole stops being feasible |
| **Restructuring the corpus** — a whole-corpus findings pass, and a log with it | A pass over a corpus this small finds nothing, and its shape is unknown until revalidation has run by hand a few times. Scheduling either pass automatically comes after that | Revalidation exists and has been run manually a few times |
| **Synthesis / wiki layer** | Reorganising the user's own claims across notes is what the note layer now allows (a note may draw on several captures and notes). Genuine synthesis is machine material at corpus scale — same fence, same rules — and needs volume to say anything | Overlap between notes becomes a felt problem |
| **Cards derived from the wiki** | Not forbidden — the wiki reorganises claims the user already articulated. Blocked on telling reorganisation from genuine synthesis, and on overlapping cards already drawn from the same notes. Free-recall cards especially may belong here, since causation, ordering and tradeoff emerge *across* notes rather than within one | The wiki exists, and note-derived cards are numerous enough to test the overlap against |
| **Machine-graded free recall** — for *recall* cards; understanding cards are graded through `/kb-quiz` already | Adds friction where the habit is weakest, and recall review on a phone is most of what keeps it going | Self-graded review has been unbroken for a month, and the understanding-card grading has proved itself |
| **A `visibility` key, and a mechanical sanitisation check** | Only a general pattern is meant to leave for another knowledge base, and it is written to travel from the start (`kb-common`), so there is nothing else to label and nothing a second check would catch that writing it did not | Something other than a harvested pattern needs to leave, or a pattern is found to have carried a project identifier out |
| **Checklists offered by the agent** — naming the shape of a task ("threads one field end to end") and offering its closed questions, as a stopping rule for tracing | Working-session behaviour, not knowledge-base design; needs no mechanism | The open items a skill records turn out to be mostly unanswered checklist questions |
| **A drill skill** — predict-then-run, break-and-read, specify-then-diff, with a log across sessions | Any session with an agent can run these on request, and a wrong prediction is just a capture. A skill earns its place only if history across sessions turns out to matter | The user is running these regularly and wants the record |
| **Knowledge authored by the agent** (answers worth keeping from asking the corpus questions) | Now has a place — a machine-origin capture, or a machine block in the note it concerns — and may never become a card. The open half is only whether such answers accumulate enough to need cataloguing | After the wiki layer settles |
| **Deletion reconciliation with the scheduler** | Nothing has been retired yet | The first card is retired |

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
  records no local path (`reference/schema/core.md`), so the pass needs some
  way to be told where the repo is. Decide it with the pass; anything decided
  now would be a convention kept ready rather than a mechanism.
- **Time-triggered.** `stale_after: <YYYY-MM-DD>` on the item, measured against
  `reviewed`. An absolute date rather than a relative TTL, so staleness is a
  plain date comparison (OKF §5.5). Both keys arrive with this work.

**A hit does not mean "wrong" — it means "recheck."** The pass re-reads only the
flagged items, reports, and on confirmation sets `status: deprecated` and
suspends the card in the scheduler. Never deletes.

**Retirement is the cheaper sibling**, and needs no change detection: at
project exit, the cards whose chain ends in that repository are suspended in
the scheduler and their items marked `deprecated` or left as reference. The
chain is what identifies them — no item needs a key saying which lane it is
in. Revalidation is then only for what outlives the project, a far smaller
set.

**Staleness reaches a card through its notes.** Do not add `commit` or a check
date to a card when building this: it would create a second copy of the same
fact, free to drift out of step with the first. A card's `sources` stay notes
only.

### The scheduler integration

**It now exists** — `scripts/kb_anki.py`, built for understanding cards, which
needed a grade to travel from a conversation to the scheduler. Suspension of
deprecated cards, deletion reconciliation and machine-graded free recall are
the same integration and now hang off it rather than waiting for one.

- **Report, do not delete.** A card missing from the markdown is reported, never
  removed — a parser bug must not be able to reach review history.
- **The grade is proposed, never sent unasked.** What `/kb-quiz` does for
  understanding cards is the pattern: the agent says what was right and wrong
  and recommends a button; the user presses it. That is what makes lenient
  grading harmless — nobody is grading themselves against their own memory of
  what they meant.

## Appendix: scheduler setup

**Moved to [`reference/anki-setup.md`](reference/anki-setup.md).** It stopped
being a note about deferred work the moment `/kb-quiz` began driving the
scheduler, and it is now the setup a working system depends on.
