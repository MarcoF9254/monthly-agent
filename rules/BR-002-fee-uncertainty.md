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

`fee[].notes` is informational context for human review only. BR-002 does not evaluate `fee[].notes` when deciding whether a fee item passes or fails.

## Pass Condition

Fee details are source-supported. If `fee[].amount` is `null`, `uncertain_fields` includes `"fee"` unless `fee[].amount_text` matches one of the recognized free indicators defined below.

Free indicators are explicit fee information and do not require `fee` to be listed in `uncertain_fields`.

## Fail Condition

`fee[].amount` is `null` because the fee is unclear, pending, or requires enquiry, but `uncertain_fields` does not include `"fee"`.

BR-002 also fails when `fee[].amount` is not `null` but `fee[].amount_text` is missing, empty, placeholder-only, or not meaningful, and `uncertain_fields` does not include `"fee"`. `fee[].amount_text` is the source text, while `fee[].amount` is the normalized value. A normalized amount without meaningful source text must not be treated as confirmed.

BR-002 validates each `fee[]` item independently. A valid amount or free indicator in one fee item must not cause another unclear fee item to pass.

## Overlapping Findings

BR-002 may emit a finding for the same `fee[]` item that also triggered BR-001. This is intentional. Business rules may independently report findings on the same field or item when their own conditions are met. Any deduplication or display grouping should be handled later by the report or QA presentation layer, not by BR-002.

## Recognized Free Indicators

The following `fee[].amount_text` values are recognized as explicit free-fee information:

- `免費`
- `全免`
- `不設收費`
- `免收費`
- `免收費用`
- `費用全免`
- `free`
- `free of charge`
- `no charge`

Values not listed above must not be interpreted as free unless this specification is explicitly updated.

Matching rule:

- Trim surrounding whitespace before comparison.
- English matching is case-insensitive.
- Chinese matching is exact after trimming.
- Do not use broad substring matching unless this rule is later explicitly updated to allow it.

## Severity

High. Fee errors can mislead participants and affect registration decisions.

## Example Pass

`amount_text` is `"會員 $25；非會員 $35"`, `amount` is `null`, and `uncertain_fields` includes `"fee"`.

`amount_text` is `"免費"` and `amount` is `null`.

`amount_text` is `"Free of charge"` and `amount` is `null`.

## Example Fail

`amount_text` is `"請向中心查詢"`, `amount` is `null`, and `uncertain_fields` is empty.

`amount_text` is `"費用待定"`, `amount` is `null`, and `uncertain_fields` does not include `"fee"`.

`amount_text` is `""`, `amount` is `15`, and `uncertain_fields` does not include `"fee"`.

`fee` is:

```json
[
  {"fee_type": "會員", "amount": 20, "amount_text": "$20"},
  {"fee_type": "非會員", "amount": null, "amount_text": ""}
]
```

BR-001 may pass because the fee field exists. BR-002 must fail the second fee[] item unless that specific fee uncertainty is explicitly flagged.

## Human Review Guidance

Confirm the fee from the centre source, staff note, or later corrected programme notice. If the fee cannot be confirmed, keep `fee` in `uncertain_fields` and do not approve the record for newsletter use.
