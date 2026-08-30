# WIP: regrouping the instructions

Relocation only. Every block is byte-identical to where it came from — nothing
merged, nothing reworded, duplicates left standing so they can be seen. Group
headings are the only new text. `instructions/` is a placeholder location, not a
proposal.

`kb-common` is now a wrapper that injects all four files, so what every skill
sees is unchanged from `c502028`.

## What moved

| Group | From `kb-common` | From `reference/frontmatter.md` |
|---|---|---|
| `articulation.md` | "only add new information when the user explicitly articulated it" | — |
| `lifecycle.md` | the pipeline diagram; stale claims; append-don't-edit; update downstream; "an unverified note is not allowed to produce cards" | "the **first** source of a derived item…"; "a note must be machine-confirmed or better…" |
| `verification.md` | the whole `## Verification` section; the actor/timestamp rule; "don't say the correct answer" | — |
| `mechanics.md` | source-code references; slug choice; the two bearings rules; `## After writing` | "Draw it with `kb_cardid.sh`…"; "Frontmatter is authoritative…" |

## Left where it was, and why

**Mixed paragraphs in `reference/frontmatter.md`** — instruction and schema in
one breath, so splitting them means rewriting them:

- the `origin` paragraph ("says **whose claims these are**, and is never
  inferred") — belongs to `articulation.md` but defines a field
- "A note does not list its cards…" — mid-paragraph inside the **Note** kind
- "`sources` are notes only, never a repository or a document" — mid-paragraph
  inside the **Card** kind
- "A repository is named by URL, never by a local path…" — the rule and its
  rationale in one paragraph
- "**Unverified means draft**, for everything…" — starts as a rule and turns
  into an account of what `kb_check.py` does

One artefact from cutting mid-paragraph: `mechanics.md` opens its card-ID block
with "Draw it with…", whose antecedent stayed behind in the schema. A `## Card
IDs` heading stands in for now.

**Skill-local instructions**, not moved because moving them would apply them to
every skill. Candidates for each group, if the grouping is meant to be complete:

| Group | Candidates |
|---|---|
| `articulation.md` | kb-capture "never write a capture from the session transcript…", "transcribing, not summarising"; kb-ingest "your voice appears nowhere", "this is reference material, not knowledge the user holds"; `external-sources.md` §4 |
| `verification.md` | kb-capture "transcription repair is the one exception", the whole "Capturing without verification" section; kb-redact "verify, if capture did not"; kb-ingest "the `verified` entry you stamp… means the text is faithful"; kb-quiz "verify what you append"; kb-cards "the user approves each card" |
| `lifecycle.md` | kb-cards step 1 "Eligible: `origin: human`, has `verified`, `status: stable`" (a third statement of the gate already in this group twice), "the note is not touched"; kb-redact "one raw item, one note"; kb-quiz "appending puts the raw item ahead of its note" |
| correcting the user | kb-quiz "be careful not to give away the answers in the questions" |

## Visible once grouped

- **`lifecycle.md` states the cards gate twice** — "an unverified note is not
  allowed to produce cards" and "a note must be machine-confirmed or better *and*
  out of `status: draft`" — and `kb-cards` step 1 states it a third time. The
  second is the precise one; the first omits the `status` half.
- **`verification.md` holds both sides of the correction question.** "Say what
  is wrong and let the user state the correction" sits six lines above "don't say
  the correct answer… don't make the answer inferable from the pointer."
- **`mechanics.md` is the leftovers pile** — naming, card IDs, a frontmatter
  policy, bearings, and a script invocation. If a group is going to fail to
  justify itself, it is this one.
- **`articulation.md` is one bullet** — the thesis of `motivation.md` §1.3 is
  three sentences long, while everything enforcing it sits in the skills.
