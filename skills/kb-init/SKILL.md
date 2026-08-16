---
name: kb-init
description: Create a knowledge base for the other kb skills. Use when the user wants to set up their knowledge base, or when captures have been landing in the working directory because no knowledge base is configured.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh *)
---

# kb-init

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/kb_init.sh <path>
```

The path is whatever the user gave, else `~/knowledge-base`. The default is
fine; re-running the script elsewhere later costs nothing.

It records the location in `~/.config/kb-tools/kb-home`, so nothing depends on
`KB_HOME` being exported or on a shell restart. Report where it landed.
