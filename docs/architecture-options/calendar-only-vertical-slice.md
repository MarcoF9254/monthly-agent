# Calendar-Only Vertical Slice — Implementation Architecture Options

Decision authority: `OD-CAL-ARCH-001`, `OD-CAL-ARCH-002`, and `OD-CAL-ARCH-003`

Status: Architecture direction approved for contract drafting. No implementation or activation is authorized.

## Option A — Per-Activity Projection

Generate one canonical projection per eligible activity.

Benefits:

- smallest independently auditable unit;
- a changed activity does not require replacing unrelated projections;
- direct binding to one evidence record and its effective eligibility chain.

Trade-offs:

- no canonical monthly inventory;
- consumers must discover files externally;
- absence cannot be distinguished from incomplete generation without another contract.

## Option B — Monthly Batch Projection

Generate one canonical payload containing every eligible activity for a programme month.

Benefits:

- one consumer input;
- monthly completeness is represented in one artifact;
- simple distribution.

Trade-offs:

- one change replaces the whole batch;
- per-activity provenance and reuse are less granular;
- partial regeneration and independent verification are harder.

## Option C — Per-Activity Projections Plus Monthly Manifest

Generate one canonical projection per eligible activity and a canonical monthly manifest that enumerates and binds the complete ordered projection set.

Benefits:

- preserves per-activity auditability and reproducibility;
- makes monthly completeness explicit;
- supports deterministic discovery without trusting filenames or directory order;
- binds each manifest entry to both `projection_id` and `payload_sha256`.

Trade-offs:

- two artifact types must validate together;
- manifest regeneration is required when membership or projection identity changes;
- implementation must prevent incomplete, duplicated, or mismatched sets.

## Approved Direction

The Architecture Owner approved Option C under `OD-CAL-ARCH-001`: per-activity canonical projections plus a monthly manifest. `OD-CAL-ARCH-002` refines Option C by requiring an externally authorized monthly selection decision so permission and publication inclusion remain separate.

The manifest binds the effective selection to valid eligible projections; projection presence or eligibility alone never selects publication. This remains contract drafting only and does not accept schemas, implement logic, issue decisions, generate artifacts, migrate a consumer, or activate `calendar-renderer`.

`OD-CAL-ARCH-003` clarifies the draft contracts only: authority purposes are typed and non-transferable, and each external artifact must bind the digest of the exact canonical authorization subject. It does not accept an executable schema or authorize implementation.
