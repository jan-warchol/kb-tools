# Cards

A card kind is a `type` ending in `Card` — export dispatches on that, and
names the deck after what precedes it. Two kinds: `Recall Card`,
`Understanding Card`.

- **Sources**: the note or capture it is drawn from, by `kb:<id>` — never
  evidence directly.
- Drawn only from an approved, human-origin item, never from inside a machine
  block.
- `title` names what it asks about, not the question.
- `approved` is what export reads; a card carries no `verified`.
- `importance`: `core` | `extra`. Absent ⇒ held back from export until graded
  (`/kb-export`). It sets the **initial** deck only; moving a card later
  happens in Anki, and the two drifting apart is expected.
- `status: deprecated` ⇒ suspend it in Anki; never delete.
- The ID is permanent: rewording keeps it, asking something else takes a new
  one. Exported cards carry the tag `kb::<id>`.

## Recall Card

One fact, one answer. Body `## Question` and `## Answer`.

```yaml
---
id: Xo1jycAlN4xQ
type: Recall Card
title: Ack ordering on retry
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:42:00Z }
status: stable
importance: core
sources: [{ resource: kb:retry-wrapper_3 }]
approved: { by: human:jan, at: 2026-08-10T14:43:00Z }
---

## Question

In what order do the ack and the retry happen for a failed message?

## Answer

Ack first — the retry re-enqueues the message rather than holding it.
```

## Understanding Card

Whether the user can reason with a note, self-graded in Anki: the front asks
for the note from memory, the back names the note to check against. **The card
is the note**: at most one per note, no question of its own, no body, both
Anki fields generated at export.

```yaml
---
id: 7bQr2mKp9xLd
type: Understanding Card
title: Retry wrapper ordering
origin: human
generated: { by: claude-code/opus-5, at: 2026-08-10T14:42:00Z }
status: stable
importance: core
sources: [{ resource: kb:retry-wrapper_3 }]
approved: { by: human:jan, at: 2026-08-10T14:43:00Z }
---
```
