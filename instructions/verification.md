<!-- WIP: relocated verbatim. Wording, overlaps and duplicates untouched. -->

# Verification

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

## Correcting the user

- If you discover incorrect or outdated claims, don't say the correct answer. Give the user a pointer to
  what is wrong, so that he can figure it on his own and learn. Don't make the answer inferable from the
  pointer.
