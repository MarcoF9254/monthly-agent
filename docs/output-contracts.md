# Output Contracts

## 1. Purpose

Define lightweight shared output contracts for monthly-agent validation tools.

These contracts keep schema validation, business rule validation, QA review, and future regression tests consistent enough to compare results across tools.

## 2. Severity Enum

Validation findings should use one of these severity values:

- `critical`
- `high`
- `medium`
- `low`

Use `high` for participant-facing practical errors such as incorrect date, time, fee, venue, quota, eligibility, or registration details.

## 3. Schema Validator Output Contract

The schema validator checks extracted activity records against `schemas/activity.schema.json`.

Expected output:

- Print `PASS` when all records are schema-valid.
- Print `FAIL` when any record has one or more schema violations.
- On failure, print one finding per schema violation.
- Include record index and `activity_id`; use `"<missing>"` when `activity_id` is missing.
- Use `rule_id: "SCHEMA"`.
- Use `severity: "critical"`.
- Use recommendation: `Fix the JSON structure so the record validates against schemas/activity.schema.json.`
- Do not apply business rules.

## 4. Business Validator Output Contract

The business validator checks workflow and participant-facing rules that go beyond JSON schema.

Expected output:

- Print `PASS` when all records pass business rules.
- Print `FAIL` when any record violates one or more business rules.
- On failure, print one finding per business rule violation.
- Include the business rule ID, affected field, severity, and recommendation.
- Support only pass/fail status for now.
- Do not replace QA or Human Review decisions.

Business findings should use rule IDs from `rules/`, such as `BR-001`.

## 5. Uncertain Fields Semantics

`uncertain_fields` remains an array of strings.

A string may be either:

- a top-level field name, such as `fee` or `registration_period`
- an approved deterministic indexed path, such as `dates[1].date_text`

Indexed paths are allowed only when an accepted rule specification explicitly requires per-element uncertainty marking.

Approved indexed path shape:

```text
<field>[<zero-based-index>].<subfield>
```

Top-level markers remain valid for rules that define top-level uncertainty behavior.

Do not treat `uncertain_fields` as full JSONPath.

Do not support wildcards, ranges, regex, fuzzy paths, or semantic paths.

This is documentation semantics only; no structural `schemas/activity.schema.json` change is required because `uncertain_fields.items` is already `type: string`.

Finding `path` may use detailed indexed paths. `uncertain_fields` may reuse the same narrow path vocabulary only where approved.

## 6. Finding Object Fields

Label: Finding Contract v1

When a validator emits structured findings, each finding should use these fields:

- `index`: zero-based record index in the input array.
- `activity_id`: activity identifier when available, otherwise the string `"<missing>"`.
- `rule_id`: rule identifier such as `SCHEMA`, `BR-001`, or `BR-002`.
- `field`: affected top-level field derived from `path`, such as `fee` for `fee[0].amount`.
- `path`: detailed field path, such as `fee[0].amount`.
- `severity`: one of `critical`, `high`, `medium`, or `low`.
- `message`: concise explanation of the problem.
- `recommendation`: practical next step for correction, QA, or Human Review.

If the error path is the record root, use `field: "<record>"` and `path: "<record>"`.

## 7. Pass / Fail Behavior

The current validator status enum is:

- `pass`
- `fail`

Validation passes when no findings are produced.

Validation fails when one or more findings are produced, regardless of severity.

Warning-only mode is not implemented yet. It may be added in the future if a workflow explicitly supports warnings that do not fail validation.

## 8. Exit Code Behavior

- Exit code `0`: validation passed.
- Exit code `1`: validation failed.
- Exit code `2`: validator could not run because of invalid arguments, unreadable files, invalid JSON, missing schema, or other tool execution errors.

## 9. Example PASS Output

```text
PASS
```

## 10. Example FAIL Output

```text
FAIL
Record 3 (activity_id: sample-2026-04-004), rule_id: SCHEMA, field: fee, path: fee[0].amount, severity: critical
Message: None is not of type 'number'.
Recommendation: Fix the JSON structure so the record validates against schemas/activity.schema.json.
```
