---
name: kb-export
description: Export approved cards as an Anki import file, one deck per card kind. Use when the user wants to export their cards or update their Anki decks — "export my cards", "make the anki deck".
allowed-tools: Read, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *)
---

# kb-export

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py     # --dry-run to look first
```

Writes `<kb>/export/kb-export.txt` and regenerates each note's `cards:` list.
Report what it printed: the count per deck, anything held back as unapproved,
and any deprecated cards — **those it cannot retire for the user**, since a
package only adds and updates, so they need suspending in Anki by hand.

Then: File → Import in Anki. Re-import matches on the card ID in the guid
column, so an existing card is updated in its current deck with its scheduling
intact. Two consequences:

- **Editing card text in Anki does not survive** the next import. Edit the
  markdown and re-export.
- **Renaming a deck means renaming it in both places** — `DECKS` in
  `kb_export.py` and Anki. Renaming in Anki alone keeps the existing cards where
  they are, but the next new card recreates a deck under the old name and splits
  the collection in two.
