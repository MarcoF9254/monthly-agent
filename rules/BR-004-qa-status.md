# BR-004 QA Status

## Rule ID

BR-004

## Rule Name

QA status must match the workflow stage.

## Purpose

Prevent extracted records from being treated as QA-approved before source checking or Human Review has occurred.

## Applies to Fields

- `qa_status`
- `uncertain_fields`

## Validation Scope

BR-004 runs at the pre-QA business rule validation stage. This is before GPT QA or Human Review has processed the record set.

At this stage, every input record is treated as newly extracted. BR-004 does not track workflow history and cannot verify whether QA or Human Review has genuinely occurred.

If reused on post-QA or already-reviewed records, this rule must be re-scoped or replaced by a separate post-QA rule. Running BR-004 unchanged on post-QA data may misclassify legitimately approved records.

## Pass Condition

At the pre-QA validation stage, a record passes when `qa_status` is `"pending"`.

`uncertain_fields` may be empty or non-empty while `qa_status` is `"pending"`.

## Fail Condition

At the pre-QA validation stage, a record fails when:

- `qa_status` is `"approved"`, `"needs_review"`, or `"rejected"`.
- `qa_status` is `"approved"` while `uncertain_fields` is non-empty.

The second case is a high-risk subset of premature approval.

## Severity

- High: `qa_status` is `"approved"` at the pre-QA stage, especially when `uncertain_fields` is non-empty.
- Medium: `qa_status` is `"needs_review"` or `"rejected"` at the pre-QA stage.

## Finding Field Guidance

Use `field: "qa_status"` and `path: "qa_status"` when the finding is about premature status.

Use `field: "uncertain_fields"` and `path: "uncertain_fields"` when the finding is specifically about approved records with non-empty uncertainty.

For `qa_status: "approved"` with non-empty `uncertain_fields`, emit one finding using `field: "uncertain_fields"` and `path: "uncertain_fields"`. Do not also emit a separate `qa_status` finding for the same record unless this rule is later updated to allow overlapping BR-004 findings.

## Example Pass

```json
{
  "qa_status": "pending",
  "uncertain_fields": ["fee"]
}
```

## Example Fail

```json
{
  "qa_status": "approved",
  "uncertain_fields": []
}
```

```json
{
  "qa_status": "approved",
  "uncertain_fields": ["registration_period"]
}
```

```json
{
  "qa_status": "needs_review",
  "uncertain_fields": ["fee"]
}
```

```json
{
  "qa_status": "rejected",
  "uncertain_fields": []
}
```

## Human Review Guidance

If BR-004 fires during pre-QA validation, reset premature status to `"pending"`.

Do not mark records as approved until QA or Human Review has completed. If uncertainty remains, keep relevant field names in `uncertain_fields`.

Approval with non-empty `uncertain_fields` should not proceed to newsletter generation.
