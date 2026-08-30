---
name: kb-quiz
description: Quiz the user on topics from their knowledge base. Use when the user wants to be tested — "quiz me", "test me on X", "quiz me on last week's notes". Asks about reasoning and understanding rather than plain recall, captures anything new the user says, and logs the session.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-quiz

Asks about material the user already holds, to find the edges of it. Plain
recall is what cards are for; this is for reasoning and understanding.

## Bearings

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

No knowledge base means nothing to quiz on: say so and offer `/kb-init`.

## Rules

- **Never give the answer away** — not in the question, and not by framing it so
  the answer is inferable. This applies to a wrong answer too: point at what is
  wrong and let the user reach the correction themselves (`/kb-common`).
- **What the user says in an answer is theirs, and is the only thing worth
  keeping.** Nothing you know goes into the base because it came up here.
- **You are not grading.** Nothing in this system checks answers; say where an
  answer was thin and move on.

## Procedure

**1. Pick the material.** The notes the user named, else the ones they have not
been asked about recently. Read each note, and read the previous quiz logs for
it if there are any — ask about what was missed last time or not covered at all.

**2. Gather context.** Follow `sources` in the frontmatter to whatever the note
was verified against. With the source in front of you the questions can range a
little wider than the note, into adjacent behaviour the user plausibly met at
the same time.

**3. Ask.** One or two questions per note, no more. Each should be answerable in
a few sentences — if it needs an essay, it is the wrong question. Skip anything
already covered by a card on that note: those are drilled elsewhere, and asking
again here primes them.

**4. Keep what is new.** Where an answer contains something the note does not
already say, that is dictation and belongs in the base — verify it per
`/kb-common`, then append it to the raw item behind the note, leaving what is
already written alone.

If you cannot verify it now, do not append it: an unverified sentence inside a
verified item makes the whole item's `verified` entry a lie. Say so, and offer
`/kb-capture` for it instead.

Appending puts the raw item ahead of its note, and the note ahead of its cards.
Say which ones now trail and offer `/kb-redact`; do not quietly rewrite them.

**5. Log the session** where the previous logs live — the questions, the
answers, and what was thin or wrong about them, so the next quiz can start where
this one stopped. The log is a record of an exchange and not a knowledge item:
plain markdown, no frontmatter, nothing downstream reads it.

**6. Report** what was covered, what the user was shaky on, anything appended,
and anything left uncaptured for `/kb-capture`.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
