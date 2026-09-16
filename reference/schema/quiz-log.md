# Quiz Log

What `/kb-quiz` asked, the answers as given, and the grades. `origin: machine`
— the grading is the agent's. Written once, never revised; anything the user
said worth keeping leaves through `/kb-capture` or `/kb-update`.

`sources` lists every note quizzed, by `kb:<id>` — that is how the next quiz
finds it. ID: the note's slug, next free number, for one note; `quiz-<date>_1`
for several.

```yaml
---
id: retry-wrapper_4
type: Quiz Log
title: Quiz — retry wrapper ordering
origin: machine
generated: { by: claude-code/opus-5, at: 2026-08-14T09:20:00Z }
verified: { by: claude-code/opus-5, at: 2026-08-14T09:20:00Z }
status: stable
sources:
  - resource: kb:retry-wrapper_3
---

## Retry wrapper ordering

**Q.** A message fails after the wrapper has run. What is in the queue?
**A.** "a copy of it, re-enqueued" — correct
**Q.** Why does the ack not wait for the retry to succeed?
**A.** "so the consumer doesn't block" — partial: missed that the broker would
redeliver it.
```
