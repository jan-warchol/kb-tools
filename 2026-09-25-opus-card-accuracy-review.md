# Card accuracy review: work list

Opus reviewed all 100 cards on 2026-09-25 and edited nothing. The findings
were triaged on 2026-09-27 against each card's note and grouped by how the
fix is made. Work through it one section at a time and one item at a time,
settling each before the next.

**Rules for the fixing session**

- **Every finding is a hypothesis.** Check it against the source before
  acting. One finding (openssl, A8) has already turned out doubtful.
- **Claims come from the user.** Point at what is wrong, never at the right
  answer (`/kb-common`, Verification).
- **Scope goes in the question.** When a card needs a condition (a platform,
  a version, a default), put it in the question as scope, so the answer
  stays short.
- **Suspended in Anki** (marked ⏸): after the fixed card is exported and
  imported, unsuspend it. A card that is dropped is `status: deprecated`
  and stays suspended.

## A. Reword the card from its note

The note is right, and the card lost something while being shortened. The
agent proposes a rewording drawn from the note and the user approves it. No
new claim and no capture: `/kb-update` step 7.

1. ⏸ `kb:ZMRkHiieeFmz` (.netrc users): the card puts curl on par with ftp
   and wget. The note says curl reads `.netrc` only with an option.
2. ⏸ `kb:7BSJaDwOilYI` (Go vs Python "package"): "opposite of Python" is
   misleading, since Python's "package" has two meanings. The note says
   *commonly*.
3. ⏸ `kb:YLS08hrbdtyH` (Valkey): Redis didn't become closed source. The note
   says "not fully open source".
4. `kb:mCFgkUxcZkPR` (Go, two methods with the same name): read as "same
   type", it's a compile error, which conflicts with `kb:Zg7gaRhq1NEQ`. The
   note says *different types*.
5. `kb:jxLWLutCJNxq` (WSL reboot): "only kills the session" is vague. The
   note says it doesn't restart the VM.
6. ⏸ `kb:3kgT5bxtUmWI` (jq branching): the answer mixes in `def`, which has
   nothing to do with branching. Trim it.
7. ⏸ `kb:2V62y6DYmd5S` (trusting CA certificates "on Linux"): the path and
   command are Debian-family only. The user said so in another conversation,
   but it isn't recorded. Have them dictate it (a capture), then put it into
   the question as scope.
8. ⏸ `kb:6j7KMudtjpCM` (convert .cer to .crt): the review said
   `openssl x509` fails on a binary DER `.cer` without an input-format flag.
   OpenSSL 3.0.2 converted one without a flag in a test on 2026-09-27. The
   reviewer reportedly tested it too and saw a failure, so the result may
   depend on which openssl ran. macOS ships LibreSSL as `openssl`. **Settle
   which one fails first.** Then bring back the note's caveat ("older
   versions may require additional flags"), in the question as scope if it
   depends on the platform. If the note's caveat names the wrong condition,
   this moves to section B.
9. `kb:QBVoZarkZO7s` (unpacking a zipapp): "zipfiles" should read
   "zipapps". A typo, so scaffolding.

## B. Correct the note, then its cards

The note itself is wrong or incomplete, so the card can't be fixed from it.
Per note: one `/kb-update` session. The agent asks one pointed question per
finding, the user answers, and the answer is verified. **One correction
capture per note**, holding all of its corrections, never one per card.
Then the note's sections are edited and the cards reworded.

### B1. Content-length headers and GCS upload limits

Note: `kb:content-length-headers-and-gcs-upload-limits_2`. Its table and its
closing paragraph carry most of these.

- ⏸ `kb:DHA6SVNsNoSu` (signed URL enforces size): the size is part of the
  signature only if it is included as a signed header, not automatically.
