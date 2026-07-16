# External Authority Registry Contract Draft

Status: architecture contract specified under `OD-CAL-ARCH-003`; executable schema `0.2.0-draft`; not accepted, implemented, or runtime-active

The registry provides deterministic lookup and integrity binding. It cannot create, accept, authenticate, or revoke authority by itself.

Each immutable snapshot contains stable identity, explicit predecessor or `null`, and entries sorted by `authority_id`. Each entry has exactly one non-transferable `authority_purpose`: `calendar-eligibility`, `calendar-monthly-selection`, or `calendar-authority-revocation`. There is no generic calendar-renderer authority and no wildcard scope.

Each entry binds an `authority_id` to an immutable authority artifact path, RFC 8785 SHA-256, accepted decision reference, exact authorized subject type and digest, and purpose-specific exact scope. Eligibility requires exact run, activity, and consumer. Monthly selection requires exact run, consumer, and programme month.

Every consumer verification requires exact equality among the purpose expected by the consuming contract, the registry entry purpose, and the externally verified artifact purpose. It also requires exact subject type, subject digest, artifact digest, and applicable scope equality. Authority for one purpose fails closed for every other purpose.

The registry is only an index and content-binding layer. It cannot grant or broaden authority, authenticate itself, transfer authority across purposes, or revoke authority through metadata alone.

If `authority_status` is `revoked`, the entry must also contain:

- `revocation_reference`;
- `revocation_artifact_sha256`;
- `revoked_at`.

The revocation reference must resolve externally to a verified immutable revocation artifact with `authority_purpose: calendar-authority-revocation`. Its authorization subject binds at least the exact original authority identifier, artifact SHA-256, original purpose, and exact original scope. Revocation authority cannot authenticate eligibility or selection. Registry status and revocation metadata remain insufficient without external verification of that exact subject.

Duplicate identifiers or paths, missing artifacts, hash mismatch, unverified grant or revocation, revocation scope mismatch, ambiguous snapshots, missing links, broken chains, cycles, cross-scope supersession, or multiple active snapshots fail closed.

Filename, timestamp, mtime, directory order, generation order, and file presence confer no precedence. Historical snapshots and authority artifacts are never overwritten.

Executable accepted-owner-authority and revocation-artifact schemas and verifiers remain explicit blockers before implementation authorization. Until the revocation schema exists, the exact subject binding above is normative contract design, not executable validation.

Draft schema: `schemas/drafts/calendar-only/external-authority-registry.schema.json`.
