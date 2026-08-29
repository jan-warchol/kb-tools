# External source kinds

An extension of [`frontmatter.md`](frontmatter.md), covering the two kinds
`/kb-ingest` writes. `/kb-init` appends it to `SCHEMA.md`; everything else in
this file follows the common format described there.

The whole of the external-source capability is separable — see
[`external-sources.md`](../external-sources.md).

## Identity

| Kind | ID form | Example |
|---|---|---|
| source transcript | `<YYYY-MM-DD>-<slug>` | `2026-08-16-cap-theorem` |
| source summary | `<slug-id>-summary` | `2026-08-16-cap-theorem-summary` |

The `type` is `Source Transcript` or `Source Summary`.

## `verified`

On an ingested source the entry means the text is faithful to the original, not
that the original is correct.

## `sources`

The transcript cites the original; the summary cites the transcript first, then
the original, so it stays traceable on its own — a summary is a derived item,
and the first source of a derived item is what it came from. A summary written
where no transcription was possible has nothing internal to cite, and names the
original directly.

## Example

**Source transcript and summary** — both `origin: machine`, because the claims
are the publication's and not the user's.

```yaml
---
id: 2026-08-16-cap-theorem
type: Source Transcript
title: CAP theorem revisited
origin: machine
generated: { by: claude-code/opus-5, at: 2026-08-16T09:12:00Z }
status: stable
sources:
  - resource: https://codahale.com/you-cant-sacrifice-partition-tolerance/
    author: human:codahale
    retrieved: 2026-08-16
verified:
  - { by: claude-code/opus-5, at: 2026-08-16T09:12:00Z }
---
```
