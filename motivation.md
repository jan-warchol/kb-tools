# Personal learning system — motivation

## 1. Problem

Moving through technical material fast — under work pressure, with AI
assistance — produces understanding at the moment of contact and no retention
afterwards. Reading more does not fix that; scheduled recall can. Note systems
optimise capture because friction is measurable and retention is not, but a
system that never forces re-contact produces an archive, not knowledge.

### 1.1 Two kinds of knowledge, both first-class

**General knowledge** survives changes of project and employer.
**Project-specific knowledge** — which module owns what, where the non-obvious
behaviour lives — is valuable only on that codebase, and expires when the code
changes.

The tempting conclusion is that the second kind is not worth memorising. Wrong:
learning an unfamiliar codebase is a memorisation task — costly to lack, not
reconstructible from first principles, forgotten fast without practice. The mix
will shift, so neither may be the secondary case, which means the system must
own the problem of knowledge going stale.

Project knowledge is worth memorising for the duration of the engagement, not
for ever. That makes **retirement, not revalidation, the right answer for most
of it**: its cards are retired when the project is left, rather than maintained
against a codebase nobody is reading any more. Revalidation is for what
outlives the project. Which of the two an item is needs no label: it is legible
in the sources it was checked against.

### 1.2 Dictation is the input, and dictation is lossy

Knowledge enters by voice; anything with more friction goes unused at the
moment learning happens. Three error classes, not to be handled as one:

1. **Factual.** The user misunderstands and states a falsehood. Most dangerous:
   uncorrected, review would reinforce it until it is reliably remembered —
   worse than no memory, and a stale memory is the same thing on a delay fuse.
   Discovering the error is also the most valuable signal the pipeline
   produces, so a silent repair would spend it.
2. **Transcription.** Casing lost, `camelCase` / `kebab-case`
   indistinguishable by ear, words swapped for similar-sounding ones.
   Recognition predicts from context, so errors land on the terms carrying the
   meaning.
3. **Noise.** Repetition, self-correction, digression. Harmless; cleaned up.

### 1.3 Articulation cannot be delegated

An agent can summarise a codebase better than the user can, but knowledge the
user did not articulate themselves does not become theirs. Encoding happens in
the effort of finding the words, so the raw material has to be the user's own.

Agent-written material is not prohibited in principle, but the line has to be
drawn in the right place. **Claims** — causation, consequence, why, tradeoffs,
what follows from what — must be the user's, always. **Scaffolding** —
identifiers, paths, call order, the topology of a diagram — is transcription of
the source, not composition of knowledge, and an agent supplying it takes
nothing from the user.

So agent material is kept, mechanically separable, and never carded. The route
out of it is not approval: reading a paragraph and agreeing with it is the
illusion of understanding, which is what this section is about. The route is a
question — **the claim the user states in answering is theirs**, whatever
prompted it, and it enters the way any other articulation does.

### 1.4 The corpus drifts toward whatever the trigger catches

Capture fires on stumbling under work pressure, so what accumulates is whatever
was in the way: plumbing. What would have prevented the stumble — the language,
the framework's execution model — is never what one is stuck on, and so is
never captured. The bias is structural, so the system corrects for it rather
than hoping: under most specific stumbles there is a general pattern, and it is
cheapest to name with the instance still on screen.

## 2. Goal

> **Take knowledge the user has articulated themselves, verify it, hold it in a
> durable, structured form, schedule reinforcement, and detect when it has
> stopped being true.**

Five obligations, each load-bearing:

| Obligation | | Failure if absent |
|---|---|---|
| **Articulate** | stated in the user's own words | storage without learning |
| **Verify** | checked against the source before it is kept | memorised falsehoods |
| **Structure** | connected to what is already known | an unnavigable pile |
| **Schedule** | re-presented before it is forgotten | no retention |
| **Revalidate** | rechecked as the subject changes | falsehoods on a delay fuse |

**Success criterion.** The user can answer questions about things they learned
several months earlier, understands a codebase they no longer actively develop,
is not drilled on anything that has become false — and is still using the
system, because it never demanded more of a week than was in it.

**Durability.** The knowledge must outlive this project's code, so it lives in
plain files readable without it.

**Scope.** Recall — knowing without lookup — is the purpose; lookup is a
secondary benefit, possibly served in another layer with different rules.
Verification settles whether a claim is true, not whether recalling it is worth
anything; only the user can judge that.

## 3. Influences

[**Karpathy's LLM-wiki pattern**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
— immutable raw sources, derived items maintained on top of them, and a config
document that makes the agent a disciplined maintainer. The architecture is
adopted directly, the config document being the skill files; maintaining
derived material is what humans abandon and agents do not mind. Its authorship
model (the LLM writes, the human curates) is not rejected in principle, but the
focus here is different: the user's own articulation is the point (§1.3).

[**Open Knowledge Format v0.2**](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
— markdown whose YAML frontmatter carries the machine-readable half. Taken
from it: derivation and evidence answer one question and share one field, and
an item is a plain file that reads without the tooling.
