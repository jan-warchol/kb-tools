# kb-tools

Tooling for the personal learning system described in [`spec.md`](spec.md) —
with [`motivation.md`](motivation.md) for why it is shaped this way and
[`deferred.md`](deferred.md) for what it deliberately does not do yet.
**Contains no knowledge** — it installs on any machine, including ones the
knowledge must never reach.

| | |
|---|---|
| `/kb-init` | creates a knowledge base |
| `/kb-capture` | writes a verified raw item from dictation |
| `/kb-redact` | turns raw items into polished notes |
| `/kb-cards` | makes recall cards from a note |
| `/kb-export` | writes an Anki import file, one deck per card kind |

One card kind exists, the recall card — one fact, one answer. Cards graded
against a rubric are a future kind; see [`deferred.md`](deferred.md).

The file format is specified once, in
[`reference/frontmatter.md`](reference/frontmatter.md). The skills inject that
file, `/kb-init` copies it into the knowledge base as `SCHEMA.md`, and
`scripts/kb_check.py` checks its shape — so it is never restated anywhere.

## Install

```
/plugin marketplace add jan-warchol/kb-tools
/plugin install kb-tools@kb
```

## Set up a knowledge base

The knowledge base is a separate repository this plugin never ships or assumes:

```
/kb-init                               # or /kb-init ~/somewhere-else
```

That records the location in `~/.config/kb-tools/kb-home` and lays out a
starting arrangement of directories. A directory with `SCHEMA.md` at its root is
a knowledge base. The skills find it from `$KB_HOME` if it is exported, else that
pointer file, else by looking around the working directory — upwards, then a
couple of levels below it, then beside it — so nothing depends on a shell
restart, and a base kept inside a project (`~/src/myproject/kb`) is found from
anywhere in that project, including from a sibling checkout such as
`~/src/myproject/frontend`.

The one optional file is `knowledge-base.yaml` — or `.yml`, either spelling is
read — holding what cannot be read off the base itself, today a single key:

```yaml
anki_deck_name: Knowledge    # the default
```

Each card kind gets its own subdeck under that, named after the kind, so recall
cards land in `Knowledge::Recall`.

**The layout is yours to change.** Only `/kb-init` names a directory; the skills
read the base to see where each kind of item already lives. Rearrange it and
nothing breaks.

**You can capture before any of this exists.** With no knowledge base found,
`/kb-capture` writes the raw item into the current directory and says so; `mv`
it in later.

Items record a repository by URL, and `.repository-mapping/` resolves that URL
to wherever the repo sits on this machine — a symlink named after the URL:

```bash
cd $KB_HOME/.repository-mapping && mkdir -p github.com/acme
ln -s ~/src/acme/backend github.com/acme/backend
```

So an item survives the repo moving on disk, and survives being read on another
machine, which needs only its own links. **You maintain this by hand, and
nothing reads it yet** — capture verifies in the repository you are already
standing in. It matters when revalidation is built; keeping it up to date now
is optional.

Nothing in a knowledge base identifies a person — a base can have several
contributors, so who captured an item is recorded on the item. That comes from
`$KB_USER`, falling back to the system username, which is right on a personal
machine and the reason the variable is optional.

## Use

Say what you learned, from wherever you are working — normally inside the
project repository, so the code is at hand for verification:

```
/kb-capture the retry wrapper wraps the consumer, so retries happen before the ack
```

The skill repairs the transcription against the real source, verifies the claim
against the code, stops and asks if the claim is wrong, records the files and
symbols it read, writes one raw item, and reports how many captures are still
unredacted.

Later, work the captures into notes with `/kb-redact`. It takes the oldest raw
item with no note, polishes it without altering any claim, and leaves the note a
draft until you approve it.

## What it will not do

Constraints the design exists to protect, not missing features:

- It will not write a capture from the session transcript, your analysis, or
  the code. You have to articulate it — that is the step that does the
  learning.
- It will not silently correct a claim it finds to be false. It reports and
  stops; you state the correction.
- It will not rewrite a raw item on its own initiative. Raw material is the
  record of what you said, so a later correction is normally a new capture —
  though it will edit one if you ask.
- It will not mark something verified because it sounds right.
- It will not alter a claim while polishing it, and will not mark a note
  approved on your behalf.
