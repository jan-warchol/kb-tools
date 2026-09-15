#!/usr/bin/env bash
# Print the knowledge base's path, or nothing when there is none.
#
# Injected into a skill with !`...`: always exits 0, since a non-zero exit
# aborts the skill invocation.

set -u

# A base is marked by the schema it carries, so it can be read without this
# plugin and nothing exists purely to be detected.
is_kb() { [ -f "$1/SCHEMA.md" ]; }

expand_tilde() {
  case "$1" in
    "~") printf '%s' "$HOME" ;;
    "~/"*) printf '%s' "$HOME/${1#\~/}" ;;
    *) printf '%s' "$1" ;;
  esac
}

find_kb() {
  local cand dir d
  pointer="${XDG_CONFIG_HOME:-$HOME/.config}/kb-tools/kb-home"

  # 1. $KB_HOME.
  if [ -n "${KB_HOME:-}" ]; then
    cand=$(expand_tilde "$KB_HOME")
    is_kb "$cand" && { printf "%s\n" "$cand"; return; }
  fi

  # 2. The pointer file kb_init.sh writes. It exists because $KB_HOME only
  #    reaches processes started from a shell that sourced the profile.
  if [ -r "$pointer" ]; then
    cand=$(expand_tilde "$(head -n 1 "$pointer")")
    is_kb "$cand" && { printf "%s\n" "$cand"; return; }
  fi

  # 3. The working directory or one of its ancestors.
  dir=$PWD
  while [ -n "$dir" ] && [ "$dir" != "/" ]; do
    is_kb "$dir" && { printf "%s\n" "$dir"; return; }
    dir=$(dirname "$dir")
  done

  # 4. Up to two levels below: a base kept inside the project it serves.
  for d in "$PWD"/*/ "$PWD"/*/*/; do
    is_kb "${d%/}" && { printf "%s\n" "${d%/}"; return; }
  done

  # 5. A child of an ancestor, nearest first: a base that is a sibling of the
  #    sub-project being worked in. Never above $HOME.
  dir=$(dirname "$PWD")
  while [ -n "$dir" ] && [ "$dir" != "/" ]; do
    for d in "$dir"/*/; do
      is_kb "${d%/}" && { printf "%s\n" "${d%/}"; return; }
    done
    [ "$dir" = "$HOME" ] && break
    dir=$(dirname "$dir")
  done
}

find_kb

exit 0
