# Personal learning system — decisions

Choices made about things outside this system, recorded so they are not
re-litigated. Nothing here is an instruction, and editing a skill never obliges
a change to this file — that is the point of keeping it separate.

## 1. Review is Anki's, not ours

The system owns everything from the spoken sentence to the moment a card is
handed to the scheduler. It does not own scheduling and does not implement a
review interface. Noticing when what it holds has stopped being true stays
inside the boundary.

**Understanding cards once crossed it**: `/kb-quiz` questioned the user on a
note and sent the grade through AnkiConnect, on the grounds that a self-graded
"did I understand that?" is the unreliable judgement. The quiz was removed in
0.15 — it did not work well in practice. Understanding cards are now reviewed
and self-graded in Anki like recall ones, and the line holds without
exception; `scripts/kb_anki.py` keeps only status, backup and sync.

## 2. Why the card ID goes in Anki's `guid` column

Anki matches an imported row to an existing note on the first field, or on the
`guid` column when the file supplies one. **Matching on the first field makes
the question text the identity**, so fixing a typo in a question orphans its
review history and adds a second card. That alone is disqualifying — permanent
card IDs exist to make rewording free.

Anki's manual nonetheless recommends against the alternative: *"If you are
creating your own IDs, such as `MYNOTE0001`, then it's recommended that you
place the IDs in the first field, instead of assigning them to Anki's internal
GUID."* It does not say why. Three reasons are visible in what a guid is, each
answered by something this system already does:

- **The namespace is global** — a guid is unique across every collection in the
  world, which is what makes updating a shared deck work, and a collision is
  silent: *"if a GUID is provided, and already exists in the collection, a
  duplicate will not be created."* But that hazard belongs to the IDs, not the
  column, as the manual's own `MYNOTE0001` shows. The random tail in a card ID
  answers it.
- **A guid is invisible from inside Anki** — not shown, not searchable, not
  editable — so nothing can be repaired on that side. Accepted: this deck is
  generated, an edit made in Anki does not survive the next import, and the fix
  for anything wrong is a corrected card and a re-import.
- **It disables the import dialog's duplicate handling** for rows carrying a
  guid. Nothing here wants it — a duplicate ID is already fatal at export.

The remaining alternative, an ID in the first field of a custom notetype, costs
a notetype — and **a text import cannot create one**. It would have to be built
by hand in Anki, on every machine, before the first import worked anywhere. The
export targets stock `Basic` instead.

## 3. The export is a tab-separated text file

One importable package, one deck per card kind, split again by `importance` —
`Knowledge::Recall::Core` and `::Extra` — because daily limits and desired
retention are settable per deck and nowhere else. The card ID goes in the `guid`
column and that is the whole of what stable identity needs; a binary package
would add a dependency to carry the same fact.

The split is uniform across kinds although only recall needs it today: a text
import creates decks lazily, so a kind that never grades a card `extra` never
creates that deck, and the day one does, nothing has to be restructured. Making
the deck path depend on the data instead is how a collection gets split in two.

Deck names belong to the identity contract as much as card IDs do: the
scheduler keys review history off them, so a rename means renaming in both
places, and renaming a *kind* moves its cards to a new deck.

## 4. The export renders HTML, not markdown

Card bodies are markdown, but Anki renders markdown not at all: under
`#html:false` a `**zipapp**` reaches review with its asterisks showing, and a
blank line between an answer and its example collapses to nothing. Both are
things the cards rely on — the length rule asks that an explanation be
*visually separate* from the answer, which needs a real block element to be
true of the rendered card.

So `kb_export.py` renders the markdown subset the cards use — paragraphs,
bullet and ordered lists, fenced and inline code, bold and italic — and sets
`#html:true`. It is deliberately a small hand-written renderer rather than a
markdown library: the export is a gate, and a second dependency to format five
constructs is not worth what it costs to install. Anything outside the subset
is HTML-escaped and passed through, so an unsupported construct degrades to
its literal text rather than to broken markup.

**The renderer is provisional in a way the `#html:true` above it is not.**
Rendering at all is forced by what Anki does with a field; hand-writing the
renderer is a cost judgement, and costs move. Nothing rests on it: swapping in a
library is a change to `to_field` and what sits beside it, reaching no card, no
deck name and no part of the identity contract. Revisit when the subset stops
covering what cards actually use, or when a rendering bug turns out to be one a
library would not have had.

## 5. Every exported card carries a `kb::<id>` tag

