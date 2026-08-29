# Personal learning system — external sources

Ingest keeps external material — an article, a paper, a doc page, a local file —
as reference beside the user's own knowledge. It is specified here rather than
apart from the rest so that it can be lifted out whole.

**The capability lives in three files and nothing else:**

- this one,
- [`skills/kb-ingest/SKILL.md`](skills/kb-ingest/SKILL.md) — the skill,
- [`reference/frontmatter-sources.md`](reference/frontmatter-sources.md) — the
  two item kinds it writes, appended to `SCHEMA.md` by `/kb-init`.

Four one-line residues sit outside them and are named at the end of this file.

## 1. Scope

| Operation | What it does |
|---|---|
| **Ingest** | Transcribe an external source and summarise it, as reference material |

## 2. Flow

```
  external source
        │
        ▼  ingest ······· transcribes faithfully
     source               summarises at a tenth
        │
        ╎  reference only — the claims are the source's, so nothing here
        ╎  becomes a card without passing through dictation first
        ╎
        ╰┄┄▶ dictation ──▶ capture ──▶ … (the pipeline every item takes)
```

## 3. Why the material is segregated

Ingest exists to keep reading, not to shortcut articulation. Its two files are
`origin: machine` throughout, and their `verified` entry asserts only that **the
text is faithful to the source** — never that the source is right.

That is the whole of the segregation the design depends on: external material is
readable, citable and searchable alongside the user's own, and mechanically
distinguishable from it by one field. A card drawn straight from an ingested
source would be knowledge the user never articulated, so the route from a source
to a card runs through dictation like everything else.

This is the `machine` half of `origin` (`reference/frontmatter.md`) put to
work: the agent wrote nothing of its own, and the item is still
`origin: machine`, because the claims are the publication's.

## 4. Constraints

- It will not add its own voice to an ingested source, in either file.

## 5. Use

```
/kb-ingest <url-or-path>
```

Keeps an external source: a faithful transcription plus a summary a tenth as
long. Both are marked as the source's claims, not the user's — it is reference
material, and the way something becomes a card is still the user saying it in
their own words.

## 6. Deferred

| Deferred | Why not now | Revisit when |
|---|---|---|
| **Cards drawn from ingested sources** | Ingest keeps external material as reference. A card made straight from it would be knowledge the user never articulated, so today the route runs through dictation. Relaxing that needs the `origin` split to have proven itself in daily use, not merely to be recorded | Reading is a major input channel and the provenance split has held up |

## 7. Attaching and detaching

Nothing outside these three files names this capability, so removing it is
deleting them. `/kb-init` assembles `SCHEMA.md` from `reference/frontmatter.md`
plus every `reference/frontmatter-*.md` fragment beside it, so the fragment's
absence is already handled and the script needs no edit.

Two consequences worth knowing when this moves:

- **The plugin manifests do not mention ingest.** `.claude-plugin/plugin.json`
  and `marketplace.json` describe the core pipeline only, so a project taking
  this capability on adds the clause itself.
- **`/kb-init` lays out no directory for ingested files.** The skill reads the
  base and writes each file where that kind already lives, asking when nothing
  fits (`scripts/kb_bearings.sh`). A base that wants a fixed home for them gets
  one by hand — conventionally `sources/`.

One incidental mention survives elsewhere and is deliberately left. The Karpathy
authorship-model bullet in `motivation.md` §3 says the LLM-writes/human-curates
model is "likely to be used for external sources"; that is a remark about where
that model belongs, not about this capability, and reads correctly either way.
