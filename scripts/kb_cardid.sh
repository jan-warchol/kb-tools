#!/usr/bin/env bash
# Draw card IDs.  The tail comes from /dev/urandom because a model asked for a
# random string does not produce one, and a card ID doubles as its Anki guid —
# a namespace shared with every deck the user has ever imported, where a
# counter unique to this base is not enough.
# Card IDs for a note: its slug, then ten random characters of [A-Za-z0-9].
#
# Usage:  kb_cardid.sh <note-id> [count]
#
# Drawn here rather than by a model because a card ID lands in Anki's `guid`
# column, where a repeat silently overwrites an existing card's history.

set -eu

[ $# -ge 1 ] || { echo "usage: kb_cardid.sh <note-id> [count]" >&2; exit 2; }

slug=${1#[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-}
count=${2:-1}

i=0
while [ "$i" -lt "$count" ]; do
  printf '%s-%s\n' "$slug" \
    "$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 10)"
  i=$((i + 1))
done
