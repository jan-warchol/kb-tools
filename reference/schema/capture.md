# Capture

The raw layer: a record of one session. `origin` separates the two cases; they
are one kind.

**Open during the session that wrote it, closed after — both origins.** Open:
added to and reworded in place, changed claims verified again, `generated.at`
moved. Closed: never edited again; anything later about the subject is a new
capture, same slug, next free number. If you are not certain this conversation
wrote the file, it is closed. A superseded capture is left as it is — the note
carries the current state.

**One author per capture.** Mixed authorship is two captures.

## Dictated — `origin: human`

The user's words, transcription repaired; `generated.by` the user, `verified`
the agent. Sources: evidence only.

```yaml
---
id: retry-wrapper_1
type: Capture
title: Retry wrapper ordering
origin: human
generated: { by: human:jan, at: 2026-08-10T14:32:00Z }
verified: { by: claude-code/opus-5, at: 2026-08-10T14:35:00Z }
status: stable
sources:
  - resource: https://github.com/acme/backend
    path: src/queue/retry.py
    symbol: RetryWrapper
    commit: a1b2c3d
---

`RetryWrapper` is applied inside `Consumer.handle`, so the message is acked
first and the retry re-enqueues it rather than holding it.
```

## Written by the agent — `origin: machine`

The agent's material: a diagram, a walkthrough, a trace summary, a verify
report. **A record, not a worklist** — nothing in it is meant to be crossed
off. Never approved, carded, or redacted as the user's words; `/kb-redact`
mines it for scaffolding. Sources: the item it concerns, then evidence.

```yaml
---
id: retry-wrapper_2
type: Capture
title: Retry wrapper — consumer flow
origin: machine
generated: { by: claude-code/opus-5, at: 2026-08-10T14:40:00Z }
verified: { by: claude-code/opus-5, at: 2026-08-10T14:40:00Z }
status: stable
sources:
  - resource: kb:retry-wrapper_1
  - resource: https://github.com/acme/backend
    paths: [src/queue/retry.py, src/queue/consumer.py]
    commit: a1b2c3d
---
```

**A verify report** (`/kb-verify`) is a machine capture whose first source is
the note it checked, with two sections and nothing else:

```markdown
## Scaffolding that moved

- `fetchState` → `loadState`, `src/state/load.go`

## Claims affected

- "The value is fetched on demand." — `Sync.push` now stores it; the fetch is
  only called from `repair`.
```

Older captures may end in `## Open / follow-ups`: history, not read.
