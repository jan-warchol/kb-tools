#!/usr/bin/env bash
# Print the git repository holding the working directory: its root, origin
# and commit, or "not in a repository".
#
# Injected into a skill with !`...`: always exits 0.

set -u

root=$(git rev-parse --show-toplevel 2>/dev/null)
url=$(git remote get-url origin 2>/dev/null)
commit=$(git rev-parse --short HEAD 2>/dev/null)

# ssh remotes and insteadOf rules give different strings for the same
# repository; reduce them all to https://<host>/<org>/<repo>.
if [ -n "$url" ]; then
  url=https://$(printf '%s' "$url" |
    sed -E 's#^[a-zA-Z+]+://##; s#^[^/@]*@##; s#^([^/:]+):#\1/#; s#\.git$##')
fi

if [ -n "$root" ]; then
  printf 'root: %s\n' "$root"
  printf 'origin: %s\n' "${url:-none}"
  printf 'commit: %s\n' "${commit:-none}"
else
  printf 'not in a repository\n'
fi

exit 0
