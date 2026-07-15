# Scoped Downstream Eligibility — Future Implementation

Status: not implemented in Stage 1.

## Decision Resolver

A future resolver must verify accepted owner authority, exact scope, stable decision identity and version, and one valid supersession chain. It must reject absence, unverifiable authority, multiple active decisions, duplicate identity/version, broken chains, cycles, cross-scope supersession, or precedence inferred from filename, modification time, directory order, or timestamp alone.

## Projection Builder and Validator

A deterministic builder must join closed evidence to the effective consumer decision, intersect `allowed_fields` with the consumer allowlist, apply direct-copy rules, reject unsupported empties without inference, and emit canonical payload bytes plus separately bound provenance. Identical evidence, authority chain, contract version, and builder version must reproduce the same payload, `projection_id`, and `payload_sha256`.

A calendar validator must reject wrong-consumer or wrong-record decisions, extra fields, `activity_title` in the renderer payload, any title transformation beyond the exact `activity_title` to `title` rename, `source_reference` leakage, transformed or partial `dates` or `time`, fields absent from `allowed_fields`, affirmative empty interpretations, missing or mismatched projection/provenance binding, or output inside `data/runs/`.

Acceptance includes positive reproducibility and negative cases for absent or unverifiable authority, mismatch, duplicate or cyclic decisions, cross-scope supersession, revocation, extra fields, invalid direct copies, empty required values, traceability leakage, broken hashes or identifiers, and evidence mutation.

## Migration and Activation Gate

R03 records 033–045 remain `needs_review` and outside `approved_records.json`. Consumer completeness is separate from their historical `qa_status`. Existing approved-only consumer behavior is not weakened. Future calendar release requires an explicit accepted owner eligibility decision, accepted contracts, implemented negative-case validation, and separate downstream activation authorization.