- ⏸ `kb:aIr0oML7RS8X` (X-Upload-Content-Length): the request that starts a
  resumable upload can have a body (the object's metadata). "Carries no
  payload" is too strong. "Content-Length is meaningless" was added by the
  user during the card round, not taken from the note.
- ⏸ `kb:B0bBoJNWqWTh` (Content-Length applies to PUT and POST): the header
  goes with any message that has a body, including other methods and
  responses. The restriction comes from the note's table.
- ⏸ `kb:WhCjm6lvSqCv` (what can limit upload size to a range): presents the
  POST-policy condition as the only option. PUT signed URLs have their own
  mechanism.
- `kb:wjhgoevghtLc` (where the size limit must be enforced), minor: the
  frontend check doesn't enforce anything, it only improves the user
  experience.

### B2. musl

Note: `/notes/2026-08-25_musl-c-standard-library_2.md`. Both cards turn on
what statically linked glibc still needs at runtime.

- ⏸ `kb:yCylppzV9ol5` (why musl links statically better): "glibc has
  dependencies" misstates it. The trouble is what glibc loads at runtime,
  even in a static binary.
- `kb:AoPYfgNTywny` (static linking caveat): the card turns a glibc-specific
  point into one about every static library, and doesn't say which kind of
  dependency still has to be present.

### B3. Custom CA certificates on Linux

Note: `kb:custom-ca-certificates-linux_2`.

- ⏸ `kb:GGdpjeGnqN7H` (update-ca-certificates needs .crt): `.crt` is a file
  extension, not a format. The encoding matters too. Related to A8.

### B4. Go struct embedding

Note: `kb:go-struct-embedding_3`.

- ⏸ `kb:N5MtK05UTaLa` (Go type elements): leaves out a big restriction on
  where such an interface can be used.
- ⏸ `kb:xEmVcmjaaQUv` (embedded methods satisfy an interface): "Yes" hides a
  caveat about pointer receivers when the struct is embedded by value.

### B5. GCS signed-URL upload CORS

Note: `/notes/2026-08-25_gcs-signed-url-upload-cors_2.md`. The GCS checksum
note (`/notes/2026-08-11_gcs-upload-checksum_2.md`) makes the same claim
("will be for any upload to GCS") and needs the same correction.

- ⏸ `kb:0R2tRHFGLJng` (GCS CORS "by definition"): it isn't by definition.
  Also, CORS compares origins, not domains.

### B6. Sort order and locale

Note: `/notes/2026-08-26_sort-order-locale-collation_2.md`.

- `kb:hsytSeooyouY` (sort order and LANG): leaves out a variable that
  overrides both.

## C. Decide: leave, narrow or drop

The card is true as stated, or the gap is unlikely to mislead. One word from
the user per card. A narrowing that only removes something is a rewording
(section A). Anything that adds a claim moves to section B.

- ⏸ `kb:0qAoqV5o0Upx` (SubtleCrypto hashes): the list is missing one SHA
  variant. The lesson is that MD5 and CRC32c aren't there, so narrow the
  card to that, correct the list (B), or drop it.
- `kb:KwnaaBM3MRzY` (shiv "up to 2× faster"): doesn't say faster at what,
  and the number couldn't be verified. Drop the number, or the card.
- ⏸ `kb:l3ZQygUEN5v1` (Go and .netrc): read for more than just `go get`.
  Narrower than reality, but harmless.
- `kb:ymSrtJtNaiol` (ConfigMap change doesn't restart the pod): a bare "No"
  can suggest the mounted files never change.
- `kb:SvzeoQpVxSqX` (keyset sort key must be unique): a unique composite key
  is still a unique key.
- `kb:zalo4AL7JcOa` (`-race` in CI and production): "definitely not" may be
  too strong.
- `kb:VPikwbWQEFYT` (VS Code extensions with WSL): not every extension runs
  inside WSL. Some stay on the Windows side.
- `kb:x91CxySUhyTe` and `kb:EmW8zXTqSTg7` (Vite proxy): the review's note is
  garbled ("the Vite prrver"). Probably that the proxy exists only in the dev
  server, not in a production build. Check before deciding.
