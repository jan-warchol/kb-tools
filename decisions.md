# Personal learning system — decisions

Choices made about things outside this system, recorded so they are not
re-litigated. Nothing here is an instruction, and editing a skill never obliges
a change to this file — that is the point of keeping it separate.

## 1. Review is Anki's, not ours

The system owns everything from the spoken sentence to the moment a card is
handed to the scheduler: not scheduling, and no review interface. Noticing when
what it holds has stopped being true stays inside the boundary.

**Understanding cards once crossed it** — `/kb-quiz` questioned the user on a
note and sent the grade through AnkiConnect, since a self-graded "did I
understand that?" is the unreliable judgement. The quiz went in 0.15 and the
kind in 0.16: a review that means reasoning through a whole note costs far more
than a recall card and did not return it, so those cards went unreviewed.
Recall cards are the only kind, the line holds without exception, and
`kb_anki.py` keeps only status, backup and sync. The question the kind was for
is open, not settled (`deferred.md`).

## 2. Why the card ID goes in Anki's `guid` column

Anki matches an imported row on the first field, or on `guid` when the file
supplies one. **Matching on the first field makes the question text the
identity**, so fixing a typo orphans a card's review history and adds a second
card. That alone is disqualifying: permanent IDs exist to make rewording free.

Anki's manual recommends a custom ID in the first field instead, without saying
why. Three properties of a guid explain it, each already answered here: the
namespace is **global** and a collision is silent, which the random tail
answers; a guid is **invisible from inside Anki**, accepted because this deck is
generated and the fix for anything wrong is a corrected card and a re-import;
and it **disables duplicate handling** on import, which nothing wants, a
duplicate ID being fatal at export already. The alternative costs a custom
notetype, and **a text import cannot create one** — it would have to be built by
hand on every machine before the first import worked. The export targets stock
`Basic`.

## 3. The export is a tab-separated text file

One file, one deck per card kind, split again by `importance` —
`Knowledge::Recall::Core` and `::Extra` — because daily limits and desired
retention are settable per deck and nowhere else. The ID in the `guid` column
is the whole of what stable identity needs; a binary package would add a
dependency to carry the same fact. The split is uniform across kinds although
one kind exists: a text import creates decks lazily, so a kind that never
grades a card `extra` never creates that deck, and making the deck path depend
on the data instead is how a collection gets split in two. Deck names are part
of the identity contract — the scheduler keys review history off them — so a
rename means renaming in both places.

## 4. The export renders HTML, not markdown

Anki renders markdown not at all: under `#html:false` a `**zipapp**` reaches
review with its asterisks showing, and the blank line separating an answer from
its example collapses to nothing. The cards rely on both. So `kb_export.py`
renders the subset they use — paragraphs, lists, fenced and inline code, bold
and italic — and sets `#html:true`. It is a small hand-written renderer rather
than a library because the export is a gate, and a second dependency to format
five constructs is not worth installing; anything outside the subset is escaped
and passed through, degrading to its literal text rather than to broken markup.

**The renderer is provisional in a way the `#html:true` above it is not.**
Rendering at all is forced by what Anki does with a field; hand-writing it is a
cost judgement, and costs move. Swapping in a library touches `to_field` and
nothing in the identity contract.

## 5. Every exported card carries a `kb::<id>` tag

A card found in Anki has to lead back to the file that made it. The ID is
already in `guid`, but **no Anki interface reads a guid back out** — not the
browser, not AnkiConnect — so it cannot be the mechanism, however right it is
as the identity. Printing the ID in a field would work and cost two fewer API
calls, but it puts an identifier on the face of a card a person reads. One
collapsed `kb` parent in the tag sidebar is the price of searchability.

## 6. Agent material is fenced, and never converted

It is kept — a diagram, a walkthrough, a delta report — because re-dictating it
is the cost that made it unaffordable. Where it lives follows what
fragmentation costs at each layer: at the raw layer **its own file**, since
that layer is a journal nobody rereads and a capture's value is being exactly
what the user said; in a note an **agent block**, since a note is what the user
reads and one subject must stay one file.

**`authored` carries the distinction, not `type`.** A separate kind was
considered and dropped: every skill that could confuse the two already reads the
byline, so a second kind would be a duplicate switch to keep in step.

