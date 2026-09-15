#!/usr/bin/env bash
# Print the knowledge base's directories, two levels deep, relative to its
# root. Prints nothing when there is no base.
#
# Injected into a skill with !`...`: always exits 0.

set -u

kb=$("$(dirname "$0")/kb_home.sh")
[ -n "$kb" ] || exit 0

find "$kb" -mindepth 1 -maxdepth 2 -type d ! -path "$kb/.git" ! -path "$kb/.git/*" \
  2>/dev/null | sed "s#^$kb/##" | sort

exit 0
