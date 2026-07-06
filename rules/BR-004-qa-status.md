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

## Pass Condition

Newly extracted records use `qa_status: "pending"`. Records are marked `approved`, `needs_review`, or `rejected` only after QA or Human Review makes that decision.

Approved records have no unresolved entries in `uncertain_fields`.

## Fail Condition

A newly extracted record is marked `approved`, `needs_review`, or `rejected` before QA. A record is marked `approved` while still containing unresolved uncertain fields.

## Severity

High when a record is incorrectly approved. Medium when the status is inconsistent but the record is not approved for downstream use.

## Example Pass

A newly extracted record has `qa_status: "pending"` and `uncertain_fields` includes `"fee"` for an unclear fee.

## Example Fail

A record has `qa_status: "approved"` while `uncertain_fields` includes `"registration_period"`.

## Human Review Guidance

Confirm whether QA or Human Review has already made a decision. If not, reset the status to `pending`. If unresolved uncertainty remains, do not approve the record until the issue is resolved or formally accepted.
