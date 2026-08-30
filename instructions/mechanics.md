<!-- WIP: relocated verbatim. Wording, overlaps and duplicates untouched. -->

# Mechanics

## Naming and sources

- When recording source code references, focus on the most important paths and symbols, not all of them.
- When choosing slug for the item ID, pick something that stands on its own - don't use truncated title.

## Card IDs

Draw it with `scripts/kb_cardid.sh <note-id> [count]` and never invent one — a
card ID doubles as the card's identity in the scheduler, where a repeat silently
overwrites another card's review history. **Card IDs are permanent**: rewording
a card keeps its ID, changing what it asks takes a new one.

## Frontmatter

Frontmatter is authoritative. Prose may name a file inline where it aids
reading; those mentions are decorative and are not maintained.

## Bearings

- **No knowledge base, no work on it.** Where the bearings report none, say so and offer `/kb-init`.
  The one exception is `/kb-capture`, which writes into the working directory instead and says so:
  dictation happens at the moment of learning, and a lost capture is not recoverable the way a
  misplaced file is.
- If the bearings report the knowledge base as found rather than configured, work in it, say so, and
  offer `/kb-init` to record it — it was found by looking around, not by being told where it is.

## After writing

Check the frontmatter of every item you wrote or changed — it catches mechanical
mistakes, and a skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```

Anything that is not a knowledge item — a quiz log, for one — carries no
frontmatter and is not checked.
