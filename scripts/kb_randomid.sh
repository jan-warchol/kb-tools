#!/usr/bin/env bash
# Draw random IDs: twelve characters of [A-Za-z0-9] (base62) from
# /dev/urandom, because a model asked for a random string does not produce
# one. This is the ID form for anything that leaves the base — a card, for
# instance, whose ID doubles as its Anki guid, a namespace shared with every
# deck the user has ever imported.
#
# Usage:  kb_randomid.sh [count]
#
# Drawn here rather than by a model because such an ID can land somewhere a
# repeat silently overwrites existing state (Anki's guid column does).

set -eu

count=${1:-1}

i=0
while [ "$i" -lt "$count" ]; do
  LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 12
  printf '\n'
  i=$((i + 1))
done
