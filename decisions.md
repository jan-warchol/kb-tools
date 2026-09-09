# Personal learning system — decisions

Choices made about things outside this system, recorded so they are not
re-litigated. Nothing here is an instruction, and editing a skill never obliges
a change to this file — that is the point of keeping it separate.

## 1. Review is Anki's, not ours — with one deliberate exception

The system owns everything from the spoken sentence to the moment a card is
handed to the scheduler. It does not own scheduling and does not implement a
review interface. Noticing when what it holds has stopped being true stays
inside the boundary.

**Understanding cards cross it, knowingly.** They ask whether the user can
reason with a note, which a self-graded "did I understand that?" cannot answer
— that judgement is exactly the unreliable one. So for that kind the grade is
produced here: `/kb-quiz` conducts the review, `scripts/kb_anki.py` sends the
result.

Scheduling is still not ours, and the split is sharper than it looks: the quiz
drives **Anki's own reviewer** through AnkiConnect rather than searching for
due cards, so limits, orders and steps stay the scheduler's. Only the grade
crosses — and even that is proposed, not sent: the user presses the button.

Two consequences, accepted. **`/kb-quiz` is the only review path for the kind**
— no phone, no AnkiWeb, Anki running locally; recall review is unaffected. And
**the kind cannot be reviewed in Anki's interface at all**, since what it shows
there is a placeholder and any button pressed on it is a wrong grade, which is
why `reference/anki-setup.md` makes "never click the parent deck" a rule.

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

A card found in Anki has to lead back to the file that made it — `/kb-quiz`
needs that when the scheduler hands it one. The ID is already in the `guid`
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
