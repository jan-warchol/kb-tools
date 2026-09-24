---
name: kb-common
description: General instructions for working on the knowledge base. Use always when interacting with knowledge bases managed by kb-tools plugin.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_home.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_layout.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_repo.sh), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

## Bearings

**Knowledge base:** !`${CLAUDE_PLUGIN_ROOT}/scripts/kb_home.sh`

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_layout.sh`

Save new items by those conventions; ask if nothing fits.

**Repository:** !`${CLAUDE_PLUGIN_ROOT}/scripts/kb_repo.sh`

`paths` are relative to its root; with no repository, cite the documents you
read instead. Find items with `python3
${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py` — by ID, a slug pool (`--pool
<slug>`), or what refers to an item (`--refs <id>`). Name items by `kb:<id>`,
never by path.

## Flow

```
dictation ─▶ /kb-capture ─▶ capture ─▶ /kb-redact ─▶ note ─▶ /kb-cards ─▶ card ─▶ /kb-export ─▶ Anki
your output ─▶ capture (authored: agent) ─▶ agent blocks in a note
a note against today's code ─▶ /kb-verify ─▶ capture (authored: agent)
```

Every stage after capture is optional, and a capture the user points at can be
carded directly. **A correction is a new capture, then `/kb-redact` again** —
there is no update command.

## Rules

- **One item per run** — one note, its cards, one verify report. Several ⇒ one
  at a time, settled before the next. Never an operation across notes.
- **A closed capture is never touched again** — anything later is a new one,
  same slug, next free number. Not certain this conversation wrote it ⇒ closed.
- **Your claims never enter the user's capture**, not as prose and not fenced:
  they are an `authored: agent` capture of their own.
- **A note never narrates what changed** — the slug pool is its history.
- **Scaffolding** — a URL, a path, a renamed identifier, a redrawn diagram —
  needs no capture and moves no status or `date`, and applies across a note and
  its cards directly.
- **A dictated correction is verified on the spot**, whatever the effort: it is
  one claim. Only one that cannot be checked stays `draft`, and you say so.
- **After a card changes, export** (`kb_export.py`) and say to import.

## Claims are the user's, scaffolding is yours

Causation, consequence, why, tradeoffs: never add one to an `authored: human`
item that the user did not articulate — articulating does the learning.
Identifiers, paths, call order, the topology of a diagram you may supply, being
transcription of the code rather than composition of knowledge. Your own
material never becomes the user's by being agreed with: their *answer* to a
question about it is theirs. Slugs stand on their own, not truncated titles;
never show frontmatter for approval.

**The general pattern** under a project-specific stumble — the language, the
framework's execution model, a pattern with a name — you may suggest once. The
user's sentence is what is kept: its own capture, verified against the code the
pattern was seen in, never against the capture it came out of. **Word it to
travel**, naming no repository, path or identifier of the project, so it can be
read aloud into another base; arriving that way it is an ordinary dictation,
verified against an example you can see, and `draft` if there is none.

## Checking

- **Report before you write.** An incorrect or outdated claim stops you: quote
  it, let the user state the correction. Theirs is a claim; yours never is.
- **Don't give the answer away** — point at what is wrong, not at what is right.
- **Read the code**, never reason from identifier names, and record what the
  claims turn on in `code` and `paths`.
- **Repair dictation** where recognition failed on the words carrying the
  meaning: lost casing, `camelCase` / `kebab-case`, approximated paths,
  sound-alikes (`ack` / `act`). Find the real spelling in the code, never
  guess, ask if you cannot tell, and repair only what was *meant* as an
  identifier — "the config file" stays as spoken. Add sentence breaks, and
  touch nothing else.

## Effort, and stopping

**quick** does the least that is still the operation, and stops; **normal** is
the default; **thorough** follows the code paths. Nothing is done sloppily at
quick — it is simply not done. **Effort is depth, never breadth**: no level
reaches beyond the item in hand.

**Say what you skipped** in a line or two — claims unchecked, follow-ups,
patterns you saw — then offer nothing further. It is written nowhere: a capture
is a record, never a to-do list, and stopping is allowed to be the end of it.
Be terse: one line per item, what and where, no rationale or restatement.
`status: retired` is how the user declines something, and how a claim that
stopped being true is marked — ask first, and delete nothing.

## After writing

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```
