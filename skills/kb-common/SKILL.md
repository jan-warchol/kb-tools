---
name: kb-common
description: General instructions for working on the knowledge base. Use always when interacting with knowledge bases managed by kb-tools plugin.
---

## General flow

```
dictation ─▶ raw capture ─▶ note ─▶ card ─▶ export ─▶ Anki
```

- **NEVER add new information to items with human origin on your own.** Only add
  information that the user explicitly articulated, or that comes directly from
  other updated knowledge base items. Articulating does the learning.
- When choosing slug for the item ID, pick something that stands on its own -
  not a truncated title.
- Don't show frontmatter for approval.

## Verification

Applies wherever a claim is checked — capture, redaction, and anything that
writes a `verified` entry:

- **Report, don't fix silently.** An incorrect or outdated claim stops you:
  let the user state the correction. Discovering the error is the most valuable
  thing a check produces, and a silent repair spends it. Once they have stated
  it, fold it into the text — an item holds what the user claims, not the
  exchange that produced it.

- **Check what has not been checked.** Material already carrying a `verified`
  entry is rechecked by revalidation, not here. One item can hold both, where
  something was appended after the last check.

- **Don't give the answer away:** give the user a pointer to what is wrong, so
  that they can figure it out on their own and learn. Don't make the answer
  inferable from the pointer.

- **Check claims against evidence, never against plausibility.** The codebase
  when the claim is about code, the cited sources otherwise. Read the code;
  never reason from identifier names.

- **Record what you read**, in `sources`: the repo-relative
  `path`, the `symbol` where one is meaningful, and the `commit` it was read at.
  Focus on the most important paths and symbols, not all of them.

- **Your `verified` entry is machine confirmation and nothing more.** A `human:`
  entry means the user has said so themselves; never stamp one on their behalf,
  and never read it out of their silence.

- Where the claims were not checked, write no `verified` key and
  `status: draft`.

## Dictation

Wherever the user speaks — a capture, an update, an answer during a quiz —
recognition predicts from context, so the errors land on exactly the words
carrying the meaning: identifiers whose casing was lost, `camelCase` /
`kebab-case` confusions, approximated paths, similar-sounding substitutions
(`ack` / `act`, `enqueue` / `and queue`).

Read the code to find the real spelling; never guess a plausible one, and ask if
you cannot tell what was meant. Repair only what was *meant* as an identifier:
"the config file" stays as spoken even where the parameter is called
`fileSettings`, because describing a thing in plain English is not a
mis-transcription of its name. Dictation may be unpunctuated, so sentence breaks
are part of the repair.

This is the one exception to **report, don't fix**: recovering the identifier
the user meant to say does not change what they claimed. Nothing else about
their words is touched.

## After writing

Check the frontmatter of every item you wrote or changed — it catches mechanical
mistakes, and a skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```
