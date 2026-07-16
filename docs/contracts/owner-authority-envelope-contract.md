# Owner Authority Envelope Contract Draft

Status: inactive Draft 0.1 contract under `OD-OAR-CONTRACT-AUTHOR-001`; not executable or implemented

One generic authority envelope binds one separately stored, RFC 8785-canonical purpose-specific subject. It records `authority_id`, lifecycle identity, exact `authority_purpose`, `authorized_subject_type`, `authorized_subject_id`, `authorized_subject_sha256`, exact scope, and `authorized_at`.

Purposes are non-transferable: `calendar-eligibility`, `calendar-monthly-selection`, `calendar-registry-publication`, `run-metadata-binding`, and `calendar-authority-revocation`. Purpose, subject type, digest, identifier, and scope must agree exactly.

For every purpose except registry publication, an envelope has effect only when its exact identifier and complete artifact digest are accepted ordinary membership in the externally anchored effective snapshot. Schema validity and digest integrity confer neither authority nor authentication.

Registry publication is the sole bootstrap exception. Its envelope must never occur as ordinary membership in the snapshot it authorizes. The bootstrap contract governs it.

There is no intrinsic Phase 1 expiry. No audit/source reference is required. Optional metadata is non-authoritative and cannot affect identity, authentication, digest construction, or resolution.

`authority_artifact_sha256` is SHA-256 of RFC 8785 canonical UTF-8 bytes of the complete envelope. The envelope excludes that digest. Authority supersession uses `supersedes_authority_id` and is independent of business-subject supersession.
