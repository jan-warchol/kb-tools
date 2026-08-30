---
name: kb-quiz
description: Quiz the user on topics from their knowledge base. Use when the user wants to be tested — "quiz me", "test me on X", "quiz me on last week's notes". Asks about reasoning and understanding rather than plain recall, captures anything new the user says, and logs the session.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-quiz

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

No knowledge base means nothing to quiz on: say so and offer `/kb-init`.

## Instructions

Ask questions about a topic selected from the knowledge base (usually a specific
note or set of notes). Use the information about sources from the frontmatter to
gather any additional necessary context, e.g. from source code.

Ask 1-2 questions per note. The questions should focus on reasoning and
understanding the topic, not on plain recall - recall is handled by flashcards
(if the knowledge base has flashcards related to the notes, you can skip facts
covered by the flashcards). Be careful not to give away the answers in the
questions. Also, try to formulate the questions so that the answer doesn't have
to be a long elaborate. If there are any logs of previous quizzes on the topic,
ask about the aspects that haven't been covered yet or that the user failed to
answer properly last time.

If you have access to the sources, you can expand the scope of the questions
slightly to cover adjacent, related issues. If the user provides information
that wasn't previously available in the quizzed item, take that part of his
answer and append it to the corresponding raw capture.

After the quiz is done, log the questions, answers, and any important comments
on the answers in a file.

## Appending, and the log

- **Verify what you append**, per `/kb-common`. If you cannot verify it now, do
  not append it: an unverified sentence inside a verified item makes the whole
  item's `verified` entry a lie. Say so, and offer `/kb-capture` for it instead.
- **Appending puts the raw item ahead of its note, and the note ahead of its
  cards.** Say which ones now trail and offer `/kb-redact`; do not quietly
  rewrite them.
- **The log is a record of an exchange and not a knowledge item**: plain
  markdown, no frontmatter, nothing downstream reads it. It goes where the
  previous logs live.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
