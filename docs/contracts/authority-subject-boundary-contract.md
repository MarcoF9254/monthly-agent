# Authority Subject Boundary Contract Draft

Status: inactive Draft 0.1 contract; contract drafting only

A purpose-specific subject contains exactly the business decision approved by the owner. It excludes its digest, every authority reference, authority evidence, envelope digest, and complete enclosing artifact digest.

`subject_sha256 = SHA-256(RFC 8785 canonical UTF-8 bytes of the complete subject artifact)`, represented as 64 lowercase hexadecimal characters.

Construction is one-way: construct and validate the subject; hash its canonical bytes; construct and hash the envelope binding exact type, ID, digest, purpose, and scope; establish ordinary anchored membership except for publication bootstrap; then resolve lifecycle.

No digest input contains its own output. Subject and authority identity are distinct. Business-subject supersession does not supersede an authority, and authority supersession does not silently change business content.
