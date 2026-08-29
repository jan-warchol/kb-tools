---
name: kb-common
description: General instructions for working on the knowledge base. Use always when interacting with knowledge bases managed by kb-tools plugin.
---

```
dictation ─▶ raw capture ─▶ note ─▶ card ─▶ export ─▶ Anki
```

- When working on items with human origin, only add new information when the user explicitly
  articulated it, or it comes from updated source items. NEVER add new information on your own.
  Articulating is the step that does the learning.
- When updating notes, prefer simply removing stale claims rather than describing change history.
- After a raw capture is created, prefer appending new statements to it rather than editing what was written.
  That is a default, not a prohibition: a user who asks for a raw item to be changed or removed gets it
  changed or removed.
- When new information is added, update downstream items (notes from row captures, cards from notes etc).
- When recording source code references, focus on the most important paths and symbols, not all of them.
- When choosing slug for the item ID, pick something that stands on its own - don't use truncated title.
- If you discover incorrect or outdated claims, don't say the correct answer. Give the user a pointer to
  what is wrong, so that he can figure it on his own and learn. Don't make the answer inferable from the
  pointer.
- An unverified note is not allowed to produce cards.
- If the bearings report the knowledge base as found rather than configured, say so and offer `/kb-init`
  to record it — it was found by looking around, not by being told where it is.
