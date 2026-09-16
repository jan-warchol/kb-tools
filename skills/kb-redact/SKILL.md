---
name: kb-redact
description: Turn captures in the knowledge base into short, structured notes. Use when the user wants to redact, process, or work through their capture backlog — "redact", "process a capture", "turn these into notes". Every claim stays the user's; the shape is the agent's. Verifies anything captured unverified, and never marks a note approved without the user's say-so. Does not make cards.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/*), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_find.py *)
---

# kb-redact

One subject, one note, one run. Its captures are the slug pool
(`kb_find.py --pool`); a capture from another subject is another run.

Invoke `/kb-common` skill if you haven't already.

1. **Gather**: the slug pool — human captures, the machine captures beside
   them, any note already made from them. A note exists ⇒ at normal effort edit
   the sections newer captures affect; at thorough, rebuild it from the whole
   pool. Verify what was captured unverified, at the requested effort
   (`/kb-common`).
2. **Claims are theirs, shape is yours.** Every sentence outside a machine
   block must trace to something the user said; reorder and recast freely,
   add or drop a claim never. Where captures disagree, the newer one is the
   current state. A hedge that verification settled goes; a scope
   qualifier ("only when…") stays. A contradiction — within the material or
   against the code — stops you: quote both sides, let the user settle it.
   Their answer is a claim: a new capture, verified on the spot.
3. **Outline first**, except at quick effort. The outline is the note's
   structure, never its content: one line per section, `<heading> —
   <shape> with <what's inside>`, where what's inside is two to five words.
   No claims, identifiers, code or examples; if a line teaches something
   about the subject, it is a draft, not an outline. E.g.
   `Embedding is not subtyping — gotcha with the failed call`.
   Raise any contradiction separately, below the outline. Take the
   correction before filling.
4. **Fill.** Shapes: **flow** (trigger, ordered steps with real identifiers,
   decisions with their conditions, terminal states, the invariant; mermaid
   for topology plus a numbered list for detail), **comparison** (the axis,
   the subjects, the choosing rule), **gotcha** (symptom, the wrong model
   that made it surprising, cause, fix). Plain prose stays legitimate.
   Bullets over prose for lists of facts; code formatting speech could not
   carry. Diagrams and walkthroughs from the machine-origin capture
   go in **machine blocks**; the scaffolding you fill in yourself (paths,
   symbols, topology) too. Never a history of what changed. The note stands on
   its own without the captures.
5. **Present, then on approval write** it under the pool's slug, next free
   number (an existing note keeps its ID): `sources` the captures by
   `kb:<id>` and only evidence you read beyond theirs, `verified` your check,
   `approved` stamped now, `status: stable`. A capture already short enough is
   promoted as-is. Unapproved stays `draft`.
6. Say what you left open (`/kb-common`, Stopping), and run the check.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/core.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/capture.md`

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/schema/note.md`
