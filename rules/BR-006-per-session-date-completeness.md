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
- `uncertain_fields` only if an approved uncertainty mechanism supports exact per-entry uncertainty marking

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

## Validation Scope

BR-001 owns field-level required-field validation for `dates`.

BR-006 owns per-entry completeness validation within `dates[]`.

BR-006 does not replace BR-001.

## Pass Condition

A record passes BR-006 when every `dates[]` entry satisfies one of the following:

1. `dates[i].date_text` is meaningful.
2. The exact per-session date field is explicitly marked as uncertain using an approved uncertainty mechanism.

`date_text` is meaningful when it is a string containing at least one non-whitespace character after trimming.

## Fail Condition

A record fails BR-006 when any `dates[]` entry has missing or blank `date_text` and that exact per-session date field is not explicitly marked uncertain using an approved uncertainty mechanism.

Emit one finding per failing `dates[]` entry.

Do not fail merely because the date is not parseable, not normalized, calendar-invalid, or inconsistent with weekday text; those are out of scope unless covered by another approved rule.

## Overlapping Findings

If a record is missing the entire `dates` field, BR-001 or schema validation owns that finding.

BR-006 applies only when `dates[]` exists and contains one or more entries.

If both BR-001 and BR-006 could report related date issues, validators should preserve the more specific BR-006 finding for per-entry missing `date_text` and preserve BR-001 for field-level missing or uncertain required fields.

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

`Fill in the session date from source evidence or mark the exact per-session date field as uncertain for QA / Human Review once an approved uncertainty mechanism exists.`

## Example Pass

Example Pass A: every `dates[]` entry has non-blank `date_text`.

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

Example Pass B: a per-session `date_text` is blank, but the exact field is explicitly marked uncertain using an approved per-entry uncertainty mechanism.

This example is dependent on the pending uncertainty-path decision. The repository currently defines `uncertain_fields` as field names and does not yet approve indexed paths such as `dates[1].date_text`.

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

## Human Review Guidance

Human Review should resolve whether the missing per-session date should be filled from source evidence, left uncertain, or corrected upstream.

Human Review must not be replaced by BR-006. BR-006 only reports deterministic missing per-session date entries.

## Pending Decision

```text
DECISION PENDING — Requires Human Approval
```

The repository currently defines `uncertain_fields` as field names, and existing precedent marks top-level fields such as `registration_period`.

BR-006 requires exact per-session uncertainty marking, such as an indexed path like `dates[i].date_text`, but that path format and per-array-element granularity are not yet approved.

BR-006 must not be implemented until the uncertainty path format and per-array-element uncertainty semantics are approved.

This pending decision is about more than string formatting; it affects whether `uncertain_fields` may represent exact nested array-element fields rather than only top-level field names.
