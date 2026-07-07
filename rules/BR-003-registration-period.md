# BR-003 Registration Period

## Rule ID

BR-003

## Rule Name

Registration timing must be actionable or explicitly exempt.

## Purpose

Ensure each activity communicates when registration opens, closes, remains available, or is not required. Participants should not receive a record that only describes how to register or asks them to enquire, without actionable registration timing or a clear no-registration exemption.

## Scope

BR-003 focuses only on registration timing.

Applies to:

- `registration_period`
- `uncertain_fields`

Out of scope:

- `registration_method`
- Activity dates
- Centre practice or assumptions not stated in the source

The validator must not infer registration periods from activity dates, registration methods, recurring centre practice, or general programme context.

## Pass Condition

A record passes BR-003 when one of the following is true:

- `registration_period` contains a meaningful, non-placeholder value that is not in the Recognized Non-Actionable Indicators list.
- `registration_period` contains a recognized no-registration indicator.
- `registration_period` is missing, empty, placeholder-like, or non-actionable, and `uncertain_fields` includes `"registration_period"`.

Under the current schema, no-registration indicators such as `"毋須報名"` are accepted as an exemption because they clearly explain that no registration timing applies.

## Valid Registration Timing Examples

The following examples communicate actionable registration timing and should pass when they appear in `registration_period`:

- `"6月3日上午9時開始報名"`
- `"6月3日至6月10日"`
- `"截止報名日期：6月10日"`
- `"即日起接受報名"`
- `"即日起至額滿"`
- `"額滿即止"`
- `"長期接受報名"`
- `"全年接受報名"`
- `"每月首個工作天開始報名"`
- `"活動前一星期截止"`
- `"電話報名，6月3日起接受報名"`

## Recognized No-Registration Indicators

The following values are accepted as explicit no-registration exemptions:

- `"毋須報名"`
- `"無須報名"`
- `"不用報名"`
- `"免報名"`
- `"無需登記"`
- `"no registration required"`
- `"registration not required"`

Matching rules for no-registration indicators:

- Trim surrounding whitespace before comparison.
- English matching is case-insensitive.
- Chinese matching is exact after trimming.
- Do not use broad substring matching.
- Exact matching is used for now, even when the indicator appears inside a longer sentence.
- Longer sentences such as `"本活動毋須報名，敬請留意"` should not be treated as recognized no-registration indicators unless this specification is later updated to allow contains matching.
- If the sentence is otherwise meaningful and not in the Recognized Non-Actionable Indicators list, it may still pass as actionable registration information under BR-003.

## Recognized Non-Actionable Indicators

The following values are recognized as describing registration method, enquiry instructions, missing timing, or pending status only — not actionable registration timing.

A `registration_period` matching one of these values does not satisfy the Pass Condition and must be listed in `uncertain_fields` unless a separate source-supported timing statement is also present.

- `"電話報名"`
- `"親臨中心報名"`
- `"請向中心職員查詢"`
- `"詳情請致電中心"`
- `"報名日期待定"`
- `"稍後公布"`
- `"通訊未列明報名日期"`

Matching rules for non-actionable indicators:

- Trim surrounding whitespace before comparison.
- English matching is case-insensitive.
- Chinese matching is exact after trimming.
- Do not use broad substring matching.

Values not listed above, not placeholders, and not recognized as no-registration indicators are treated as actionable registration timing.

## Fail Condition

A record fails BR-003 when `registration_period` is missing, empty, placeholder-like, unclear, or non-actionable, and `uncertain_fields` does not include `"registration_period"`.

`"親臨中心報名"` and `"電話報名"` describe registration method only. They do not communicate registration timing and must not pass BR-003 by themselves.

## Overlapping Findings

BR-001 checks whether `registration_period` is meaningful or listed in `uncertain_fields`.

BR-003 checks whether the value is actionable, recognized as no-registration, or explicitly uncertain.

Both rules may emit findings for the same record. For example, an empty `registration_period` with no uncertainty flag may fail BR-001 because the field is not meaningful and fail BR-003 because no registration timing is provided.

## Severity

High. Registration timing affects whether participants can join an activity.

## Example Pass: Specific Start Time

```json
{
  "activity_id": "ACT-001",
  "registration_period": "6月3日上午9時開始報名",
  "uncertain_fields": []
}
```

## Example Pass: No Registration Required

```json
{
  "activity_id": "ACT-002",
  "registration_period": "毋須報名",
  "uncertain_fields": []
}
```

## Example Pass: Unclear Timing Flagged for Review

```json
{
  "activity_id": "ACT-003",
  "registration_period": "請向中心職員查詢",
  "uncertain_fields": ["registration_period"]
}
```

## Example Pass: Method With Timing

```json
{
  "activity_id": "ACT-004",
  "registration_period": "電話報名，6月3日起接受報名",
  "uncertain_fields": []
}
```

## Example Fail: Enquiry Text Only

```json
{
  "activity_id": "ACT-005",
  "registration_period": "請向中心職員查詢",
  "uncertain_fields": []
}
```

## Example Fail: Registration Method Only

```json
{
  "activity_id": "ACT-006",
  "registration_period": "電話報名",
  "uncertain_fields": []
}
```

## Example Fail: Missing Timing Statement

```json
{
  "activity_id": "ACT-007",
  "registration_period": "通訊未列明報名日期",
  "uncertain_fields": []
}
```

## Human Review Guidance

Reviewers should compare `registration_period` against the source document and confirm whether it states when registration opens, closes, remains available, or is not required.

If the source only states a registration method, contact instruction, missing-date note, or pending-status note that appears in the Recognized Non-Actionable Indicators list, mark `registration_period` as uncertain unless a separate source-supported registration timing statement is present.

If the source does not list registration timing, do not infer it from the activity date, the registration method, previous newsletters, or centre practice. Leave the value unresolved and include `"registration_period"` in `uncertain_fields` for human review.
