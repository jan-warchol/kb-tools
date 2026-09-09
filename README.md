# kb-tools

Tooling for a personal learning system. **Contains no knowledge** — it installs
on any machine, including ones the knowledge must never reach.

## Install

```
/plugin marketplace add jan-warchol/kb-tools
/plugin install kb-tools@kb
```

## Commands

| | |
|---|---|
| `/kb-init` | create a knowledge base |
| `/kb-capture` | dictate something learned |
| `/kb-redact` | work captures into notes |
| `/kb-update` | correct or extend something already captured |
| `/kb-cards` | make cards from a note |
| `/kb-quiz` | review what Anki says is due, or be questioned on a note |
| `/kb-export` | write the Anki import file |

```
/kb-init                               # or /kb-init ~/somewhere-else
/kb-capture the retry wrapper wraps the consumer, so retries happen before the ack
```

There is no lookup command: asking an agent inside the knowledge base is
sufficient, and needs no dedicated mechanism.

## Anki

Recall cards are reviewed in Anki as usual. **Understanding cards are reviewed
by `/kb-quiz`**, which drives Anki's own reviewer over
[AnkiConnect](https://foosoft.net/projects/anki-connect/) and sends the grade
you pick — so that half needs Anki running locally with the add-on. Everything
else works without it.

[`reference/anki-setup.md`](reference/anki-setup.md) holds the settings that
matter, worth reading once before the first import.

## Configuration

The one optional file is `<kb>/knowledge-base.yaml` — or `.yml`, either
spelling is read — holding what cannot be read off the base itself, today a
single key:

```yaml
anki_deck_name: Knowledge    # the default
```

## Reading

| | |
|---|---|
| [`motivation.md`](motivation.md) | the problem this exists for, and the obligations that follow |
| [`decisions.md`](decisions.md) | choices made about Anki, and where the boundary sits |
| [`reference/anki-setup.md`](reference/anki-setup.md) | the scheduler settings this depends on, and backups |
| [`reference/frontmatter.md`](reference/frontmatter.md) | the file format, specified once |
| [`deferred.md`](deferred.md) | what it deliberately does not do yet |
