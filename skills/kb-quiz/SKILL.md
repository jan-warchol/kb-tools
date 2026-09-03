---
name: kb-quiz
description: Quiz the user on topics from their knowledge base. Use when the user wants to be tested — "quiz me", "test me on X", "quiz me on last week's notes". Asks about reasoning and understanding rather than plain recall, captures anything new the user says, and logs the session.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-quiz

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Instructions

Ask questions about a topic selected from the knowledge base (usually a specific
note or set of notes). Use the information about sources from the frontmatter to
gather any additional necessary context, e.g. from source code.

The questions should focus on reasoning and
understanding the topic, not on plain recall - recall is handled by flashcards
(if the knowledge base has flashcards related to the notes, you can skip facts
covered by the flashcards). Be careful not to give away the answers in the
questions. If there are any logs of previous quizzes on the topic,
ask about the aspects that haven't been covered yet or that the user failed to
answer properly last time.

If you have access to the sources, you can expand the scope of the questions
slightly to cover adjacent, related issues. If the user provides information
that wasn't previously available in the quizzed item, take that part of his
answer and append it to the corresponding raw capture.

Ask all questions about each note together.

After the quiz is done, ask whether the user would like another round. If not,
log the questions and answers (graded correct / partial / incorrect) in a file.

### Mode: quick / default / detailed

- Default: ask the questions so that answering requires no more than a short
  phrase (1-3 words). 2-3 questions per note.
- Detailed: ask more complex questions that can require a full sentence to answer.
  1-2 questions per note.
- Quick: ask multiple choice questions using Ask User Question Tool
  - **shuffle the answers** - always putting correct answer first ruins the quiz
  - use real alternatives from the knowledge base for the distractions rather than
    inventing them, if possible,
  - up to 4 questions per note.
- This is not about questions difficulty, just the effort required to answer them -
  although, obviously, detailed mode allows for harder questions.

## Appending, and the log

- **Repair and verify what you append**, per `/kb-common` — a spoken answer
  reaches you with the same transcription damage a dictated capture does. If you
  cannot verify it now, do not append it: an unverified sentence inside a
  verified item makes the whole item's `verified` entry a lie. Say so, and offer
  `/kb-capture` for it instead.
- **Appending puts the raw item ahead of its note, and the note ahead of its
  cards.** Say which ones now trail and offer `/kb-redact`; do not quietly
  rewrite them.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
