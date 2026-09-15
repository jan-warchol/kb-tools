#!/usr/bin/env bash
# Print the user to attribute human actions to: $KB_USER, else the system user.
#
# Not the git user, since capture has to work outside a repository, and not
# anything stored in the base, which may have several contributors.
#
# Injected into a skill with !`...`: always exits 0.

set -u

if [ -n "${KB_USER:-}" ]; then
  printf '%s\n' "$KB_USER"
else
  id -un 2>/dev/null || printf '%s\n' "${USER:-unknown}"
fi

exit 0