A card found in Anki has to lead back to the file that made it — to fix it,
suspend it, or open its note. The ID is already in the `guid`
column, and **no Anki interface reads a guid back out**: not the browser, not
AnkiConnect. So it cannot be the mechanism, however right it is as the
identity.

The tag is written for **every kind** though only one needs it today. Printing
the ID in a field of that kind instead would work and cost two fewer API calls,
but it makes the export dispatch on kind for something that is not about kind,
and puts an identifier on the face of a card a person reads. The cost is one
collapsed `kb` parent in Anki's tag sidebar; browser searchability pays for it.

Understanding cards additionally show their note's ID on the front and an
instruction on the back. **That is a fallback for a human, not a mechanism** —
both are generated from `sources` at export, so neither can drift, and nothing
reads them back.

## 6. Agent material is fenced, and never converted

Agent-written material is kept — a diagram, a walkthrough, a delta report,
suggested follow-ups — because re-dictating it is the cost that made it
unaffordable. Where it lives is decided by what fragmentation costs at each
layer: at the raw layer **its own file**, because the raw layer is a journal
nobody rereads and a capture's value is that it is exactly what the user said;
in a note or an understanding card a **machine block**, because those are what
the user reads, and one subject must stay one file.

**`origin` carries the distinction, not `type`.** A separate kind for the
agent's file was considered and dropped: every skill that could confuse the two
already has to read `origin` — nothing may be carded from machine material
wherever it sits — so a second kind would be a duplicate switch, one more thing
to keep in step, and a false suggestion that the layer has two halves.

The rules travel with the origin and the fence, not the file: never carded,
rewritten freely by the agent. **No operation converts machine text
into the user's.**
Reading agent prose and thinking "yes, exactly" is the illusion of
understanding `motivation.md` §1.3 exists to prevent; what the user says in
answering a question about a block is theirs, and enters through capture or
update. This removes a per-item decision and closes the only real hazard.

## 7. Format choices that look arbitrary

The schema in `reference/schema/` states rules only; the reasons live here.

- **Two ID forms.** Items that stay in the base read well as `<slug>_<n>`, and
  kind is not part of identity, so a capture, its note and its verify reports
  share one number pool — the slug pool, which is also how a subject's history
  is found. A card leaves the base, and its ID becomes an Anki guid, a namespace
  shared with every deck ever imported: twelve base62 characters is 62¹² ≈
  3.2×10²¹ values, so even with ten million drawn the chance of any collision is
  about one in 64 million. Drawn by a script, because a model asked for a random
  string does not produce one.
- **References by ID, not path.** Items move between directories as a base is
  reorganised, and every path reference went stale with them. The filename
  contains the ID, so resolving one is a glob and survives any move.
- **Repositories by URL, never a local path.** Where a checkout sits is
  machine-local; an item naming it would be false on the next machine.
- **Evidence recorded once, where it was read.** Copying a capture's evidence
  into its note made notes' frontmatter longer than their bodies and gave the
  same fact two places to drift apart. Revalidation follows the chain.
- **`verified` holds the latest check, not a history.** A growing list said
  nothing a reader acted on; the history of what changed is in verify reports.
- **A card's sources are never evidence.** Staleness reaches a card through
  the item it was drawn from; a `commit` on a card would be a second copy of
  the same fact.
- **`importance` is the initial deck only.** Anki does not move an existing
  card on re-import, so a grade takes effect only before the first import —
  which is why an ungraded card is held back rather than defaulted. Demoting a
  card afterwards is a judgement made in review, from history this base cannot
  see.

## 8. How items change

- **A capture is open during the session that wrote it, and closed after —
  whichever origin.** Session, not day: an agent can know whether it wrote a
  file in this conversation, and a same-day rule would let a session with no
  memory of a file write into it, which is how an agent's claims once landed
  under the user's byline. One author per capture follows: `generated.by` is
  true by construction.
- **Captures are records, never to-do lists.** An `## Open / follow-ups`
  ledger was tried in 0.13 and dropped: a list meant to be crossed off cannot
  live in a closed file, and carrying it forward session to session is an
  obligation in another form. What a run skipped is reported in the
  conversation, and that is allowed to be the end of it.
- **Approval covers claims.** A scaffolding edit — a URL, a path, a diagram —
  keeps approval and `generated.at`; rewording the user asked for is approved
  by the asking; a claim change comes only from a dictated claim, re-stamped on
  acceptance. Clearing approval on every body change made a URL fix a review.
- **One item per run.** A run touching several notes produced a diff nobody
  could review, and the notes done one at a time gave the same result.
- **Verification is read-only and writes a report.** A check that may edit
  what it checks will, as soon as nothing dictated stands in its way.
