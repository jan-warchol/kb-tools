# Personal learning system — decisions

Choices made about things outside this system, recorded so they are not
re-litigated. Nothing here is an instruction, and editing a skill never obliges
a change to this file — that is the point of keeping it separate.

## 1. Review is Anki's, not ours

The system owns everything from the spoken sentence to the moment a card is
handed to the scheduler. It does not own scheduling and does not implement a
review interface. Noticing when what it holds has stopped being true stays
inside the boundary.

**Nothing in the motivation puts it there.** A system that scheduled and
presented its own reviews would satisfy the same obligations. The boundary is
drawn where it is because Anki already implements that half, well, and reusing
it is cheaper than rebuilding it — a reason that could stop being true, at
which point the boundary should move rather than be defended.

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

One importable package, one deck per card kind. The card ID goes in the `guid`
column and that is the whole of what stable identity needs; a binary package
would add a dependency to carry the same fact.

Deck names belong to the identity contract as much as card IDs do: the
scheduler keys review history off them, so a rename means renaming in both
places, and renaming a *kind* moves its cards to a new deck.
