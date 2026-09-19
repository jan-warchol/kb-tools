---
name: kb-common
description: General instructions for working on the knowledge base. Use always when interacting with knowledge bases managed by kb-tools plugin.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_home.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_layout.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_user.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_repo.sh), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

## Bearings

**Knowledge base location:** !`${CLAUDE_PLUGIN_ROOT}/scripts/kb_home.sh`
**KB user:** !`${CLAUDE_PLUGIN_ROOT}/scripts/kb_user.sh`

KB layout:

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_layout.sh`

Save new items according to knowledge base conventions; ask if nothing fits.

Current repository:

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_repo.sh`

Source paths are relative to the repository root. No repository, or no
origin: cite the documents you read instead.

Find items with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py`: by ID, a
slug pool (`--pool <slug>`), or what refers to an item (`--refs <id>`). Refer to
items by `kb:<id>`, never by path.

## Flow

```
dictation    ─▶ capture ─┬▶ note ─▶ card ─▶ export ─▶ Anki
                         └▶ card
agent output ─▶ capture (origin: machine) ─▶ machine blocks in the note
note         ─▶ /kb-verify ─▶ capture (origin: machine): the verify report
```

Every stage after capture is optional: a capture is a finished item. A capture
is one kind; `origin` says whether the user dictated it or you wrote it.

## Changing items

- **One item per run.** One note, its cards, one verify report. Several ⇒ one
  at a time, each shown and settled before the next. Never an operation across
  notes.
- **A capture is open during the session that wrote it, closed after** — both
  origins. Open: add to it, reword it. Closed: never touched again; anything
  later is a new capture, same slug, next free number. Not certain this
  conversation wrote it ⇒ closed.
- **One author per capture.** Your claims never enter the user's capture — not
  as prose, not fenced. They are a machine capture.
- **A note is the current state; the slug pool is its history.** Every sentence
  outside a machine block traces to a human capture. A note never narrates
  what changed.
- **Edits and approval:**

  | Edit | `approved` | `generated.at` |
  |---|---|---|
  | scaffolding — URL, path, identifier, diagram, formatting | stays | stays |
  | rewording the user asked for | moves to now: asking is approving | moves |
  | a claim | only from a claim the user dictated; re-stamped when they accept the wording | moves |

- **A correction the user dictates is verified on the spot**, whatever the
  effort — it is one claim. Only one that cannot be checked stays `draft`, and
  you say so.
- **After a card changes, export** (`kb_export.py`) and tell the user to
  import. It writes only the export file.

## Claims and scaffolding

- **Claims are the user's, always** — causation, consequence, why, tradeoffs.
  Never add a claim to a human-origin item that the user did not articulate.
  Articulating does the learning.
- **Scaffolding you may supply** — identifiers, paths, call order, the
  topology of a diagram. That is transcription of the code, not composition
  of knowledge.
- Agent-written material lives in a machine-origin capture or a machine block
  (schema), is never carded, and never becomes the user's by being agreed
  with: the user's *answer* to a question about it is theirs.
- Choose slugs that stand on their own, not truncated titles. Don't show
  frontmatter for approval.

## The general pattern

Under most project-specific stumbles there is a general pattern — the
language, the framework's execution model, a pattern with a name. You may
suggest it. The user articulates it, and their sentence is what is kept, like
any other claim. It is captured on its own and verified like any other
capture, against the code the pattern was seen in — never against the capture
it came out of, which is a mention at most and not a source.

**Written to travel.** Word a general pattern so it could be typed or read
aloud by hand into another knowledge base: self-contained, naming no
repository, path, identifier or term of the project it was seen in. That check
runs here, where the project is visible.

Dictated elsewhere, it arrives as an ordinary dictation — the user's words,
verified against an example you can see. Find none and keep it unverified: a
pattern that cannot be grounded outside the codebase that prompted it is
probably not general yet.

## Effort

The user's word — quick, normal (the default), thorough — sets **how much work
happens, never how well it is done**. Nothing in the quick column is done
sloppily; it is simply not done, and what was left is said (below).

Effort is depth, never breadth: no row reaches beyond the item in hand.

| | quick | normal | thorough |
|---|---|---|---|
| **verifying** | nothing; record the repository and `commit` from the bearings and any path the user named; no `verified` key, `status: draft` | the claims the item turns on, hedged ones first | everything, following the code paths |
| **capture** | the dictation, and stop | plus the glance at the base, and the general pattern suggested where you see one | as normal, verifying thoroughly |
| **redact** | promote as-is or compress minimally; no outline step | outline then fill; an existing note edited in the affected sections | the note rebuilt from its whole slug pool |
| **cards** | the one or two obvious facts, and the understanding card | a full sweep of the item, and the understanding card | as normal |
| **update** | the new capture, and stop | plus the note's affected sections and its cards | the note rebuilt from its whole slug pool, then its cards |
| **verify** | paths changed since `commit`: scaffolding only | plus the claims the note turns on | every claim |

## Verification

- **Report before you write.** An incorrect or outdated claim stops you before
  anything is written: quote it, let the user state the correction. Their
  correction is a claim (above); yours never is.
- **Don't give the answer away** — point at what is wrong, not at what is right.
- **Check against evidence.** Read the code; never reason
  from identifier names.
- **Record what you read** in `sources`: `path`, `symbol` where meaningful,
  `commit`. The important ones, not all of them.
- **`verified` is your latest check**, replacing any earlier one. `approved`
  is the user's, stamped only when they say so, never read out of silence.

## Dictation

Recognition predicts from context, so errors land on the words carrying the
meaning: lost casing, `camelCase` / `kebab-case`, approximated paths,
sound-alikes (`ack` / `act`). Read the code to find the real spelling; never
guess; ask if you cannot tell. Repair only what was *meant* as an identifier —
"the config file" stays as spoken. Add sentence breaks. Nothing else about the
user's words is touched.

## Stopping

- **Say what you skipped** — claims left unchecked, follow-ups, patterns you
  saw — to the user, in a line or two, and offer nothing further. It is not
  written anywhere: a capture is a record, never a to-do list, and stopping
  is allowed to be the end of it.
- **Terse.** One line per item, less than a sentence: what, and where. No
  rationale, no restating the claim, no padding.
- `status: abandoned` is how the user declines something — a capture that will
  not be redacted, a follow-up not worth pursuing, a note overtaken by events.
  Ask before stamping it, record it, and delete nothing.

## After writing

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```