**No operation converts agent text into the user's.** Reading agent prose and
thinking "yes, exactly" is the illusion of understanding `motivation.md` §1.3
exists to prevent. What the user says in *answering a question* about a block is
theirs, and enters through capture like anything else.

## 7. Format choices that look arbitrary

`reference/schema.md` states rules only; the reasons live here.

- **One byline, naming whose claims these are — never who typed.** A separate
  key for the typist went false in use: an agent appended its own claims to a
  dictated capture while the byline still read as the user's. Typing is not
  authorship (`motivation.md` §1.3), so a note the agent worded from the user's
  captures is `authored: human`, and no second key can disagree with the first.
  Which model wrote a file is in git; the actor prefixes went with it, one base
  having one user.
- **`status: confirmed` is one act, not two.** `verified` (the agent's check)
  and `approved` (the user's keep) were separate stamps for a distinction the
  workflow never exercises: every skill presents before it writes and works one
  item per run, so both happen in the same breath. Given up with them is the
  mechanical stale-approval check; `kb_check.py` warns instead when a confirmed
  note's slug pool holds a human capture the note does not list, which is the
  case that actually occurred.
- **`retired` does not say why.** `deprecated` and `abandoned` both meant
  *don't drill this, don't delete it*, and nothing read the difference.
- **Two ID forms.** Items staying in the base read well as `<slug>_<n>`, and
  kind is not part of identity, so a subject's captures, note and verify
  reports share one number pool — which is also how its history is found. A
  card leaves the base and its ID becomes a guid, in a namespace shared with
  every deck ever imported: twelve base62 characters is 62¹² ≈ 3.2×10²¹, so
  even with ten million drawn a collision is about one in 64 million. Drawn by
  a script, because a model asked for a random string does not produce one.
- **References by ID, not path.** Items move as a base is reorganised, and
  every path reference went stale with them. The filename contains the ID, so
  resolving one is a glob.
- **Evidence is `code` and `paths`: one repository at one commit, per item.** A
  repository by URL, never a local path, because where a checkout sits is
  machine-local. One per item, because an item is checked in one run against
  one HEAD — a second entry is a second moment pretending to be one. The nested
  `sources` this replaced carried `symbol` and `retrieved`, which nothing read,
  and let a note copy its captures' evidence until frontmatter outgrew bodies.
  Evidence is recorded once, where it was read; revalidation follows the chain.
- **A card's evidence is never its own.** Staleness reaches a card through the
  item it came from; a `commit` on a card is a second copy free to drift.
- **`importance` is the initial deck only.** Anki does not move an existing card
  on re-import, so a grade takes effect only before the first import — which is
  why an ungraded card is held back rather than defaulted. Demoting later is a
  judgement made from review history this base cannot see.

## 8. How items change

- **A capture is open during the session that wrote it, closed after** —
  whichever author. Session, not day: an agent knows whether it wrote a file in
  this conversation, and a same-day rule would let a session with no memory of
  one write into it, which is how an agent's claims once landed under the
  user's byline. One author per capture follows, and the byline is true by
  construction.
- **Captures are records, never to-do lists.** An `## Open / follow-ups` ledger
  was tried in 0.13 and dropped: a list meant to be crossed off cannot live in a
  closed file, and carrying it forward session to session is an obligation in
  another form. What a run skipped is said in the conversation, and that is
  allowed to be the end of it.
- **A note is a projection of its slug pool.** Rebuilding it from the whole pool
  is *thorough* effort, not the default, because a rebuilt note has to be
  re-reviewed whole; the default edits the sections newer captures affect.
- **Confirmation covers claims.** A scaffolding edit changes neither `status`
  nor `date`; a changed claim returns the item to `draft` until the user accepts
  the wording. Clearing confirmation on every body change made a URL fix a
  review.
- **One item per run.** A run touching several notes produced a diff nobody
  could review, and the notes done one at a time gave the same result.
- **Verification is read-only and writes a report.** A check that may edit what
  it checks will, as soon as nothing dictated stands in its way — it happened: a
  verify pass rewrote a note's prose, added claims of its own, and left the
  approval standing. `/kb-verify` declares no `Edit`.
