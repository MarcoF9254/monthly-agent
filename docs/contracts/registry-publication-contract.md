# Registry Publication Authority Contract Draft

Status: `registry-publication-authority/0.1.0-draft`; inactive, unimplemented, and not accepted as executable

Schema: `schemas/drafts/bounded-authority-input/registry-publication-authority.schema.json`

## Separate Purpose

Snapshot publication requires external authority with the exact non-transferable purpose `calendar-registry-publication`. It cannot authenticate `calendar-eligibility`, `calendar-monthly-selection`, or `calendar-authority-revocation`; those purposes cannot authenticate publication.

Publication authority is separate from revocations contained in a snapshot and from revocation of the publication authority artifact itself.

## Canonical Subject

The snapshot authorization subject contains exactly:

- `contract_version`;
- `registry_id`;
- `snapshot_id`;
- `snapshot_version`;
- `supersedes_snapshot_id`;
- `supersedes_snapshot_artifact_sha256`;
- exact `scope`;
- complete ordered `entries`.

`snapshot_subject_sha256` is lowercase hexadecimal SHA-256 over RFC 8785 canonical UTF-8 bytes of that object. The subject excludes its own digest, authority evidence, publication timestamp/metadata, and the complete snapshot artifact digest.

Construction order:

1. construct the canonical subject;
2. compute `snapshot_subject_sha256`;
3. externally verify publication authority binding that digest, exact type, registry, snapshot, and scope;
4. attach the authority reference and authority artifact digest to the complete snapshot;
5. compute the complete canonical snapshot artifact digest.

The complete snapshot artifact contains no field for its own digest. No direct or indirect hash cycle exists. Reusing authority after any subject mutation fails closed.
