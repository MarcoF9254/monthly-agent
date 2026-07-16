# Authorized Closed-World Registry Snapshot Contract Draft

Status: `authority-registry-snapshot/0.1.0-draft`; inactive, unimplemented, and not accepted as executable

Schema: `schemas/drafts/bounded-authority-input/authority-registry-snapshot.schema.json`

## Identity and Closed World

`registry_id` identifies the logical registry. `snapshot_id` identifies one immutable published version. They are not interchangeable.

For one exact run, consumer, programme month, and registry purpose, one externally authorized snapshot defines the complete authority-resolution universe. An artifact omitted from that closed world cannot participate in authoritative resolution. The snapshot indexes and binds artifacts; it does not grant eligibility or monthly-selection authority.

Entries are unique and lexicographically ordered by the tuple `(entry_type, logical_id)`. Duplicate logical identities, conflicting hashes, unknown types, malformed ordering, or incomplete revocation state fail closed.

## Lifecycle

Snapshots are immutable and append-only. Version 1 has no predecessor. Every later snapshot binds the direct predecessor's ID and complete artifact digest and preserves exact scope and logical registry identity.

Missing predecessor, broken predecessor digest, cycle, cross-scope supersession, duplicate identity, multiple active tips, unauthorized publication, stale-tip use, or rollback relative to the external trust anchor fails closed.

Authority revocations represented by entries are distinct from revocation of the snapshot's `calendar-registry-publication` authority. Neither substitutes for the other.

## Storage

Normative: artifact bytes must be deterministically digest-verifiable, and storage location confers no authority.

Non-normative guidance only: content-addressed storage, object-store layouts, hash directories, and archive packaging may be considered during implementation. No layout is required by this architecture.
