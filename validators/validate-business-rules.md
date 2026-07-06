# Business Rule Validation

## Purpose

Business rule validation checks whether extracted activity records follow monthly-agent workflow expectations that go beyond JSON schema structure.

These checks help catch records that are structurally valid but unsafe, incomplete, misleading, or not ready for QA or newsletter use.

## Input

- Schema-valid extracted activity records.
- Original source document or source text when source-supported checks are required.
- Extraction notes or QA notes when available.

## Output

Business rule validation should follow the shared pass/fail output contract in `docs/output-contracts.md`.

The current validator status enum is:

- `pass`: no business rule findings were produced.
- `fail`: one or more business rule findings were produced.

Any finding causes `FAIL`, regardless of severity. Warning-only behavior is not implemented yet and is reserved for future workflow support.

Each finding should include:

- `index`
- `activity_id`, using `"<missing>"` if the activity ID is missing
- `rule_id`
- `field`
- `path`
- `severity`
- `message`
- `recommendation`

## Rules

### Empty Key Fields

Key participant-facing fields should not be empty without being flagged.

If any of these fields are empty, missing in meaning, or set to unclear placeholder text, the field name should appear in `uncertain_fields`:

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

### Fee Amount and Uncertainty

If a fee entry has `amount: null`, `uncertain_fields` should include `fee` unless `amount_text` clearly says the activity is free.

Examples that do not require `fee` in `uncertain_fields`:

- `amount_text`: `免費`
- `amount_text`: `Free`

Examples that should require `fee` in `uncertain_fields`:

- `amount_text`: `待定`
- `amount_text`: `暫定$25，實際收費待中心公布`
- `amount_text`: `請向中心查詢`

### QA Status Before QA

Newly extracted records should remain `qa_status: "pending"` before QA review.

Records should not be marked `approved`, `needs_review`, or `rejected` during extraction unless a QA or Human Review step has explicitly made that decision.

### Approved Records and Uncertainty

Approved records should not contain unresolved uncertain fields.

If `qa_status` is `approved`, then `uncertain_fields` should usually be empty. If an approved record still has entries in `uncertain_fields`, it should be treated as a fail unless there is a documented reason that the uncertainty was resolved or accepted.

### Source Reference

`source_reference` should not be empty for extracted records.

The source reference should be specific enough for QA to trace the record back to the original source, such as a section heading, table row, page number, or nearby activity title.

### Registration Period

Missing or unclear registration periods should be flagged.

If `registration_period` is empty, says the date is not printed, or tells readers only to ask staff, then `uncertain_fields` should include `registration_period`.

Examples requiring a flag:

- `registration_period`: `通訊未列明報名日期`
- `registration_period`: `請向中心職員查詢`
- `registration_period`: `unknown`

### High-Impact Participant-Facing Errors

Errors in participant-facing practical details should be treated as high-impact because they can mislead service users.

High-impact fields include:

- Date
- Time
- Fee
- Venue
- Quota
- Eligibility or target participants
- Registration method
- Registration period

If any of these values are wrong, unsupported, missing, or misleading, the issue should be flagged for QA with high severity unless it is already clearly marked for Human Review.

## Pass Criteria

A record passes business rule validation when:

- Key fields are present or clearly listed in `uncertain_fields`.
- Fee uncertainty is correctly flagged.
- Newly extracted records remain `pending` before QA.
- Approved records have no unresolved uncertain fields.
- `source_reference` is present and useful.
- Missing or unclear registration details are flagged.
- No high-impact participant-facing errors are found.

## Fail Criteria

A record fails business rule validation when:

- Empty or unclear key fields are not listed in `uncertain_fields`.
- `amount` is `null` for an unclear fee and `fee` is not listed in `uncertain_fields`.
- A newly extracted record is marked `approved` before QA.
- An approved record still has unresolved uncertain fields.
- `source_reference` is empty or too vague to support QA.
- Missing registration period is not flagged.
- Date, time, fee, venue, quota, eligibility, or registration information is misleading or unsupported.