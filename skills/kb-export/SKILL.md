---
name: kb-export
description: Export approved cards as an Anki import file, one deck per card kind and importance. Use when the user wants to export their cards or update their Anki decks — "export my cards", "make the anki deck".
allowed-tools: Read, Glob, Grep, Edit, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *)
---

# kb-export

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py     # --dry-run to look first
```

The script writes `<kb>/export/kb-export.txt` and nothing else — it never
writes back into the knowledge base. Report what it printed: the count per deck,
anything held back as unapproved (no `approved` key) or ungraded, and any
deprecated cards — **those it cannot retire for the user**, since a package
only adds and updates, so they need suspending in Anki by hand.

**Ungraded cards are the one thing to act on here**, and the only edit this
skill makes. Read them, then propose a grade for each in one pass — `core` is
what the user would be materially worse at their work for not producing
unprompted, `extra` is what it is enough to recognise or to know to look up.
Propose `extra` unless a card clears that bar: core stays useful only while it
stays small. Judge them against each other, which is the whole reason the grade
waits until here. Write `importance:` on the ones the user agrees with, then
re-run the export.

Then: File → Import in Anki. Re-import matches on the card ID in the guid
column, so an existing card is updated in its current deck with its scheduling
intact (`decisions.md` for why identity sits there). Three consequences:

- **Editing card text in Anki does not survive** the next import. Edit the
  markdown and re-export.
- **Moving a card between decks in Anki does survive**, and is meant to: an
  existing card is never relocated by an import, so `importance:` places a card
  once and demoting it later belongs in Anki, where the review history that
  justifies it lives.
- **Renaming a deck means renaming it in both places** — `anki_deck_name:` in
  `<kb>/knowledge-base.yaml` (or `.yml`) and Anki. Renaming in Anki alone keeps the existing
  cards where they are, but the next new card recreates a deck under the old
  name and splits the collection in two.
