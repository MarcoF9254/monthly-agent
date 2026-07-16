# Calendar Projection Contract Draft

Status: architecture contract specified; executable schema `0.1.0-draft`; not implemented or runtime-active

Contract version: `calendar-projection/0.1.0-draft`

Draft schemas:

- `schemas/drafts/calendar-only/calendar-activity-projection.schema.json`
- `schemas/drafts/calendar-only/calendar-monthly-manifest.schema.json`

## Renderer Payload

The strict renderer allowlist is:

- `activity_id`
- `title`
- `dates`
- `time`

The only title mapping is activity record `activity_title` to renderer `title`, with the string value copied exactly. No other title transformation is permitted. `dates` is copied as the complete ordered array of schema-valid date objects without flattening, omission, inference, or reordering. `time` is copied as the complete schema-valid string without inference or normalization.

No field appears merely because it exists in the activity schema. `source_reference` is prohibited from the renderer payload. Every payload field must be allowed both by this contract and by the effective owner decision. Missing, empty, placeholder, partial, or unmatched values acquire no affirmative meaning; required unsupported content fails closed.

For `calendar-renderer`, the effective eligibility grant must equal exactly the source fields `activity_id`, `activity_title`, `dates`, and `time`. General scoped eligibility may express subsets, but a subset or additional field is invalid for this fixed projection.

## Projection Identity and Provenance Binding

Every projection has a stable `projection_id` deterministically derived from projection contract version, `consumer_id`, evidence `run_id` and `activity_id`, the ordered effective eligibility `decision_id` values, and `payload_sha256`. The identity input excludes `projection_id`. Exact derivation is defined in `docs/contracts/calendar-only-vertical-slice-contract.md`.

Eligibility decision IDs are ordered from the unique root to the unique active tip. Missing, extra, reordered, or non-effective references fail closed.

The projection envelope keeps provenance separate from the renderer `payload` property. Provenance fields contain:

- `projection_id`
- `payload_sha256`
- the exact referenced eligibility `decision_id` values
- evidence `run_id` and `activity_id`
- `consumer_id`
- projection contract version
- `source_evidence_locator`, populated from the closed evidence record's `source_reference`

`payload_sha256` is computed over the exact UTF-8 bytes produced by the JSON Canonicalization Scheme in RFC 8785. Object keys are sorted as that scheme requires, array order is preserved, and insignificant whitespace is absent. The payload bytes used by the renderer must be exactly those canonical bytes.

Missing provenance, a missing or mismatched `projection_id`, a payload hash mismatch, an unresolved decision reference, an evidence-reference mismatch, or any broken binding fails closed. Provenance is not a renderer payload.

## Monthly Selection and Manifest Binding

Eligibility is permission; it is not publication selection. Manifest membership must equal the effective externally authorized monthly selection. Each selected activity must have uniquely effective exact-field eligibility and one schema-valid projection whose consumer, run, evidence activity, payload activity, recomputed `projection_id`, recomputed `payload_sha256`, and provenance all match the manifest entry. Any invalid selected activity fails the whole manifest; it cannot be silently dropped. Eligible but unselected projections cannot be added.

The manifest binds `selection_id`, the SHA-256 of the complete canonical selection artifact, builder and contract versions, consumer, run, programme month, and ordered entries. An empty manifest is valid only for an explicit effective selection with `selected_activity_ids: []`. The run/month relation must be verified from future authoritative run metadata and must not be inferred from `run_id`.

## Storage

Generated projections are reproducible envelopes with explicit identity, provenance, and a strictly isolated renderer `payload`. They belong under `data/projections/calendar-renderer/<run_id>/activities/<projection_id>.json`, outside immutable run trees. Monthly manifests belong under the sibling `manifests/` directory. Regeneration does not mutate closed evidence or eligibility decisions.

## Non-executable Fictional Examples

Projection envelope:

```json
{
  "contract_version": "calendar-projection/0.1.0-draft",
  "projection_id": "calproj_sha256_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "consumer_id": "calendar-renderer",
  "evidence": {
    "run_id": "2099-01-r01",
    "activity_id": "example-activity-001"
  },
  "eligibility_decision_ids": ["example-decision-calendar-001-v1"],
  "payload_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "source_evidence_locator": "fictional-source-page-1",
  "payload": {
    "activity_id": "example-activity-001",
    "title": "Example Gentle Exercise",
    "dates": [
      {
        "date_text": "2099-01-20",
        "start_date": "2099-01-20"
      }
    ],
    "time": "09:30-10:30"
  }
}
```

The digests are fictional shape examples, not claimed hashes. This example asserts nothing about R03 evidence or eligibility.
