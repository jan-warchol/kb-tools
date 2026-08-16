---
name: kb-ingest
description: Transcribe an external source — an article, paper, doc page or local file — into the knowledge base as clean markdown, plus a summary one tenth its length. Use when the user points at a URL or a file and wants to keep it — "ingest this", "save this article", "summarise this for the kb". Writes two documents and never mixes its own claims into either.
allowed-tools: Read, Write, Glob, WebFetch, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(wc -w *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-ingest

Writes **two files**: a faithful markdown transcription of an external source,
and a summary of it. Both carry the *source's* claims, never yours and never the
user's.

## Bearings

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

Both files go where the bearings show ingested sources live. Never copy an actor
or a timestamp out of an example.

## Rules

- **Transcribe, don't rewrite.** The transcription carries the source's own
  words, structure and headings. Strip the packaging — navigation, cookie
  banners, share buttons, newsletter prompts, related-article rails, comments —
  and nothing else. Never condense, reorder or improve the prose.
- **Your voice appears nowhere.** No commentary, no corrections, no "note that
  this is outdated" in either file. If the source is wrong, it is still what the
  source says. Say it in your report instead.
- **The summary is a summary.** Only what the source claims, at a tenth the
  length. No conclusions the source did not draw.
- **This is reference material, not knowledge the user holds.** Both files are
  `origin: machine`, and nothing here becomes a card — that route runs through
  the user dictating it themselves.

## Procedure

**1. Get the source.** If what comes back looks summarised, truncated or
paywalled, say so and ask before writing — a partial transcription that looks
complete is the failure mode worth avoiding.

**2. Transcribe** into markdown. Keep images that carry meaning (diagrams,
screenshots, charts) pointing at their original absolute URLs; drop decorative
and tracking ones. Keep links inline, absolutised.

**3. Summarise** the transcription — the most important points, in the source's
order, targeting **10% of its word count**, ±20%. Structural markdown over
prose: a short lead sentence, then bullets. Anything the source's argument turns
on belongs here; examples, restatements and asides do not.

```bash
wc -w <the transcription you wrote>
```

**4. Write both files**, per the schema below. The `verified` entry you stamp on
each means **the text is faithful to the source** — not that the source is
correct. You are in no position to assert the latter and must not imply it.

Then, optionally, check the frontmatter — it catches mechanical mistakes, and a
skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the two files you wrote>
```

**5. Report** both paths, the two word counts and the ratio, and anything you
had to leave out or could not fetch.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
