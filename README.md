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
| `/kb-cards` | make cards from a note |
| `/kb-quiz` | be questioned on a note |
| `/kb-export` | write the Anki import file |

```
/kb-init                               # or /kb-init ~/somewhere-else
/kb-capture the retry wrapper wraps the consumer, so retries happen before the ack
```

## Reading

| | |
|---|---|
| [`motivation.md`](motivation.md) | the problem this exists for, and the obligations that follow |
| [`spec.md`](spec.md) | what is built, and why each decision went the way it did |
| [`reference/frontmatter.md`](reference/frontmatter.md) | the file format, specified once |
| [`deferred.md`](deferred.md) | what it deliberately does not do yet |
