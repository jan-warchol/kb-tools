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

## Verification

Applies wherever a claim is checked — capture, redaction, and anything that
writes a `verified` entry:

- **Report, don't fix silently.** An incorrect or outdated claim stops you:
  let the user state the correction. Discovering the error is the most valuable
  thing a check produces, and a silent repair spends it.

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

## After writing

Check the frontmatter of every item you wrote or changed — it catches mechanical
mistakes, and a skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```
