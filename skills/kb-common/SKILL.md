---
name: kb-common
description: General instructions for working on the knowledge base. Use always when interacting with knowledge bases managed by kb-tools plugin.
---

```
dictation ─▶ raw capture ─▶ note ─▶ card ─▶ export ─▶ Anki
```

- When working on items with human origin, only add new information when the user explicitly
  articulated it, or it comes from updated source items. NEVER add new information on your own.
  Articulating is the step that does the learning.
- When updating notes, prefer simply removing stale claims rather than describing change history.
- After a raw capture is created, prefer appending new statements to it rather than editing what was written.
  That is a default, not a prohibition: a user who asks for a raw item to be changed or removed gets it
  changed or removed.
- When new information is added, update downstream items (notes from raw captures, cards from notes etc).
- When recording source code references, focus on the most important paths and symbols, not all of them.
- When choosing slug for the item ID, pick something that stands on its own - don't use truncated title.
- If you discover incorrect or outdated claims, don't say the correct answer. Give the user a pointer to
  what is wrong, so that he can figure it on his own and learn. Don't make the answer inferable from the
  pointer.
- An unverified note is not allowed to produce cards.
- **No knowledge base, no work on it.** Where the bearings report none, say so and offer `/kb-init`.
  The one exception is `/kb-capture`, which writes into the working directory instead and says so:
  dictation happens at the moment of learning, and a lost capture is not recoverable the way a
  misplaced file is.
- If the bearings report the knowledge base as found rather than configured, work in it, say so, and
  offer `/kb-init` to record it — it was found by looking around, not by being told where it is.

## Verification

Applies wherever a claim is checked — capture, redaction, and anything that
writes a `verified` entry.

- **Check claims against evidence, never against plausibility.** The codebase when
  the claim is about code, the cited sources otherwise. Read the code; never reason
  from identifier names.
- **Report discrepancies; never fix them silently.** An incorrect claim stops you:
  say what is wrong and let the user state the correction. Discovering the error is
  the most valuable thing a check produces, and a silent repair spends it.
- **Record what the check actually looked at**, in `sources`: the repo-relative
  `path`, the `symbol` where one is meaningful, and the `commit` it was read at.
  None of that can be recovered later, once the verifying context is gone.
- **Your `verified` entry is machine confirmation and nothing more.** A `human:`
  entry means the user has said so themselves; never stamp one on their behalf, and
  never read it out of their silence.
- **Unverified means draft.** Where the claims were not checked, write no `verified`
  key and `status: draft`.
- **Verify once.** What an earlier step already checked is not rechecked by a later
  one — read only what the task in front of you needs.
- **Never copy an actor or a timestamp out of an example**; re-sample with `date -u`.

## After writing

Check the frontmatter of every item you wrote or changed — it catches mechanical
mistakes, and a skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```

Anything that is not a knowledge item — a quiz log, for one — carries no
frontmatter and is not checked.
