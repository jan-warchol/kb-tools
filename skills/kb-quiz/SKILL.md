---
name: kb-quiz
description: Quiz the user on topics from their knowledge base. Use when the user wants to be tested — "quiz me", "test me on X", "quiz me on last week's notes", "quiz me on what changed". Asks about reasoning rather than plain recall, grades understanding cards, and logs the session so the next quiz leads with what was missed.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_anki.py *), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), AskUserQuestion, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-quiz

**No topic → review what Anki says is due. A topic → quiz that topic.**

Invoke `/kb-common` skill if you haven't already.

| Mode | Per note | An answer is |
|---|---|---|
| quick | up to 4 questions | one of up to 4 options, via AskUserQuestion; wrong options are real answers from neighbouring notes |
| normal (default) | 2–3 questions | a short phrase, 1–3 words; no bare yes/no |
| detailed | 1–2 questions | a full sentence |

1. **Pick the notes.** A topic names them (ask where it matches several).
   "What changed" is a topic: notes with a human capture in their slug pool
   newer than their latest quiz log. No
   topic ⇒ scheduled review: `kb_anki.py status`, then `session` (Anki's own
   Study Now — never search for due cards yourself); each card names its
   note; `next` after grading; `card: none` ends it; exit 3 means Anki is not
   running — offer a topic quiz and grade nothing.
2. **Gather per note**: prior logs and cards (`kb_find.py --refs <note id>`),
   the questions suggested in its understanding card, and whatever sources
   you need to grade. Read the code the note cites before judging an answer
   that turns on it. **What changed**: the human captures in its slug pool
   (`kb_find.py --pool`) newer than its latest quiz log — each is a
   correction or addition the user has not been asked about yet.
3. **Write each expected answer first**; if it exceeds the mode's length,
   discard the question. Ask about reasoning — derive, compare, predict, say
   why — never what a card already drills. Lead with what changed, then what
   the logs say was missed or never asked; the suggested questions are a pool
   to draw from, and a machine block is fair game to ask about. Stay on the
   note unless the user asked to widen.
   **Ask all of a note's questions together**, then the next note: in quick
   mode one AskUserQuestion call carrying them all; otherwise one numbered
   list, answered in one go.
4. **Never give the answer away** — not in the question, not in the framing,
   not in options where only one is not absurd.
5. **Repair a spoken answer before judging it** (`/kb-common`), grade correct /
   partial / incorrect against the note and its sources, and say which was
   which once the note is done. Quick mode measures recognition: recommend
   one grade lower than the score suggests.
6. **Propose the grade, never send it unasked**: the four buttons via
   AskUserQuestion, your recommendation first; then `grade <ease> <card>` in a
   scheduled review, or `grade-card <card-id> <ease>` in topic mode (a note
   without an understanding card is quizzed all the same).
7. **Offer another round** on what was still missed.
8. **Write the log** (`quizzes/` where the base has none), one file per
   session: `sources` naming every note by `kb:<id>`, each question, the answer as given,
   its grade, and the missed part in full — next time opens on it.
9. **Anything new the user articulated leaves through the front door**:
   offer `/kb-update` or `/kb-capture`; never append it to a note, a capture
   or the log. Questions worth asking again go the other way — into the
   understanding card's machine block, which you rewrite freely.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/quiz-log.md`
