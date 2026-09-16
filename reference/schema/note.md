# Note

The current state of one subject. Slug of its captures, next free number.
`generated.by` the agent, `origin: human`: **every sentence outside a machine
block traces to a human capture**. Sources: the captures and notes it draws
on, then only evidence it was itself checked against beyond them — never
their evidence copied. `verified` is the agent's latest check; `approved` is
what `status: stable` waits on. A note does not list its cards or its history
— `kb_find.py --refs` finds the cards, the slug pool holds the history.

A note with `origin: machine` is reference only, never carded.

```yaml
---
id: retry-wrapper_3
type: Note
title: Retry wrapper ordering
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:41:00Z }
status: stable
sources:
  - resource: kb:retry-wrapper_1
  - resource: kb:retry-wrapper_2
verified: { by: claude-code/opus-5, at: 2026-08-10T14:41:00Z }
approved: { by: human:jan, at: 2026-08-10T14:41:00Z }
---
```
