# Calendar Projection Contract Draft

Status: architecture contract specified; not implemented or runtime-active

Contract version: `calendar-projection/v1-draft`

## Renderer Payload

The strict renderer allowlist is:

- `activity_id`
- `title`
- `dates`
- `time`

The only title mapping is activity record `activity_title` to renderer `title`, with the string value copied exactly. No other title transformation is permitted. `dates` is copied as the complete ordered array of schema-valid date objects without flattening, omission, inference, or reordering. `time` is copied as the complete schema-valid string without inference or normalization.

No field appears merely because it exists in the activity schema. `source_reference` is prohibited from the renderer payload. Every payload field must be allowed both by this contract and by the effective owner decision. Missing, empty, placeholder, partial, or unmatched values acquire no affirmative meaning; required unsupported content fails closed.

## Projection Identity and Provenance Binding

Every projection has a stable `projection_id` deterministically derived from `consumer_id`, evidence `run_id` and `activity_id`, the ordered effective eligibility `decision_id` values, projection contract version, builder version, and `payload_sha256`. Separate provenance must contain:

- `projection_id`
- `payload_sha256`
- the exact referenced eligibility `decision_id` values
- evidence `run_id` and `activity_id`
- `consumer_id`
- projection contract and builder versions
- generation time
- `source_evidence_locator`, populated from the closed evidence record's `source_reference`

`payload_sha256` is computed over the exact UTF-8 bytes produced by the JSON Canonicalization Scheme in RFC 8785. Object keys are sorted as that scheme requires, array order is preserved, and insignificant whitespace is absent. The payload bytes used by the renderer must be exactly those canonical bytes.

Missing provenance, a missing or mismatched `projection_id`, a payload hash mismatch, an unresolved decision reference, an evidence-reference mismatch, or any broken binding fails closed. Provenance is not a renderer payload.

## Storage

Generated projections are reproducible artifacts with explicit identity and provenance. Payloads belong under `data/projections/calendar-renderer/payloads/` and provenance under `data/projections/calendar-renderer/provenance/`, outside immutable run trees. Regeneration does not mutate closed evidence or eligibility decisions.

## Non-executable Fictional Examples

Payload:

```json
{
  "activity_id": "example-activity-001",
  "title": "Example Gentle Exercise",
  "dates": [
    {
      "date_text": "2099-01-20"
    }
  ],
  "time": "09:30–10:30"
}
```

Provenance:

```json
{
  "projection_id": "example-calendar-projection-001",
  "payload_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "eligibility_decision_ids": ["example-decision-calendar-001-v1"],
  "run_id": "example-run-2099-01-r01",
  "activity_id": "example-activity-001",
  "consumer_id": "calendar-renderer",
  "projection_contract_version": "calendar-projection/v1-draft",
  "builder_version": "example-builder-1",
  "generated_at": "2099-01-16T10:00:00+08:00",
  "source_evidence_locator": "fictional-source-page-1"
}
```

The digest is a fictional shape example, not a claimed hash. These examples assert nothing about R03 evidence or eligibility.
