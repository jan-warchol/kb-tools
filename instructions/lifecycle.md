<!-- WIP: relocated verbatim. Wording, overlaps and duplicates untouched. -->

# Lifecycle and relationships

```
dictation ─▶ raw capture ─▶ note ─▶ card ─▶ export ─▶ Anki
```

- When updating notes, prefer simply removing stale claims rather than describing change history.
- After a raw capture is created, prefer appending new statements to it rather than editing what was written.
  That is a default, not a prohibition: a user who asks for a raw item to be changed or removed gets it
  changed or removed.
- When new information is added, update downstream items (notes from raw captures, cards from notes etc).
- An unverified note is not allowed to produce cards.

The **first** source of a derived item is the item it was derived from — a note
cites its raw item. That link is what marks the original as processed.

A note must be machine-confirmed or better *and* out of `status: draft` before
it can produce cards — a draft note is one the user has not approved, or one
nothing has verified. A card
must be human-reviewed before it is exported, because that entry *is* the
user's approval — a card that has been proposed and not yet approved is
`status: draft` and carries no `verified` key.
