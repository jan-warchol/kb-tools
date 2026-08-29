---
name: kb-ingest
description: Transcribe an external source — an article, paper, doc page or local file — into the knowledge base as clean markdown, plus a summary of it. Use when the user points at a URL or a file and wants to keep it — "ingest this", "save this article", "summarise this for the kb". Never mixes its own claims into what it writes; falls back to a comprehensive summary alone when the source cannot be retrieved in full.
allowed-tools: Read, Write, Glob, WebFetch, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter-sources.md), Bash(wc -w *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-ingest

Writes a faithful markdown transcription of an external source and a summary of
it — **two files normally, one when the source cannot be had in full**. What it
writes carries the *source's* claims, never yours and never the user's.

## Bearings

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

Both files go where the bearings show ingested sources live. Never copy an
actor or a timestamp out of an example.

## Rules

- **Transcribe, don't rewrite.** The transcription carries the source's own
  words, structure and headings. Strip the packaging — navigation, cookie
  banners, share buttons, newsletter prompts, related-article rails, comments —
  and nothing else. Never condense, reorder or improve the prose.
- **Your voice appears nowhere.** No commentary, no corrections, no "note that
  this is outdated" in anything you write. If the source is wrong, it is still
  what the source says. Say it in your report instead.
- **The summary is a summary.** Only what the source claims, and no conclusions
  the source did not draw. A tenth the length when there is a transcription
  behind it; comprehensive when there is not (step 4).
- **This is reference material, not knowledge the user holds.** Everything
  written here is `origin: machine`, and none of it becomes a card — that route
  runs through the user dictating it themselves.

## Procedure

**1. Get the source.** If what comes back is summarised, truncated or paywalled,
you cannot transcribe it — go to step 4. A partial transcription that looks
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

**4. When the source cannot be transcribed in full**, write the summary alone
and **make it comprehensive** — no length target applies, because the ratio
exists to keep a summary proportionate to a transcription that in this case does
not exist. Carry over everything you did get: every claim, every distinction,
every number, in the source's order. This file is all that will remain of the
source, so err heavily towards keeping.

It cites the original directly, having no transcription to cite. Say in the
file's own words nothing about the gap — your voice still appears nowhere — but
record what was unavailable in your report, and say plainly that the summary
rests on a partial reading.

**5. Write the file or files**, per the schema below. The `verified` entry you
stamp on each means **the text is faithful to what the source said** — not that
the source is correct. You are in no position to assert the latter and must not
imply it.

Then, optionally, check the frontmatter — it catches mechanical mistakes, and a
skip when PyYAML is missing is not a failure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py <the files you wrote>
```

**6. Report** every path written, the word counts and the ratio where there is a
transcription to compare against, and anything you had to leave out or could not
fetch.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter-sources.md`
