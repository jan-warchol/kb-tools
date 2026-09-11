---
name: kb-quiz
description: Quiz the user on topics from their knowledge base. Use when the user wants to be tested — "quiz me", "test me on X", "quiz me on last week's notes". Asks about reasoning rather than plain recall, grades understanding cards, and logs the session so the next quiz leads with what was missed.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py *), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), AskUserQuestion
---

# kb-quiz

Questions the user on what the base holds, grades the answers, and leaves a log
the next quiz reads.

**No topic → review what Anki says is due. A topic → quiz that topic.**

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

## Rules

- **Ask about reasoning, not recall.** Plain facts are what the cards drill;
  skip anything a card on that note already asks. A question here makes the user
  derive a consequence, compare two things, predict what would happen, or say
  why something is the way it is.
- **Never give the answer away** — not in the question, not in its framing, not
  in a set of options where only one is not absurd.
- **Grade against the note and what it cites**, never against plausibility
  (`/kb-common`). Read the code its `sources` name before judging an answer that
  turns on it.
- **Repair a spoken answer before judging it** (`/kb-common`). An answer arrives
  with the same transcription damage a dictated capture does, and marking
  `camelCase` wrong because it was heard as two words is a false negative.
- **Lead with what was missed.** The logs for a note say what went wrong last
  time and what has never been asked; open there, and move on once it is
  answered well.
- **Anything new the user articulates leaves through the front door.** A claim
  they make mid-quiz is knowledge the base does not hold yet: `/kb-update` where
  the subject is already there, `/kb-capture` where it is not. Never append it
  to a note or a raw item yourself, and never let the log carry it — a log
  records what was asked and answered, not what is true.
- **The grade is proposed, never sent unasked**: say what was right and what was
  missed, recommend one of the four buttons, and let the user choose
  (`decisions.md` §1).

## Modes

| Mode | Per note | An answer is |
|---|---|---|
| quick | up to 4 questions | one of up to 4 options, via AskUserQuestion |
| normal (default) | 2–3 questions | a short phrase, 1–3 words; avoid bare yes/no |
| detailed | 1–2 questions | a full sentence |

Mode sets the effort answering takes, not how hard the question is — though
detailed leaves room for harder ones.

- **Quick:** shuffle the options, and take the wrong ones from the base — a
  neighbouring note's real answer — rather than inventing them.
- **Normal and detailed:** the scope may widen slightly onto adjacent material.

## Procedure

**1. Pick what to quiz.** A topic names the notes; ask which where it matches
several and the user plainly meant one. No topic is a scheduled review — go to
the section below, then return here from step 3.

**2. Gather, per note.** Its prior logs (grep the logs for the note's path — the
same search that finds its cards), its cards, and whatever its `sources` name
that you need in order to grade.

**3. Ask.** All the questions about one note together, then the next note.

**4. Grade each answer** correct / partial / incorrect, and say which was which
once the note's questions are done.

**5. Grade the card.** Offer the four buttons with AskUserQuestion, your
recommendation first, then send what the user picked:

- scheduled review — `grade <ease> <card>`, for the card the reviewer is
  showing, then `next`;
- topic mode — find the note's understanding card and `grade-card <card-id>
  <ease>`. A note without one is quizzed all the same; there is simply nothing
  to send.

**6. Offer another round.** Another round asks what was still missed.

**7. Write the log** where the logs already live — a `quizzes/` directory
where the base has none — one file for the session, per the schema below: `sources`
naming every note quizzed, the body carrying each question, the answer as given,
and its grade. **What was missed is what the log is for** — write the missed
part in full, since next time's quiz opens on it.

**8. Report** the log's path, what was missed, and anything the user said that
belongs in the base — offering `/kb-update` or `/kb-capture` for it, never doing
it silently.

## Scheduled review

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py status    # what is due, and the backup age
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py session   # open the reviewer, report the first card
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py next      # the card showing now
```

`session` is Anki's Study Now button, so every limit and ordering stays the
scheduler's — **never search for due cards instead**. Each card reports the note
it stands for: quiz that note (steps 2–5), then `next`. `card: none` ends the
session. Exit 3 means Anki is not running — offer a topic quiz, and grade
nothing.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
