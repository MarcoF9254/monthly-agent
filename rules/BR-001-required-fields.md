# BR-001 Required Fields

## Rule ID

BR-001

## Rule Name

Key fields must be present or flagged as uncertain.

## Purpose

Ensure extracted activity records do not silently omit participant-facing details needed for QA, Human Review, or newsletter preparation.

## Applies to Fields

- `activity_title`
- `dates`
- `time`
- `venue`
- `target_participants`
- `fee`
- `quota`
- `registration_method`
- `registration_period`
- `source_reference`
- `uncertain_fields`

## Pass Condition

All key fields contain source-supported values, or missing and unclear key fields are listed in `uncertain_fields`.

## Fail Condition

A key field is empty, unclear, placeholder-only, or missing in meaning, and the field name is not listed in `uncertain_fields`.

## Severity

High for participant-facing fields such as date, time, venue, fee, quota, eligibility, and registration. Medium for traceability or supporting fields unless they block QA.

## Example Pass

`registration_period` is `"通訊未列明報名日期"` and `uncertain_fields` includes `"registration_period"`.

## Example Fail

`venue` is empty and `uncertain_fields` is empty.

## Human Review Guidance

Check the original source for the missing or unclear field. If the value is present, update the record with source wording. If the source does not provide the value, keep the field uncertain and decide whether the record can proceed.
