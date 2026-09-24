---
name: kb-export
description: Export confirmed cards as an Anki import file, one deck per card kind and importance. Use when the user wants to export their cards or update their Anki decks — "export my cards", "make the anki deck".
allowed-tools: Read, Glob, Grep, Edit, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *)
---

# kb-export

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py     # --dry-run to look first
```

The script writes `<kb>/export/kb-export.txt` and nothing else. Report what it
printed: the count per deck, anything held back as unconfirmed or ungraded, and
any retired cards — **those it cannot retire for the user**, since an import
only adds and updates, so they need suspending in Anki by hand.

**Ungraded cards are the one thing to act on here**, and the only edit this
skill makes. Read them, then propose a grade for each in one pass — `core` is
what the user would be materially worse at their work for not producing
unprompted, `extra` is what it is enough to recognise or to know to look up.
Propose `extra` unless a card clears that bar: core stays useful only while it
stays small. Judge them against each other, which is the whole reason the grade
waits until here. Write `importance:` on the ones the user agrees with, then
re-run the export.

Then: File → Import in Anki, which matches on the card ID and so updates an
existing card in place, scheduling intact. What that implies for editing,
moving and renaming is in `reference/anki-setup.md`.
