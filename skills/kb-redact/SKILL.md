---
name: kb-redact
description: Turn captures in the knowledge base into short, structured notes. Use when the user wants to redact, process, or work through their capture backlog — "redact", "process a capture", "turn these into notes". Every claim stays the user's; the shape is the agent's. Verifies anything captured unverified, and never marks a note approved without the user's say-so. Does not make cards.
allowed-tools: Read, Write, Glob, Grep, Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *), Bash(cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md), Bash(date -u *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_check.py *)
---

# kb-redact

One subject, one note. Usually one capture in; several where they are about
the same thing, each cited.

Invoke `/kb-common` skill if you haven't already.

!`${CLAUDE_PLUGIN_ROOT}/scripts/kb_bearings.sh`

1. **Gather**: the capture(s), the machine-origin captures beside them, any
   note already on the subject. Verify what was captured unverified, at the
   requested effort (`/kb-common`).
2. **Claims are theirs, shape is yours.** Every sentence outside a machine
   block must trace to something the user said; reorder and recast freely,
   add or drop a claim never. A hedge that verification settled goes; a scope
   qualifier ("only when…") stays. A contradiction — within the material or
   against the code — stops you: quote both sides, let the user settle it.
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
   symbols, topology) too. The note stands on its own without the capture.
5. **Record what you left open** — unchecked claims, follow-ups, patterns you
   noticed — under `## Open / follow-ups` in the machine-origin capture, never
   in the note (`/kb-common`).
6. **Present, then on approval write** it under the capture's slug, next free
   number: `verified` from the captures plus yours, `approved` stamped now,
   `status: stable`. A capture already short enough is promoted as-is.
   Unapproved stays `draft`.
7. Run the check.

---

# Schema

!`cat ${CLAUDE_PLUGIN_ROOT}/reference/frontmatter.md`
