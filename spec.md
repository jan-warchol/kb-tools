# Personal learning system — specification

## 1. Scope

### 1.1 Operations

| Operation | What it does |
|---|---|
| **Capture** | Accept dictation, repair transcription, verify claims, store raw |
| **Redact** | Turn raw material into a polished, structured, provenance-carrying note |
| **Ingest** | Transcribe an external source and summarise it, as reference material |
| **Card** | Propose recall items; the user approves them |
| **Export** | Emit an importable package for the scheduler |

Lookup is not a built operation — asking an agent inside the knowledge base is
sufficient and requires no dedicated mechanism.

### 1.2 Boundary

The system owns everything from the spoken sentence to the moment a card is
handed to the scheduler. It does not own scheduling and does not implement a
review interface. Noticing when what it holds has stopped being true is inside
that boundary.

**Nothing anywhere checks answers.** The scheduler does not grade — it consumes a
grade the human produces, for every card type, and there is no correctness
checking to hook into at any point in the pipeline. That is why a deep card's
rubric must be checkable by the person reciting it (§3.5).

## 2. Flow

```
  dictation                          external source
     │                                     │
     ▼  capture ······· verifies           ▼  ingest ······· transcribes faithfully
   raw                  against repos    source            summarises at a tenth
     │                  and sources         │
     ▼  redact ········ polishes one item   ╎  reference only — the claims are the
   note                 never reorganises   ╎  source's, so nothing here becomes a
     │                  the corpus          ╎  card without passing through
     ▼  card ·········· system proposes,    ╎  dictation first
   card                 user approves ······╯
     │
     ▼  export
  package ─────────────▶ scheduler          (review happens here, not here)
```

Raw material holds the user's words and is normally left as written. A note holds the user's
claims, approved, carrying provenance. A card has stable identity and references
its notes.

## 3. Data structures

**The format itself is specified once**, in
[`reference/frontmatter.md`](reference/frontmatter.md) — every key, the three
verification tiers, and one worked example per layer. The skills inject that
file rather than restating it, and `/kb-init` copies it into the knowledge base
as `SCHEMA.md` so the base is readable without this plugin. This section holds
only what the reference cannot: why the fields are shaped that way.

`kb_check.py` checks the *shape* of frontmatter and nothing else — keys that
must be present, values that must parse, and the rule that anything unverified
is `status: draft`. It knows no item kinds and no directory names, because both
are meant to change without a release; OKF leaves `type` open and so does this.
Everything about meaning stays with the reader.

### 3.1 Identity

Card IDs are permanent: the scheduler's identity derives from them, so reusing
one silently overwrites a card's history and changing one resets it to zero.

**The rule for editing a card:** improving the wording keeps the ID; changing
what the card *asks* takes a new ID, because the accumulated review history
describes the old question and resetting is correct.

Cards belonging to a note are found by globbing `<note-id>-c*`, not by living in
one file — which keeps per-card metadata (status, approval) natural. The glob is
anchored on the `-c` because IDs colliding within a layer take a numeric suffix,
and an unanchored prefix would sweep in a longer note's cards.

### 3.2 Provenance

`origin` says **whose claims these are** — the one field that must never be
inferred. `human` means the content asserts what the user asserted; `machine`
means it does not. This is deliberately a different question from
`generated.by`, which records who produced the *text*: a polished note is
written by the agent and still carries `origin: human`, because the claims in it
are the user's. An ingested source is the mirror image — the agent wrote nothing
of its own, and it is still `origin: machine`, because the claims are the
publication's.

`verified` is kept separate from `generated` because whoever wrote something
need not be whoever checked it, and the three tiers that follow from it (OKF
§5.3) are what gate the pipeline: a note must be machine-confirmed or better,
and out of draft, before it can produce cards, and a card must be
human-reviewed, because that entry *is* the user's approval.

### 3.3 Raw items

Normally left as written once a capture ends: a raw item is the record of what
the user said, so the usual way to correct one is a new capture rather than an
edit. This is a default, not a prohibition — a user who asks for a raw item to be
changed or removed gets it changed or removed. Transcription is repaired
silently, and a correction the user dictates while the capture is still open is
folded into the text — a raw item holds the user's words, not the exchange that
produced them.

An unverified capture carries no `verified` key and `status: draft`, and cannot
produce cards.

### 3.4 Notes

`sources` is a list from the outset, holding both where the note came from and
what its claims were checked against. `cards` is derived and regenerated on
export; the authoritative direction is card → note.

A note may be written before the user has seen it, but it stays `status: draft`
and carries no `human:` entry until they approve it — approval is what stamps
that entry and moves it to `stable`.

