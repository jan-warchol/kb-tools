---
name: kb-redact
description: Turn captures in the knowledge base into short, structured notes, and carry a change out to the note's cards. Use when the user wants to redact or process their capture backlog — "redact", "process a capture", "turn these into notes" — or to bring a note to the current state after a correction was captured, or to apply a scaffolding change across a note and its cards (a URL, a renamed identifier, a redrawn diagram), including applying a verify report. Every claim stays the user's; the shape is the agent's. Verifies anything captured unverified, and never confirms a note without the user's say-so. Does not make new cards.
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_export.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-redact

One subject, one note, one run. Its captures are the slug pool
(`kb_find.py --pool`); a capture from another subject is another run.

Invoke `/kb-common` skill if you haven't already.

1. **Gather**: the slug pool — human captures, the agent captures beside them,
   any note already made from them, and that note's cards (`--refs`). A note
   exists ⇒ at normal effort edit the sections newer captures affect; at
   thorough, rebuild it from the whole pool. Verify what was captured
   unverified, at the requested effort. **A claim dictated to you here is not
   redaction**: it is a capture first (`/kb-capture`), and reaches the note
   only from there.
2. **Claims are theirs, shape is yours.** Every sentence outside an agent block
   must trace to something the user said; reorder and recast freely, add or
   drop a claim never. Where captures disagree, the newer one is the current
   state. A hedge that verification settled goes; a scope qualifier ("only
   when…") stays. A contradiction — within the material or against the code —
   stops you: quote both sides, let the user settle it. Their answer is a
   claim: a new capture, verified on the spot.
3. **Outline first**, except at quick effort. The outline is the note's
   structure, never its content: one line per section, `<heading> — <shape>
   with <what's inside>`, where what's inside is two to five words. No claims,
   identifiers, code or examples; if a line teaches something about the
   subject, it is a draft, not an outline. E.g. `Embedding is not subtyping —
   gotcha with the failed call`. Raise any contradiction separately, below the
   outline, and take the correction before filling.
4. **Fill.** Shapes: **flow** (trigger, ordered steps with real identifiers,
   decisions with their conditions, terminal states, the invariant; mermaid for
   topology plus a numbered list for detail), **comparison** (the axis, the
   subjects, the choosing rule), **gotcha** (symptom, the wrong model that made
   it surprising, cause, fix). Plain prose stays legitimate. Bullets over prose
   for lists of facts; code formatting where speech could not carry it.
   Diagrams and walkthroughs from an agent capture go in **agent blocks**, and
   so does the scaffolding you fill in yourself. Never a history of what
   changed. The note stands on its own without the captures; re-read it whole —
   one document written today, or a document with a postscript?
5. **Carry it to the cards** (`--refs`): reword freely, keeping the ID; one the
   note no longer supports is `status: retired` on the user's say-so. New cards
   are `/kb-cards`. **A scaffolding fix alone** — a URL, a path, a renamed
   identifier — is this step and nothing else: no capture, no status change,
   `date` untouched.
6. **Present, then on approval write** the note under the pool's slug, next
   free number (an existing note keeps its ID): `from` the captures by
   `kb:<id>`, `code` and `paths` only for evidence you read beyond theirs,
   `status: confirmed`. A capture already short enough is promoted as-is.
   Unapproved stays `draft`.
7. Run the check, then the export if a card changed, and say what you left open
   (`/kb-common`).

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema.md`
