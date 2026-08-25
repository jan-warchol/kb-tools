#!/usr/bin/env bash
# Resolve everything a kb skill needs before it can write: the knowledge base,
# the user, the time, and the repositories a capture is verified against.
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

# Every directory at most two levels below the working directory, shallowest
# first, dotted names skipped. Both the base and the repositories are looked for
# there, because a project keeps them a level or two down — kb/, frontend/,
# services/api/. Nothing descends past that, so a deep tree costs nothing.
nearby() {
  for d in "$PWD"/*/; do [ -d "$d" ] && printf '%s\n' "${d%/}"; done
  for d in "$PWD"/*/*/; do [ -d "$d" ] && printf '%s\n' "${d%/}"; done
}

# The knowledge base, in order: environment, pointer file, an enclosing base, a
# base below the working directory. The last one covers a base kept inside the
# project it serves, which no walk upwards can reach.
kb=""
kb_note=""
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
if [ -z "$kb" ]; then
  while IFS= read -r cand; do
    if is_kb "$cand"; then
      kb=$cand
      kb_note='   # found below the working directory, not configured'
      break
    fi
  done <<EOF
$(nearby)
EOF
fi
# Then beside it: with the base a sibling of the sub-project being worked in,
# it is neither above the working directory nor below it. Nearest ancestor
# first, and never above $HOME, where the next directory up holds other people.
if [ -z "$kb" ]; then
  dir=$(dirname "$PWD")
  while [ -n "$dir" ] && [ "$dir" != "/" ]; do
    for d in "$dir"/*/; do
      if is_kb "${d%/}"; then
        kb=${d%/}
        kb_note='   # found beside the working directory, not configured'
        break
      fi
    done
    { [ -n "$kb" ] || [ "$dir" = "$HOME" ]; } && break
    dir=$(dirname "$dir")
  done
fi

# $KB_USER, else the system user. Not the git user — capture has to work
# outside a repository — and not anything stored in the base, which may have
# several contributors.
user=${KB_USER:-}
[ -n "$user" ] || user=$(id -un 2>/dev/null) || user=${USER:-unknown}

# The repositories in view: the one enclosing the working directory, and any
# checked out below it — a project often holds several side by side, and a
# capture is verified in whichever one holds the file it read. Each is reported
# with its root, since a source `path` is relative to that root while the
# working directory is frequently somewhere inside it, or above it entirely.
repo_root() { git -C "$1" rev-parse --show-toplevel 2>/dev/null; }

enclosing=$(repo_root "$PWD")
below=$(
  while IFS= read -r d; do
    [ -e "$d/.git" ] && repo_root "$d"
  done <<EOF
$(nearby)
EOF
)
# Deduplicated, and never repeating the enclosing repository.
below=$(printf '%s\n' "$below" | awk -v e="$enclosing" 'NF && $0 != e && !seen[$0]++')
n_below=$(printf '%s' "$below" | grep -c . || true)

# A URL is canonicalised to https://<host>/<org>/<repo>: an insteadOf rule or an
# ssh remote otherwise yields a different string for the same repository.
describe_repo() {
  root=$1
  url=$(git -C "$root" remote get-url origin 2>/dev/null)
  commit=$(git -C "$root" rev-parse --short HEAD 2>/dev/null)
  note=""
  case $PWD in
    "$root") note='   # the working directory' ;;
    "$root"/*) note='   # holds the working directory' ;;
  esac
  if [ -n "$kb" ] && [ "$root" = "$kb" ]; then
    note='   # the knowledge base itself — not a source repository'
  fi
  printf -- '- root: %s%s\n' "$root" "$note"
  if [ -n "$url" ]; then
    printf '  repo: https://%s\n' "$(printf '%s' "$url" |
      sed -E 's#^[a-zA-Z+]+://##; s#^[^/@]*@##; s#^([^/:]+):#\1/#; s#\.git$##')"
  else
    printf '  repo: none (no origin remote — cite the documents you read instead)\n'
  fi
  [ -n "$commit" ] && printf '  commit: %s\n' "$commit"
  return 0
}

if [ -n "$kb" ]; then
  printf 'kb: %s%s\n' "$kb" "$kb_note"
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

if [ -n "$enclosing" ] || [ "$n_below" -gt 0 ]; then
  printf 'repos:   # cite the one holding the file you verified against;'
  printf ' its `path` is relative to that root\n'
  [ -n "$enclosing" ] && describe_repo "$enclosing"
  # A working directory holding dozens of checkouts is a container of projects,
  # not a project: listing them all would bury the bearings. Say how many, and
  # how to get the one that turns out to matter.
  if [ "$n_below" -gt 12 ]; then
    printf '# %d repositories below the working directory, too many to list.\n' "$n_below"
    printf "# Once you know which one holds the file you read, its \`.git/config\`\n"
    printf '# names the origin URL; ask if you cannot tell which one it is.\n'
  elif [ "$n_below" -gt 0 ]; then
    while IFS= read -r root; do
      describe_repo "$root"
    done <<EOF
$below
EOF
  fi
else
  printf 'repos: none (no git repository here or below — record documents as sources instead)\n'
fi

exit 0