### 3.5 Cards

A card's `sources` are notes only — never a repository or a document directly. A
card is a question about a note, and everything about where the underlying claim
came from is already recorded there.

**Quick Card** is one fact, one answer. **Deep Card** asks for an explanation,
and its answer is a bullet rubric of 3–6 checkable points used for
self-grading. A deep card is justified only when the answer has structure —
causation, ordering, a tradeoff. If the bullets could be shuffled without loss
it is a list, not a concept, and should be quick cards or nothing.

**A rubric is grading criteria, not a decomposition.** The bullets say what a
good answer observably contains. Expanding them into *n* quick cards deletes
exactly what the card tests: selecting what is relevant without being told,
relations between facts, and reconstructing a forgotten piece from the others.

### 3.6 Ingested sources

Ingest exists to keep reading, not to shortcut articulation. Its two files are
`origin: machine` throughout, and their `verified` entry asserts only that **the
text is faithful to the source** — never that the source is right.

That is the whole of the segregation the design depends on: external material is
readable, citable and searchable alongside the user's own, and mechanically
distinguishable from it by one field. A card drawn straight from an ingested
source would be knowledge the user never articulated, so the route from a source
to a card runs through dictation like everything else.

### 3.7 Sources

**The knowledge base is an OKF bundle**, so a leading `/` in `resource` is
base-relative. Derivation and evidence share one field because both answer
"where did this come from," which is how OKF already spells it.

`commit` and `retrieved` record *what the claim was checked against*, and are
written at capture. Revalidation depends on them, and they cannot be recovered
afterwards — by then the verifying context is gone.

### 3.8 Finding the knowledge base

Resolved in order — `$KB_HOME`, then the pointer file
`~/.config/kb-tools/kb-home`, then by walking up from the working directory. The
pointer file exists because an environment variable is the one link in this
chain that can be set correctly and still be absent: it reaches a process only
through a shell that has already sourced the profile defining it.

**A knowledge base has no configuration file.** `SCHEMA.md` at its root is what
marks one, and what the walk tests for: a base carries the schema anyway so it
can be read without this plugin, so nothing exists purely to be detected.

**The layout below that is not fixed.** Nothing outside `/kb-init` names a
subdirectory. Skills are told what kind of item they are writing and read the
base to see where that kind already lives; `/kb-init` lays out the initial
directories, and only because an empty base has nothing to read. So the layout
can be reorganised without touching the plugin, which is the point — a corpus
outlives the arrangement it started in.

The single machine-local fact — where each source repository is checked out — is
carried by `.repository-mapping/<host>/<org>/<repo>` as a symlink to the
checkout, so the mapping is its own filename and nothing has to parse it. Items
record a repository by URL plus repo-relative path, and the symlink resolves the
URL to wherever the repo sits on this machine, so an item survives the repo
moving on disk and survives being read elsewhere, which needs only its own
links. It is the only part of a base not worth committing.

**The mapping is maintained by hand** — `mkdir -p` and `ln -s`, which is the
whole reason the filename carries the mapping. Nothing reads it yet either:
capture verifies in the repository it is already standing in, and revalidation,
the one pass that would need to resolve a URL, is deferred. Until then it is a
convention being kept ready, not a mechanism.

Who captured an item is likewise not configuration: it comes from `$KB_USER` or
the system user, because a base may have several contributors and the answer
belongs on the item.

**A capture never blocks on the resolution failing.** It writes the raw item
into the working directory instead and says so. Dictation happens at the moment
of learning, so friction there does not delay a capture, it loses one (§1.2 of
the motivation); a file in the wrong directory is recoverable with `mv`, and the
ID and layer make the destination unambiguous. Redaction has no such fallback —
it reads raw material and writes notes — so it asks for a knowledge base
instead.

## 4. Export

Reads the cards, emits one importable package, one deck per card kind.

- Only approved cards are exported — `status: draft` is how a proposed card
  awaiting the user sits, and it stays out of the package until it carries a
  `human:` entry in `verified`.
- Export is the one pass that writes back into a note: it regenerates the
  note's `cards` list from the cards that cite it. That direction is derived,
  the card → note direction is authoritative, and the write touches frontmatter
  and never prose.
- Scheduler identity derives from the card ID, so re-import updates an existing
  item rather than duplicating it.
- A duplicate card ID is fatal and nothing is written: two cards sharing an ID
  share an identity, and one would silently overwrite the other.
- `status: deprecated` cards are omitted and listed. **Omission does not suspend
  them** — a package can only add and update, so a card already in the scheduler
  stays active until it is suspended there by hand. The report is what makes that
  happen.
