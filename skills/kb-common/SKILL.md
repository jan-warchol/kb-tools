---
name: kb-common
description: General instructions for working on the knowledge base. Use always when interacting with knowledge bases managed by kb-tools plugin.
---

## Flow

```
dictation    ─▶ capture ─┬▶ note ─▶ card ─▶ export ─▶ Anki
                         └▶ card
agent output ─▶ capture (origin: machine) ─▶ machine blocks in the note
```

Every stage after capture is optional: a capture is a finished item. A capture
is one kind; `origin` says whether the user dictated it or you wrote it.

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
sloppily; it is simply not done, and what was left is written down (below).

| | quick | normal | thorough |
|---|---|---|---|
| **verifying** | nothing; record the repository and `commit` from the bearings and any path the user named; no `verified` key, `status: draft` | the claims the item turns on, hedged ones first; say which you left | everything, following the code paths |
| **capture** | the dictation, and stop | plus the glance at the base, and the general pattern suggested where you see one | plus the neighbouring items noted for the redactor |
| **redact** | promote as-is or compress minimally; no outline step | one capture, outline then fill | several captures into one subject note; sibling notes checked for contradiction |
| **cards** | the one or two obvious facts | a full sweep of the item | plus cross-item cards and an understanding card |
| **update** | record in the capture and stop | fold into the note | plus cards and sibling notes checked against the change |

`/kb-quiz` has its own three modes, which set the length of an answer rather
than the amount of work; they are in that skill.

## Verification

- **Report, don't fix silently.** An incorrect or outdated claim stops you: let
  the user state the correction, then fold it into the text.
- **Don't give the answer away** — point at what is wrong, not at what is right.
- **Check against evidence.** Read the code; never reason
  from identifier names.
- **Record what you read** in `sources`: `path`, `symbol` where meaningful,
  `commit`. The important ones, not all of them.
- **Your `verified` entry is machine confirmation.** `approved` is the user's,
  stamped only when they say so, never read out of silence.

## Dictation

Recognition predicts from context, so errors land on the words carrying the
meaning: lost casing, `camelCase` / `kebab-case`, approximated paths,
sound-alikes (`ack` / `act`). Read the code to find the real spelling; never
guess; ask if you cannot tell. Repair only what was *meant* as an identifier —
"the config file" stays as spoken. Add sentence breaks. Nothing else about the
user's words is touched.

## Stopping

- **Every run records what it skipped** — claims left unchecked, follow-ups
  worth a look, patterns you saw — under `## Open / follow-ups` in the
  machine-origin capture for the subject, creating that capture if there is
  none. Always there, never in the note: the note is what the user reads for
  understanding, and a todo list is not that. Low effort is then never a loss.
- **Terse.** One line per item, less than a sentence: what, and
  where. No rationale, no restating the claim, no "worth a look" or other
  padding; merge items that point at the same place. The schema's example is
  the length to aim for.
- **Report it to the user too**, in a line or two, and offer nothing further.
- `status: abandoned` is how the user declines something — a capture that will
  not be redacted, a follow-up not worth pursuing, a note overtaken by events.
  Ask before stamping it, record it, and delete nothing.

## After writing

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```
