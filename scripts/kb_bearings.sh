#!/usr/bin/env bash
# Resolve everything a kb skill needs before it can write: the knowledge base,
# the user, the time, and the repository a capture is verified against.
#
# Injected into SKILL.md with !`...`, so it must always exit 0 — a non-zero
# exit aborts the skill invocation and Claude never sees the instructions.

set -u

pointer="${XDG_CONFIG_HOME:-$HOME/.config}/kb-tools/kb-home"

expand() {
  case "$1" in
    "~") printf '%s' "$HOME" ;;
    "~/"*) printf '%s' "$HOME/${1#\~/}" ;;
    *) printf '%s' "$1" ;;
  esac
}

# A base carries the schema so it can be read without this plugin; that is what
# marks one. Nothing here knows the layout below it.
is_kb() { [ -f "$1/SCHEMA.md" ]; }

# The knowledge base, in order: environment, pointer file, an enclosing base.
kb=""
if [ -n "${KB_HOME:-}" ]; then
  cand=$(expand "$KB_HOME")
  is_kb "$cand" && kb=$cand
fi
if [ -z "$kb" ] && [ -r "$pointer" ]; then
  cand=$(expand "$(head -n 1 "$pointer")")
  is_kb "$cand" && kb=$cand
fi
if [ -z "$kb" ]; then
  dir=$PWD
  while [ "$dir" != "/" ] && [ -n "$dir" ]; do
    if is_kb "$dir"; then kb=$dir; break; fi
    dir=$(dirname "$dir")
  done
fi

# $KB_USER, else the system user. Not the git user — capture has to work
# outside a repository — and not anything stored in the base, which may have
# several contributors.
user=${KB_USER:-}
[ -n "$user" ] || user=$(id -un 2>/dev/null) || user=${USER:-unknown}

# The repository, canonicalised to https://<host>/<org>/<repo>: an insteadOf
# rule or an ssh remote otherwise yields a different string for the same repo.
repo=""
commit=""
in_git=no
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  in_git=yes
  commit=$(git rev-parse --short HEAD 2>/dev/null)
  url=$(git remote get-url origin 2>/dev/null)
  if [ -n "$url" ]; then
    repo="https://$(printf '%s' "$url" |
      sed -E 's#^[a-zA-Z+]+://##; s#^[^/@]*@##; s#^([^/:]+):#\1/#; s#\.git$##')"
  fi
fi

if [ -n "$kb" ]; then
  printf 'kb: %s\n' "$kb"
  printf 'layout:\n'
  find "$kb" -mindepth 1 -maxdepth 2 -type d \
    ! -path "$kb/.git*" ! -path "$kb/.repository-mapping*" 2>/dev/null |
    sed "s#^$kb/#  #" | sort
  printf '# Put each item where its kind already lives; ask if nothing fits.\n'
else
  printf 'kb: NONE — no knowledge base configured (/kb-init makes one).\n'
  printf '    Capture writes into the current directory (%s) and says so;\n' "$PWD"
  printf '    anything that must read the base stops and says so.\n'
fi
printf 'user: %s\n' "$user"
printf 'now: %s   # invocation time; re-sample with `date -u` for later stamps\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ -n "$repo" ]; then
  printf 'repo: %s\n' "$repo"
  [ -n "$commit" ] && printf 'commit: %s\n' "$commit"
elif [ "$in_git" = yes ]; then
  printf 'repo: none (a git repository with no origin remote)\n'
  [ -n "$commit" ] && printf 'commit: %s\n' "$commit"
else
  printf 'repo: none (not a git repository — record documents as sources instead)\n'
fi

exit 0
