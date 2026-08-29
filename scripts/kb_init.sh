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

mkdir -p "$kb/raw" "$kb/notes" "$kb/cards"

# Absolute from here on: the pointer file is read from wherever a skill happens
# to run, so a relative path given here would resolve against the wrong
# directory — and usually against no directory at all.
kb=$(cd "$kb" && pwd)

# The base has to be readable without this plugin installed — and its presence
# is what identifies a directory as a knowledge base.  Assembled rather than
# copied: kinds belonging to a separable capability live in a frontmatter-*.md
# fragment, so removing that capability needs no change here.
cp "$root/reference/frontmatter.md" "$kb/SCHEMA.md"
for fragment in "$root"/reference/frontmatter-*.md; do
  if [ -e "$fragment" ]; then
    printf '\n' >> "$kb/SCHEMA.md"
    cat "$fragment" >> "$kb/SCHEMA.md"
  fi
done
echo "wrote SCHEMA.md"

# A file, not an environment variable: nothing here depends on a shell restart.
mkdir -p "$(dirname "$pointer")"
printf '%s\n' "$kb" > "$pointer"
echo "wrote $pointer"

if command -v git >/dev/null 2>&1 && [ ! -d "$kb/.git" ]; then
  git -C "$kb" init -q && echo "initialised a git repository"
fi

echo "knowledge base ready at $kb"
