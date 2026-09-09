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
| **Machine-graded free recall** — for *recall* cards; understanding cards are graded through `/kb-quiz` already | Adds friction where the habit is weakest, and recall review on a phone is most of what keeps it going | Self-graded review has been unbroken for a month, and the understanding-card grading has proved itself |
| **Knowledge authored by the agent** (answers worth keeping from asking the corpus questions) | Where it lives is unresolved, and whether it may ever become a card sits exactly on the articulation boundary | After the wiki layer settles |
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
