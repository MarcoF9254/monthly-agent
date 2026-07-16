# Calendar Monthly Selection Decision Contract Draft

Status: architecture contract specified under `OD-CAL-ARCH-002` and clarified by `OD-CAL-ARCH-003`; executable schema `0.2.0-draft`; not accepted, implemented, or runtime-active

Draft schema: `schemas/drafts/calendar-only/calendar-monthly-selection.schema.json`

## Purpose

Selection records an externally authorized decision about which already-permitted calendar activities are intended for publication for one run and programme month. It grants no fields and cannot create or override eligibility.

## Required Shape

- `contract_version`
- stable `selection_id`
- positive `selection_version`
- `supersedes_selection_id`, `null` only for a root
- `run_id`
- `consumer_id: calendar-renderer`
- `programme_month`
- unique, lexicographically sorted `selected_activity_ids`
- `selection_subject_sha256`
- `authority_purpose: calendar-monthly-selection`
- `owner_authority` metadata
- externally resolvable `decision_reference`
- `authority_artifact_sha256`
- `decided_at`

The exact scope is `run_id` + `consumer_id` + `programme_month`.

## Lifecycle and Authority

Selection decisions are immutable and append-only. A root uses version 1. Each successor names the direct predecessor and uses the predecessor's version plus one. Historical decisions are never overwritten.

Missing, duplicate, broken, cyclic, cross-scope, unverifiable, or multiple-active chains fail closed. Filename, timestamp, mtime, directory order, generation order, and file presence establish no precedence.

`owner_authority` is descriptive metadata and cannot self-authenticate. `decision_reference` must resolve through the typed external authority registry to a verified accepted owner authority artifact and matching SHA-256.

## Authorization Subject and Exact Binding

The `calendar-monthly-selection` authorization-subject object contains exactly `contract_version`, `selection_id`, `selection_version`, `supersedes_selection_id`, `run_id`, `consumer_id`, `programme_month`, and `selected_activity_ids`. It excludes `owner_authority`, `decision_reference`, `authority_artifact_sha256`, `decided_at`, `selection_subject_sha256`, and the complete selection artifact SHA-256.

`selection_subject_sha256` is lowercase hexadecimal SHA-256 of the RFC 8785 canonical UTF-8 bytes of that subject. Validation reconstructs the subject and requires exact digest equality.

The external artifact must bind `authority_purpose: calendar-monthly-selection`, `authorized_subject_type: calendar-monthly-selection`, `authorized_subject_sha256` equal to `selection_subject_sha256`, and the exact run, consumer, and programme month. The consuming contract's expected purpose, registry purpose, and externally verified artifact purpose must be exactly equal. Any mismatch fails closed.

`selection_subject_sha256` proves which business content the owner authorized. `selection_artifact_sha256` proves which complete selection artifact the manifest consumed. They are distinct bindings.

Selection cannot mutate evidence or `qa_status`. An activity not selected cannot enter the manifest even if eligible. A selected activity cannot enter unless effective calendar eligibility and projection validation both pass.

An empty array is an explicit authorized empty publication set. Missing or failed selection resolution is not an empty selection.

## Future Storage

`data/calendar-selections/calendar-renderer/<run_id>/<programme_month>/<selection_id>.json`

This path is outside `data/runs/` and is not created during drafting.

## Non-Executable Fictional Example

```json
{
  "contract_version": "calendar-monthly-selection/0.2.0-draft",
  "selection_id": "example-selection-2099-01-v1",
  "selection_version": 1,
  "supersedes_selection_id": null,
  "run_id": "2099-01-r01",
  "consumer_id": "calendar-renderer",
  "programme_month": "2099-01",
  "selected_activity_ids": [
    "example-activity-001",
    "example-activity-003"
  ],
  "selection_subject_sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
  "authority_purpose": "calendar-monthly-selection",
  "owner_authority": "example-programme-owner",
  "decision_reference": {
    "registry_id": "example-registry-001",
    "authority_id": "example-authority-001"
  },
  "authority_artifact_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
  "decided_at": "2099-01-10T09:00:00+08:00"
}
```

This fictional example grants no real selection or authority.
