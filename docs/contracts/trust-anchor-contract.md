# External Trust Anchor Contract Draft

Status: `bounded-authority-trust-anchor/0.1.0-draft`; inactive, unimplemented, and not accepted as executable

Schema: `schemas/drafts/bounded-authority-input/trust-anchor.schema.json`

## Normative Construction

Production resolution requires exactly one externally supplied trust-anchor object containing:

- `contract_version`;
- `authorized_tip_id`, equal to the authorized immutable `snapshot_id`;
- `expected_snapshot_artifact_sha256`;
- logical `registry_id`;
- exact scope;
- `trust_source`: either a trusted delivery/configuration context or an external authority reference;
- when externally referenced, the exact authority identifier and artifact digest.

The trust-anchor data structure records expected values. The trusted delivery or configuration channel supplies those values. Digest verification proves byte equality. Owner authority determines which tip is accepted. JSON Schema validation authenticates none of these.

The anchor must not be inferred from bundle or snapshot contents, filename, directory order, timestamp, version, highest visible version, only visible tip, or generation order.

## Fail-Closed Rules

Missing anchor, unknown tip, digest mismatch, tip/digest disagreement, multiple conflicting anchors, a stale but internally valid snapshot, or rollback to a superseded snapshot rejects the entire request. Rollback detection depends on comparison with this external anchor; an internally valid snapshot hash cannot prove current authorization.
