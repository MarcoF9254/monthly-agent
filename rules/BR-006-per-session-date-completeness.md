# BR-006 — Per-session Date Completeness

## Rule ID

`BR-006`

## Rule Name

Per-session Date Completeness

## Purpose

BR-006 verifies that each individual session date entry in `dates[]` has meaningful `date_text`, while BR-001 remains responsible for field-level required-field validation.

This rule improves completeness checking for multi-session activities without inferring, repairing, approving, or validating source meaning.

## Scope

This is a per-record rule.

Applies to:

- `dates`
- `dates[].date_text`
- `uncertain_fields`

Out of scope:

- comparing activities
- merging sessions
- inspecting original source documents
- inferring missing dates from neighboring records
- inferring missing dates from prior months
- inferring missing dates from other sessions
- validating calendar correctness
- validating weekday consistency
- validating date format normalization
- resolving source authority
- resolving activity classification

BR-006 must not infer, repair, normalize, copy, or auto-fill dates.

## Uncertainty Granularity

BR-006 uses indexed uncertainty markers only.

The exact marker for a missing or unclear per-session date is:

`dates[i].date_text`

where `i` is the concrete zero-based index of the affected `dates[]` entry.

A top-level marker such as `dates` does not satisfy BR-006 for an individual missing or unclear `dates[i].date_text`.

This follows ADR-006.

## Validation Scope

BR-001 owns field-level validation for the `dates` field, such as missing `dates`, invalid field shape, or empty `dates[]`.

BR-006 owns per-entry completeness validation for `dates[i].date_text` within `dates[]`.

BR-006 does not replace BR-001.

When BR-006 is implemented and activated, BR-001 should not emit duplicate per-entry `dates[].date_text` findings for the same issue.

Any BR-001 implementation cleanup should happen together with BR-006 implementation and tests, not in this spec-alignment change.

## Pass Condition

A record passes BR-006 when every `dates[]` entry satisfies one of the following:

1. `dates[i].date_text` is meaningful.
2. The exact per-session date field is explicitly marked as uncertain using the ADR-006 indexed marker `dates[i].date_text`.

`date_text` is meaningful only when it is a meaningful string under the repository's existing meaningful-string convention, including trimming surrounding whitespace and excluding placeholder, pending, or unknown values such as `待定`, `未定`, `TBC`, or `unknown`.

Do not introduce fuzzy date parsing. Do not validate calendar correctness, weekday consistency, or date format normalization.

## Fail Condition

A record fails BR-006 when any `dates[]` entry has missing or non-meaningful `date_text` and that exact per-session date field is not explicitly marked uncertain using the ADR-006 indexed marker `dates[i].date_text`.

Emit one finding per failing `dates[]` entry.

Do not fail merely because the date is not parseable, not normalized, calendar-invalid, or inconsistent with weekday text; those are out of scope unless covered by another approved rule.

A top-level `uncertain_fields` marker such as `dates` must not suppress a BR-006 finding for a specific missing or non-meaningful `dates[i].date_text`.

## Overlapping Findings

If a record is missing the entire `dates` field, has invalid `dates` field shape, or has empty `dates[]`, BR-001 or schema validation owns that finding.

BR-006 applies only when `dates[]` exists and contains one or more entries.

If both BR-001 and BR-006 could report related date issues, validators should preserve the more specific BR-006 finding for per-entry missing or non-meaningful `date_text` and preserve BR-001 for field-level missing or uncertain required fields.

When BR-006 is implemented and activated, BR-001 should not emit duplicate per-entry `dates[].date_text` findings for the same issue. Any BR-001 implementation cleanup should happen together with BR-006 implementation and tests, not in this spec-alignment change.

## Severity

`high`

Missing participant-facing session dates affect activity attendance, registration, and newsletter correctness. This aligns with `docs/output-contracts.md`, which uses `high` for participant-facing practical errors such as date, time, fee, venue, quota, eligibility, or registration details.

## Finding Field Guidance

BR-006 findings should follow Finding Contract v1 in `docs/output-contracts.md`.

For BR-006-specific fields:

- `rule_id`: `BR-006`
- `field`: `dates`
- `path`: `dates[i].date_text`, where `i` is the concrete zero-based array index, such as `dates[1].date_text`
- `severity`: `high`

Recommended message:

`Session date is missing for dates[i].date_text.`

Recommended recommendation:

`Fill in the session date from source evidence or mark the exact per-session date field as uncertain for QA / Human Review using the ADR-006 indexed marker.`

## Example Pass

Example Pass A: every `dates[]` entry has meaningful `date_text`.

```json
{
  "activity_id": "ACT-006-PASS-A",
  "dates": [
    {
      "date_text": "2026-07-03"
    },
    {
      "date_text": "2026-07-10"
    }
  ],
  "uncertain_fields": []
}
```

Example Pass B: a per-session `date_text` is blank, but the exact field is explicitly marked uncertain using the ADR-006 indexed marker.

ADR-006 approves exact deterministic indexed paths such as `dates[1].date_text` for rules that explicitly require per-element uncertainty marking.

```json
{
  "activity_id": "ACT-006-PASS-B",
  "dates": [
    {
      "date_text": "2026-07-03"
    },
    {
      "date_text": ""
    }
  ],
  "uncertain_fields": ["dates[1].date_text"]
}
```

## Example Fail

A multi-session record fails when one `dates[]` entry has meaningful `date_text`, another entry has blank `date_text`, and no approved exact per-session uncertainty marker exists.

```json
{
  "activity_id": "ACT-006-FAIL-A",
  "dates": [
    {
      "date_text": "2026-07-03"
    },
    {
      "date_text": ""
    }
  ],
  "uncertain_fields": []
}
```

Expected finding:

- `rule_id`: `BR-006`
- `field`: `dates`
- `path`: `dates[1].date_text`
- `severity`: `high`

A top-level uncertainty marker does not suppress BR-006 for the specific missing entry:

```json
{
  "activity_id": "ACT-006-FAIL-B",
  "dates": [
    {
      "date_text": "2026-07-03"
    },
    {
      "date_text": ""
    }
  ],
  "uncertain_fields": ["dates"]
}
```

Expected finding:

- `rule_id`: `BR-006`
- `field`: `dates`
- `path`: `dates[1].date_text`
- `severity`: `high`

## Human Review Guidance

Human Review should resolve whether the missing per-session date should be filled from source evidence, left uncertain using the ADR-006 indexed marker, or corrected upstream.

Human Review must not be replaced by BR-006. BR-006 only reports deterministic missing per-session date entries.

## Implementation Status

Uncertainty semantics for BR-006 are resolved by ADR-006.

The validator implementation and focused direct unit tests are complete.

Runtime activation is held. BR-006 is not included in the active business-rule registry.

Future activation requires real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval.
