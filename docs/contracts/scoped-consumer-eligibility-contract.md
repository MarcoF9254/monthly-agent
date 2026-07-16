# Scoped Consumer Eligibility Contract Draft

Status: architecture contract specified and clarified by `OD-CAL-ARCH-003`; executable schema `0.2.0-draft`; not accepted, implemented, or runtime-active

Contract version: `scoped-consumer-eligibility/0.2.0-draft`

Draft schema: `schemas/drafts/calendar-only/scoped-eligibility-decision.schema.json`

## Decision Shape

Each immutable decision artifact requires:

- `contract_version`
- stable `decision_id`
- positive integer `decision_version`
- `supersedes_decision_id`, which is `null` for the first decision
- `run_id` and `activity_id`
- `consumer_id`
- `decision`: `eligible` or `denied`
- explicit `allowed_fields`
- explanatory `prohibited_uses`
- `eligibility_subject_sha256`
- `authority_purpose: calendar-eligibility`
- `authority_reference`, containing exact `registry_id` and `authority_id`
- `authority_artifact_sha256`
- `decided_at`

## Authority and Permission

Authority labels or descriptive metadata cannot self-authenticate. Only a verifiable, accepted owner decision artifact bound through the exact typed external registry and `authority_artifact_sha256` can grant eligibility; unverifiable authority fails closed.

The calendar-eligibility authorization-subject object contains exactly `contract_version`, `decision_id`, `decision_version`, `supersedes_decision_id`, `run_id`, `activity_id`, `consumer_id`, `decision`, `allowed_fields`, and `prohibited_uses`. It excludes all authority-reference metadata, `authority_artifact_sha256`, `decided_at`, and `eligibility_subject_sha256`. The digest is lowercase hexadecimal SHA-256 of its RFC 8785 canonical UTF-8 bytes; validation reconstructs the subject and requires exact equality.

The externally verified artifact must bind `authority_purpose: calendar-eligibility`, `authorized_subject_type: calendar-eligibility`, the exact eligibility subject digest, and exact run, activity, and consumer. Expected, registry, and artifact purposes must be equal. Calendar eligibility authority cannot authenticate monthly selection.

Only an `eligible` decision for the exact `consumer_id` grants its exact non-empty `allowed_fields`. `prohibited_uses` is explanatory and non-exhaustive. Every ungranted consumer, field, and use remains denied. A `denied` decision grants no fields.

The general scoped-eligibility architecture can express consumer-specific field subsets. The calendar-only refinement is stricter: an effective `calendar-renderer` eligible decision must grant exactly `activity_id`, `activity_title`, `dates`, and `time`, in that canonical order. A subset or any additional field cannot authorize calendar projection generation.

## Immutable Lifecycle

Decision artifacts are immutable and append-only. A root uses `decision_version: 1` and `supersedes_decision_id: null`. Replacement or supersession creates a new artifact with a new `decision_id`, the direct predecessor's version plus one, and that predecessor's exact `decision_id` in `supersedes_decision_id`. Revocation is a new `denied` decision that supersedes the previously effective decision. Historical artifacts are never overwritten.

Precedence is derived only from one valid, in-scope supersession chain. It must not be inferred from filename, modification time, directory order, or timestamp alone. Multiple active decisions, broken chains, cycles, duplicate `decision_id`, duplicate decision identity/version, or supersession across a different `run_id`, `activity_id`, or `consumer_id` fail closed.

Absence, malformed authority, or failure to match the exact `run_id`, `activity_id`, and `consumer_id` also fails closed. Decisions never transfer between consumers, mutate closed evidence, alter `qa_status`, or change `approved_records.json`.

## Storage

Decision artifacts belong under `data/consumer-eligibility/<consumer_id>/`, outside `data/runs/`. Storage is append-only; supersession adds an artifact rather than replacing one. Stage 1 creates no runtime decision artifact.

## Non-executable Fictional Example

```json
{
  "contract_version": "scoped-consumer-eligibility/0.2.0-draft",
  "decision_id": "example-decision-calendar-001-v1",
  "decision_version": 1,
  "supersedes_decision_id": null,
  "run_id": "2099-01-r01",
  "activity_id": "example-activity-001",
  "consumer_id": "calendar-renderer",
  "decision": "eligible",
  "allowed_fields": ["activity_id", "activity_title", "dates", "time"],
  "prohibited_uses": ["newsletter-publication", "infer-missing-values"],
  "eligibility_subject_sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
  "authority_purpose": "calendar-eligibility",
  "authority_reference": {
    "registry_id": "example-registry-001",
    "authority_id": "example-authority-001"
  },
  "authority_artifact_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
  "decided_at": "2099-01-15T10:00:00+08:00"
}
```

This fictional documentation example grants no eligibility.
