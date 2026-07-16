# Self-Contained Verified Resolution Bundle Contract Draft

## OAR Inventory

OAR inventories declare every subject, envelope, snapshot, and lifecycle artifact needed by one scenario. The external trust anchor remains outside the bundle. Pre- and post-revocation fixture directories are independently complete.

Status: `resolution-bundle-root/0.1.0-draft`; inactive, unimplemented, and not accepted as executable

Schema: `schemas/drafts/bounded-authority-input/resolution-bundle-root.schema.json`

## Root Binding

The root deterministically binds bundle contract version, exact scope, logical `registry_id`, immutable `snapshot_id`, complete snapshot artifact digest, builder version, and the complete ordered declared artifact inventory.

Inventory entries are unique and lexicographically ordered by `(artifact_type, logical_id)`. Every physical artifact except the root is declared exactly once, and every declaration resolves to exactly one artifact whose canonical bytes match its lowercase SHA-256 digest. The root's `bundle_id` is derived from the RFC 8785 canonical root identity input excluding `bundle_id`.

The positive fictional bundle contains run metadata, two structurally valid eligibility decisions, one monthly selection, registry publication authority, and the complete registry snapshot. One fictional activity is intentionally unselected.

This is a valid Gate 2 bounded-input envelope chain only. It does not prove executable end-to-end verification of the separate owner-authority artifacts referenced by the eligibility and selection decisions. Their schemas, fixtures, and verifiers remain separately blocked and require separate owner authorization.

## Rejection

The Bundle verifier rejects a missing declared artifact, undeclared extra artifact, hash mismatch, duplicate logical identity, conflicting content for one identity, wrong or unknown type, wrong purpose, scope mismatch, or malformed ordering. The whole bundle fails; no partial resolution result is authoritative.

The bundle does not supply its own trust. Production consumes exactly this bundle plus one external trust anchor. Loose files remain non-authoritative linting/authoring input only.

Normative storage requirements are deterministic digest verification and location-independent authority. Content-addressed or archive storage is non-normative guidance only.
