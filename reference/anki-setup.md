# Anki setup

Review belongs to Anki, not to this system (`decisions.md` §1), but a few of its
settings are load-bearing for decisions made *here*: the deck split by
importance means nothing unless the limits differ. These are the settings that
get lost and then quietly stop working.

`kb_anki.py status` and the deck options show the current state in a minute.

## Presets

**One preset per area, spanning every kind and both importances** — all of
`<root>::Recall::*`, and any kind added later.

FSRS parameters are fitted per preset from its own history, so a preset is a
claim about how one body of material is forgotten. Importance is not such a
claim; it is a policy about how much to hold on to, so splitting the preset by
it would only starve the optimiser of the history it needs.

**Genuinely different material gets its own preset** — technical knowledge and
a spoken language are not forgotten alike. A preset is assigned per deck, so
that needs a deck tree separating them, which is what `anki_deck_name:` is for:
a second area is a second knowledge base with its own root (`JW::Tech`,
`JW::Lang`). Decide it before the cards exist — deck renames do not round-trip.

Do not run the optimiser until several hundred reviews exist.

## Daily limits

New/day and reviews/day both carry a `Preset / This deck / Today only`
selector. **Set every one of them on `This deck`.**

A parent caps the total across its children; each child caps its own share.
**Always set the parent to the sum of its leaves**, which makes it inert and
lets the leaf limits mean what they say:

| Deck | New/day | Reviews/day |
|---|---|---|
| `<root>::Recall` | 5 | 30 |
| `<root>::Recall::Core` | 3 | 20 |
| `<root>::Recall::Extra` | 2 | 10 |

**This is what gives core priority, and the only thing that does.** The
tempting alternative — a low parent limit and generous leaves — cannot: limits
apply while the queue is *gathered*, before any ordering, so a binding parent
drops cards before anything can prefer core ones. A guaranteed share is the
guarantee.

Two consequences to accept knowingly:

- **A leaf's backlog can exceed its limit and wait.** 25 core reviews against a
  limit of 20 means five wait while extra still gets its ten. That is the price
  of the guarantee.
- **Change a leaf and the parent must change too**, or it silently starts
  binding and the guarantee is gone with no visible sign.

## Desired retention

Per deck like the limits, and **lower primarily for lower importance** — that
is what the knob is for. A starting point: `0.90` (the default) on
`Recall::Core` and `0.85` on `Recall::Extra`, where a review is expensive
enough to be worth buying interval with.

## Steps, and the learn-ahead limit

**One learning step and one relearning step, both 20 minutes.** A series of
steps second-guesses the scheduler; a single number lets it work. Steps are
preset-wide with no per-deck override, and 20 minutes is long enough that a
failed card is not asked again inside the same few minutes, which is the grind
that ends a session early. Steps must stay under a day.

**Set the learn-ahead limit to 5 minutes** — Preferences → Review, and
**global, not per preset**. At its default of 20 minutes it exactly cancels a
20-minute step, making a failed card available again at the end of the same
session, which is the grind the step length was chosen to prevent. At 5 the
congratulations screen appears with cards still pending later today; that is
intended.

## Orders

**Gather new cards at random.** The default introduces them in deck position
order, so extra's permanent backlog would arrive in the order the notes
happened to be written and its tail would wait forever. Preset-wide, no
per-deck selector. Per-leaf new limits still hold under random gather — worth
confirming after a week that what was introduced matches the 3/2 split.

**Review sort order: "Deck, then due date."** Deck order is alphabetical and
`Core` sorts before `Extra`, so a session abandoned halfway has done the core
cards. It changes only the order they arrive in, not which are gathered.

## Grading

**Press Again on failure, never Hard.** Hard means "recalled, with effort";
using it for a failure inflates every subsequent interval, silently and
irreversibly.

**Demote during review, in Anki, not here.** Whether a card has earned its
place is visible only from review history. Flag it (Ctrl+1…7) rather than
breaking the rhythm and move the flagged ones afterwards. Import never moves an
existing card, so the move sticks.

## Backups

**The cards regenerate from the markdown; the review history does not exist
anywhere else.** That is all a backup here has to protect, which is why
`kb_anki.py backup` exports the root deck with `includeSched: true` rather than
copying a collection.

```bash
python3 scripts/kb_anki.py backup     # <kb>/backups/anki-YYYY-MM-DD.apkg
```

**Commit it.** At ~100 KB it gets the same versioning and off-site copy as the
notes, and any past state is recoverable rather than only the last. Each export
is a fresh zip and nothing dedupes — a few MB a year at weekly cadence;
gitignore the directory if that stops being worth it.

`kb_anki.py status` reports the newest backup's age, because forgetting is the
actual failure mode. Nothing makes one unasked.

Two things to know before the day it matters:

- **Anki's own automatic backups** (Preferences → Backups) sit beside the
  collection on the same disk. They cover "I broke something", not "the disk
  died" — the gap the committed `.apkg` fills.
- **Restoring from a `.apkg` merges, it does not replace.** It is a repair
  tool, not a clean-slate restore.

If you sync to AnkiWeb, `kb_anki.py sync` is the better primary and the `.apkg`
is belt-and-braces. Decide which you rely on — "I have both" and "I have
neither" look identical until you need one.

## Two things never done in Anki's own interface

**Renaming decks or note types**, and **editing card text**. Both break the
identity contract the export depends on: renames do not round-trip, and edited
text is overwritten by the next import. Edit the markdown and re-export.
