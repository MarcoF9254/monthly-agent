# BR-003 Registration Period

## Rule ID

BR-003

## Rule Name

Missing or unclear registration periods must be flagged.

## Purpose

Ensure participants are not given incomplete or misleading registration timing.

## Applies to Fields

- `registration_period`
- `registration_method`
- `uncertain_fields`

## Pass Condition

`registration_period` contains a source-supported registration date, deadline, period, or clear statement such as `"毋須報名"`. If the period is missing or unclear, `uncertain_fields` includes `"registration_period"`.

## Fail Condition

`registration_period` is empty, says the date is not printed, or only tells readers to ask staff, but `uncertain_fields` does not include `"registration_period"`.

## Severity

High. Registration timing affects whether participants can join an activity.

## Example Pass

`registration_period` is `"通訊未列明報名日期"` and `uncertain_fields` includes `"registration_period"`.

## Example Fail

`registration_period` is `"請向中心職員查詢"` and `uncertain_fields` does not include `"registration_period"`.

## Human Review Guidance

Check whether the registration period appears in a heading, footer, registration note, or related table column. If not found, ask the centre or reviewer to confirm whether the activity is open, closed, or by enquiry only.
