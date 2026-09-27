I read all 100 cards and edited nothing. The knowledge-base rules say fixes should come from you (a dictated correction through /kb-update), so below I point at what's wrong without writing the corrected answer. Where you'd need to know the right command to see the problem, I name the missing piece.

Likely wrong: fix these first

- kb:6j7KMudtjpCM (convert .cer to .crt): Keychain .cer files are often in binary DER format. By default openssl x509 expects the text-based PEM format, so the command as written will fail on those files. It needs an input-format option.
- kb:ZMRkHiieeFmz (.netrc users): curl doesn't read .netrc unless you pass a flag. It isn't on par with ftp and wget.
- kb:DHA6SVNsNoSu (signed URL enforces size): the size is part of the signature only if you choose to include it as a signed header. It isn't there automatically.
- kb:aIr0oML7RS8X (X-Upload-Content-Length): the request that starts a resumable upload can have a body (the object's metadata). So "carries no payload" and "Content-Length is meaningless" are too strong.
- kb:B0bBoJNWqWTh (Content-Length applies to PUT and POST): the header goes with any message that has a body, including other methods and responses. As written, you'd learn a false restriction.
- kb:7BSJaDwOilYI (Go vs Python "package"): in Python, "package" has two meanings, and one of them matches Go's meaning. "Opposite of Python" is misleading.
- kb:yCylppzV9ol5 (why musl links statically better): "glibc has dependencies" misstates the problem. The trouble is what glibc loads at runtime, even in a static binary.
- kb:YLS08hrbdtyH (Valkey): Redis didn't become closed-source. "Closed the licence" is the wrong word for what changed.

Incomplete in a way you could learn wrong

- kb:2V62y6DYmd5S (trusting CA certificates "on Linux"): the path and command are specific to Debian and Ubuntu. Other distro families use different ones.
- kb:GGdpjeGnqN7H (update-ca-certificates needs .crt): .crt is a file extension, not a format. The encoding also matters.
- kb:WhCjm6lvSqCv (what can limit upload size to a range): the answer gives the POST-policy option as the only one. PUT signed URLs have their own mechanism.
- kb:0qAoqV5o0Upx (SubtleCrypto hashes): the list is missing one SHA variant.
- kb:N5MtK05UTaLa (Go type elements): it leaves out a big restriction on where such an interface can be used.
- kb:xEmVcmjaaQUv (embedded methods satisfy an interface): "Yes" hides a caveat about pointer receivers when the struct is embedded by value.
- kb:l3ZQygUEN5v1 (Go and .netrc): it's read for more than just go get.
- kb:0R2tRHFGLJng (GCS CORS "by definition"): it isn't by definition. Also, CORS compares origins, not domains.
- kb:3kgT5bxtUmWI (jq branching): the question is about conditions, but the answer mixes in def, which has nothing to do with branching.

Ambiguous wording

- kb:mCFgkUxcZkPR (Go, two methods with the same name): the question doesn't say they're on different types. Read as "same type", it's a compile error, and that conflicts with kb:Zg7gaRhq1NEQ.
- kb:ymSrtJtNaiol (ConfigMap change doesn't restart the pod): a bare "No" can suggest the mounted files never change.
- kb:jxLWLutCJNxq (WSL reboot): "only kills the session" is vague about what actually happens.
- kb:hsytSeooyouY (sort order and LANG): it leaves out a variable that overrides both.
- kb:SvzeoQpVxSqX (keyset sort key must be unique): it doesn't say that a unique composite key also works.
- kb:AoPYfgNTywny (static linking caveat): it doesn't say which kind of dependency still has to be present.
- kb:KwnaaBM3MRzY (shiv "up to 2× faster"): it doesn't say faster at what (build time or startup), and I couldn't verify the number.

Minor, fine to leave

- kb:zalo4AL7JcOa: "definitely not" in production dance.
- kb:VPikwbWQEFYT: not every VS Code extension runs inside WSL; some stay on the Windows side.
- kb:x91CxySUhyTe and kb:EmW8zXTqSTg7: the Vite prrver.
- kb:QBVoZarkZO7s: "zipfiles" should probably read "zipapps".
- kb:wjhgoevghtLc: the frontend check doesn't really enforce the limit; it only improves the user experience.
