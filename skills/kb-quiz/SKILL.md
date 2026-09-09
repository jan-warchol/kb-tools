---
name: kb-quiz
description: Quiz the user on topics from their knowledge base. Use when the user wants to be tested — "quiz me", "test me on X", "quiz me on last week's notes". Asks about reasoning and understanding rather than plain recall, captures anything new the user says, and logs the session.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py *), AskUserQuestion
---

# kb-quiz

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Two ways in

**No topic → review what Anki says is due** (below). **A topic → quiz it**, and
grade its understanding card too if it has one.

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
answer properly last time. Questions can contain short code snippets.

If you have access to the sources, you can expand the scope of the questions
slightly to cover adjacent, related issues. If the user provides information
that wasn't previously articulated, capture it.

Ask all questions about each note together.

After the quiz is done, ask whether the user would like another round. If not,
log the questions and answers (graded correct / partial / incorrect) in a file,
with the grade sent to Anki for each card. **What was missed is what the log is
for** — the next quiz on that note leads with it.

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

## Scheduled review

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py status    # what is due, and the backup age
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py session   # open the reviewer, report the first card
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py next      # the card showing now
```

`session` is Anki's Study Now button, so every limit and ordering is the
scheduler's — never search for due cards instead. `card: none` ends the
session. Exit 3 means Anki is not running: offer a topic quiz, and grade
nothing.

Per card: quiz the note it names, in **detailed** mode; say which answers were
right and which were not; offer the four grades with AskUserQuestion, your
recommendation first, each labelled with the interval `next:` printed for it.
Then `grade <ease> <card>`, then `next`.

**Hard is a real option here**, unlike in recall review — the log carries what
was missed and the next quiz leads with it.

Topic mode has no reviewer to drive: find the note's understanding card and
grade it with `grade-card <card-id> <ease>`.

**Backups.** `status` reports the newest one. Older than a week, or none, and
the review history exists in a single place — say so and offer `kb_anki.py
backup`. Never run it unasked.

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
