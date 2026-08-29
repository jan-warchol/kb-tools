# Personal learning system — motivation

## 1. Problem

Moving through technical material fast — under work pressure, with AI assistance
— produces understanding at the moment of contact and no retention afterwards.
Reading more does not fix that; scheduled recall can. Note systems optimise
capture because friction is measurable and retention is not, but a system that
never forces re-contact produces an archive, not knowledge.

### 1.1 Two kinds of knowledge, both first-class

- **General knowledge** survives changes of project and employer.
- **Project-specific knowledge** — which module owns what, where the non-obvious
  behaviour lives — is valuable only on that codebase, and expires when the code
  changes.

The tempting conclusion is that the second kind is not worth memorising. Wrong:
learning an unfamiliar codebase is a memorisation task — costly to lack, not
reconstructible from first principles, forgotten fast without practice. The mix
will shift, so neither may be the secondary case — which means the system must
own the problem of knowledge going stale.

### 1.2 Dictation is the input, and dictation is lossy

Knowledge enters by voice; anything with more friction goes unused at the moment
learning happens. Three error classes, not to be handled as one:

1. **Factual.** The user misunderstands or misremembers and states a falsehood.
   Most dangerous: if not corrected, review would reinforce it until it is
   reliably remembered — worse than no memory. A stale memory is the same thing
   on a delay fuse. However, discovering the error is the most valuable signal
   the pipeline produces — a silent repair would spend it.
2. **Transcription.** Casing lost, `camelCase` / `kebab-case` indistinguishable
   by ear, words swapped for similar-sounding ones. Recognition predicts from
   context, so errors land on the terms carrying the meaning.
3. **Noise.** Repetition, self-correction, digression. Harmless; must be cleaned
   up.

### 1.3 Articulation cannot be delegated

An agent can summarise a codebase better than the user can, but knowledge the
user did not articulate themselves does not become theirs. Encoding happens in
the effort of finding the words, so the raw material has to be the user's own.

Agent-written material is not prohibited in principle: the requirement is to
keep it mechanically separable from the user's claims and never compose
knowledge in the user's place.

## 2. Goal

> **Take knowledge the user has articulated themselves, verify it, hold it in a
> durable, structured form, schedule it for recall, and detect when it has
> stopped being true.**

Five obligations, each load-bearing:

| Obligation | | Failure if absent |
|---|---|---|
| **Articulate** | stated in the user's own words | storage without learning |
| **Verify** | checked against the source before it is kept | memorised falsehoods |
| **Structure** | connected to what is already known | an unnavigable pile |
| **Schedule** | re-presented before it is forgotten | ordinary note-taking |
| **Revalidate** | rechecked as the subject changes | falsehoods on a delay fuse |

**Success criterion.** The user can answer questions about things they learned
several months earlier, understands a codebase they no longer actively develop,
and is not drilled on anything that has become false.

**Durability.** The knowledge must outlive this project's code, so it lives in
plain files readable without it.

**Scope.** Recall — knowing without lookup — is the purpose; lookup is a
secondary benefit, possibly served in another layer with different rules.
Verification settles whether a claim is true, not whether recalling it is worth
anything — only the user can judge that.

## 3. Influences

[**Karpathy's LLM-wiki pattern**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
— immutable raw sources, an LLM-maintained wiki derived from them, and a config
document that makes the agent a disciplined maintainer.

- **The architecture is adopted directly:** immutable raw material, derived
  items maintained on top of it, and a config document — here, the skill files —
  that makes the agent a disciplined maintainer. Maintaining derived material is
  what humans abandon and agents do not mind.
- **Its authorship model is not rejected in principle.** The LLM writes and the
  human curates — likely to be used for external sources, plausibly in this
  same repository.
- **The focus of the learning part is different:** here, the user's own
  articulation is critical (§1.3).

[**Open Knowledge Format v0.2**](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
— markdown files whose YAML frontmatter carries the machine-readable half: what
links to what, and the fields automated passes read and write:

- The knowledge base is an OKF bundle, so a leading `/` in a reference is
  base-relative, and derivation and evidence share one field because both
  answer "where did this come from".
- `generated` / `verified` already spells the who-wrote / who-confirmed split.
- The `human:` actor prefix marks sign-off by a person, not a machine.
