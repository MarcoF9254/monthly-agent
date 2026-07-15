# Scoped Consumer Eligibility Contract Draft

Status: not implemented or active

Contract version: `scoped-consumer-eligibility/v1-draft`

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
- `owner_authority`
- `decision_reference`
- `decided_at`

## Authority and Permission

`owner_authority` is metadata and cannot self-authenticate. Only a verifiable, accepted owner decision artifact can grant eligibility; unverifiable authority fails closed.

Only an `eligible` decision for the exact `consumer_id` grants its exact non-empty `allowed_fields`. `prohibited_uses` is explanatory and non-exhaustive. Every ungranted consumer, field, and use remains denied. A `denied` decision grants no fields.

## Immutable Lifecycle

Decision artifacts are immutable and append-only. Replacement or supersession creates a new artifact with a new `decision_id`, incremented `decision_version`, and explicit `supersedes_decision_id`. Revocation is a new `denied` decision that supersedes the previously effective decision. Historical artifacts are never overwritten.

Precedence is derived only from one valid, in-scope supersession chain. It must not be inferred from filename, modification time, directory order, or timestamp alone. Multiple active decisions, broken chains, cycles, duplicate `decision_id`, duplicate decision identity/version, or supersession across a different `run_id`, `activity_id`, or `consumer_id` fail closed.

Absence, malformed authority, or failure to match the exact `run_id`, `activity_id`, and `consumer_id` also fails closed. Decisions never transfer between consumers, mutate closed evidence, alter `qa_status`, or change `approved_records.json`.

## Storage

Decision artifacts belong under `data/consumer-eligibility/<consumer_id>/`, outside `data/runs/`. Storage is append-only; supersession adds an artifact rather than replacing one. Stage 1 creates no runtime decision artifact.

## Non-executable Fictional Example

```json
{
  "contract_version": "scoped-consumer-eligibility/v1-draft",
  "decision_id": "example-decision-calendar-001-v1",
  "decision_version": 1,
  "supersedes_decision_id": null,
  "run_id": "example-run-2099-01-r01",
  "activity_id": "example-activity-001",
  "consumer_id": "calendar-renderer",
  "decision": "eligible",
  "allowed_fields": ["activity_id", "title", "dates", "time"],
  "prohibited_uses": ["newsletter-publication", "infer-missing-values"],
  "owner_authority": "example-architecture-owner",
  "decision_reference": "example-accepted-owner-decision-001",
  "decided_at": "2099-01-15T10:00:00+08:00"
}
```

This fictional documentation example grants no eligibility.
