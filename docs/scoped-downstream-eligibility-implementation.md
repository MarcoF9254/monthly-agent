# Scoped Downstream Eligibility — Future Implementation

Status: not implemented in Stage 1.

## Decision Resolver

A future resolver must verify the external authority registry binding, accepted immutable owner authority, exact typed purpose, canonical authorization-subject digest, exact scope, stable decision identity and version, and one valid supersession chain. It must reject absence, purpose mismatch, subject mismatch, registry or artifact hash mismatch, unverifiable authority, multiple active decisions, duplicate identity/version, broken chains, cycles, cross-scope supersession, or precedence inferred from filename, modification time, directory order, or timestamp alone.

## Projection and Manifest Builders and Validators

A deterministic projection builder must join closed evidence to uniquely effective consumer eligibility. For `calendar-renderer`, `allowed_fields` must equal exactly `activity_id`, `activity_title`, `dates`, and `time`; subsets and additions fail closed. It applies direct-copy rules, rejects unsupported empties without inference, and emits canonical payload bytes plus separately bound provenance. Identical evidence, authority chain, contract version, and builder version must reproduce the same payload, `projection_id`, and `payload_sha256`.

A future selection resolver must resolve one bounded, authoritative, complete, externally verified, same-scope monthly selection chain. This draft does not choose the bounded-input mechanism or registry-publication model. A deterministic manifest builder must bind exactly the effective selected activity set to valid eligible projections and sort entries by `activity_id`. It must fail the whole manifest rather than drop any invalid selected activity, and it must not add an eligible but unselected projection. Projection presence, filenames, timestamps, directory enumeration, or generation order establish neither membership nor precedence.

Every entry requires schema and semantic revalidation of the referenced projection, recomputation of `projection_id` and `payload_sha256`, matching run, consumer, evidence and payload activity identity, exact calendar eligibility, and membership in the effective selection. `manifest_id` binds the effective selection ID and canonical artifact hash, builder and contract versions, scope, month, and ordered entries while excluding itself. The run/month relationship must be checked against authoritative run metadata, not inferred by parsing `run_id`; D1 currently lacks sufficient normative machine-readable month metadata, which blocks implementation authorization.

A calendar validator must reject wrong-consumer or wrong-record decisions, partial or additional calendar field grants, extra payload fields, `activity_title` in the renderer payload, any title transformation beyond the exact `activity_title` to `title` rename, `source_reference` leakage, transformed or partial `dates` or `time`, affirmative empty interpretations, missing or mismatched projection/provenance binding, selection mismatch, incomplete manifest membership, or output inside `data/runs/`.

Acceptance includes explicit subset and empty selections plus negative cases for absent or unverifiable authority, registry mismatch, unverified revocation, duplicate or cyclic eligibility or selection decisions, cross-scope supersession, partial or extra calendar grants, invalid direct copies, traceability leakage, broken hashes or identifiers, silent drops or additions, incomplete manifests, run/month mismatch, and evidence mutation.

## Migration and Activation Gate

Implementation authorization remains blocked on executable owner-authority and revocation-artifact schemas and verifiers, a bounded authoritative resolver-input mechanism, deterministic registry identity and publication mechanics, authoritative machine-readable `run_id` to `programme_month` binding, implementation validation, independent review, and explicit owner schema and implementation acceptance.

R03 records 033–045 remain `needs_review` and outside `approved_records.json`. Consumer completeness is separate from their historical `qa_status`. Existing approved-only consumer behavior is not weakened. Future calendar release requires an explicit accepted owner eligibility decision, accepted contracts, implemented negative-case validation, and separate downstream activation authorization.
