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

- `registration_period` contains source-supported registration timing.
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

## Fail Condition

A record fails BR-003 when `registration_period` is missing, empty, placeholder-like, unclear, or non-actionable, and `uncertain_fields` does not include `"registration_period"`.

The following examples are unclear or non-actionable for BR-003 unless `registration_period` is marked uncertain:

- `"請向中心職員查詢"`
- `"詳情請致電中心"`
- `"報名日期待定"`
- `"稍後公布"`
- `"通訊未列明報名日期"`
- `"親臨中心報名"`
- `"電話報名"`

`"親臨中心報名"` and `"電話報名"` describe registration method only. They do not communicate registration timing and must not pass BR-003 by themselves.

## Interaction With BR-001

BR-001 checks whether `registration_period` is meaningful or listed in `uncertain_fields`.

BR-003 checks whether the value actually communicates registration timing or a recognized no-registration exemption.

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

## Example Fail: Enquiry Text Only

```json
{
  "activity_id": "ACT-004",
  "registration_period": "請向中心職員查詢",
  "uncertain_fields": []
}
```

## Example Fail: Registration Method Only

```json
{
  "activity_id": "ACT-005",
  "registration_period": "電話報名",
  "uncertain_fields": []
}
```

## Human Review Guidance

Reviewers should compare `registration_period` against the source document and confirm whether it states when registration opens, closes, remains available, or is not required.

If the source only states a registration method, contact instruction, or vague enquiry note, mark `registration_period` as uncertain unless a separate source-supported registration timing statement is present.

If the source does not list registration timing, do not infer it from the activity date, the registration method, previous newsletters, or centre practice. Leave the value unresolved and include `"registration_period"` in `uncertain_fields` for human review.
