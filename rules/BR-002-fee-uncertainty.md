# BR-002 Fee Uncertainty

## Rule ID

BR-002

## Rule Name

Unclear fees must be flagged.

## Purpose

Prevent unclear, pending, or unsupported fee details from being treated as confirmed participant-facing information.

## Applies to Fields

- `fee`
- `fee[].amount_text`
- `fee[].amount`
- `fee[].notes`
- `uncertain_fields`

## Pass Condition

Fee details are source-supported. If `fee[].amount` is `null`, `uncertain_fields` includes `"fee"` unless `fee[].amount_text` clearly states the activity is free.

## Fail Condition

`fee[].amount` is `null` because the fee is unclear, pending, or requires enquiry, but `uncertain_fields` does not include `"fee"`.

## Severity

High. Fee errors can mislead participants and affect registration decisions.

## Example Pass

`amount_text` is `"暫定$25，實際收費待中心公布"`, `amount` is `null`, and `uncertain_fields` includes `"fee"`.

## Example Fail

`amount_text` is `"請向中心查詢"`, `amount` is `null`, and `uncertain_fields` is empty.

## Human Review Guidance

Confirm the fee from the centre source, staff note, or later corrected programme notice. If the fee cannot be confirmed, keep `fee` in `uncertain_fields` and do not approve the record for newsletter use.
