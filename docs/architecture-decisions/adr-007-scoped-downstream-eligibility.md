# ADR-007 Draft: Scoped Downstream Eligibility

Status: DECISION PENDING — Requires Human Approval

This draft remains outside `docs/decisions.md` because governance reserves that file for accepted ADRs. Final acceptance requires explicit Architecture Owner approval.

## Options and Trade-offs

The owner-reviewed options are: eligibility in the activity schema; eligibility in an external approval or authority artifact alone; projection alone; and policy plus scoped approval plus generated projection. An authority artifact alone lacks deterministic least-data delivery. A projection alone cannot grant or prove authority. Schema embedding couples mutable consumer policy to evidence.

## Recommended Decision

Adopt Option D: closed run records are evidence; accepted owner decisions are authority; consumer contracts are policy; generated allowlisted payloads are projections; and traceability is separately bound provenance.

Eligibility decisions are immutable and append-only. Supersession or revocation creates a new decision artifact and never overwrites history. Decision-chain resolution is explicit and fail-closed; filename, modification time, directory order, and timestamp alone confer no precedence.

Future authority belongs under `data/consumer-eligibility/<consumer_id>/`. Reproducible projections and provenance belong under `data/projections/<consumer_id>/`. They never mutate closed evidence.

## Boundary

This ADR is not accepted. Stage 1 changes no schema, validator, run artifact, approval artifact, or runtime behavior.
