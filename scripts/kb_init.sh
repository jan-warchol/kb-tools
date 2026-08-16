#!/usr/bin/env bash
# Create a knowledge base.  Usage: kb_init.sh [path]   (default ~/knowledge-base)
#
# Idempotent: re-running refreshes SCHEMA.md and the pointer file, and creates
# only what is missing.
#
# This is the only place in the plugin that names a subdirectory of a knowledge
# base. It lays out a starting arrangement because an empty base has nothing to
# read; everything else reads the base to see where things already live, so the
# layout can be reorganised afterwards without touching any of it.

set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
pointer="${XDG_CONFIG_HOME:-$HOME/.config}/kb-tools/kb-home"

kb=${1:-$HOME/knowledge-base}
case "$kb" in "~") kb=$HOME ;; "~/"*) kb="$HOME/${kb#\~/}" ;; esac

mkdir -p "$kb/raw" "$kb/notes" "$kb/cards" "$kb/sources" "$kb/.repository-mapping"

# .repository-mapping/ holds symlinks named after the repository URL, so the
# mapping needs no configuration file and no parser. It is the one
# machine-local thing here.
if [ ! -e "$kb/.gitignore" ]; then
  printf '/.repository-mapping/\n' > "$kb/.gitignore"
  echo "wrote .gitignore (.repository-mapping/ is machine-local)"
fi

# The base has to be readable without this plugin installed — and its presence
# is what identifies a directory as a knowledge base.
cp "$root/reference/frontmatter.md" "$kb/SCHEMA.md"
echo "wrote SCHEMA.md"

# A file, not an environment variable: nothing here depends on a shell restart.
mkdir -p "$(dirname "$pointer")"
printf '%s\n' "$kb" > "$pointer"
echo "wrote $pointer"

if command -v git >/dev/null 2>&1 && [ ! -d "$kb/.git" ]; then
  git -C "$kb" init -q && echo "initialised a git repository"
fi

echo "knowledge base ready at $kb"
