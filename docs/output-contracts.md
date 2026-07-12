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

## 11. Machine-readable Validation Findings Contract

Label: Validation Findings JSON Contract v1

### Purpose

This contract defines stable JSON artifacts for schema and business validation findings. It makes validation results machine-readable without replacing existing human-readable validator output.

### Scope

This contract covers:

- schema validator findings
- business rule validator findings
- validator execution errors that currently correspond to exit code `2`
- run-level validation failures where record enumeration is impossible

This contract does not cover:

- GPT QA findings JSON
- Human Review decisions JSON
- pipeline runner behavior
- newsletter generation
- BR-006 activation
- schema changes to `schemas/activity.schema.json`

### Artifact Paths

- `data/runs/<run_id>/validation/schema_findings.json`
- `data/runs/<run_id>/validation/business_findings.json`

### Requiredness and Historical Compliance

Before D2B implementation, these artifacts are contract-defined but not yet required.

After D2B implementation is accepted for a validator, that validator's JSON artifact is required for every later committed D1 evidence run that includes that validator stage. This requirement is not retroactive. Runs committed before the corresponding D2B implementation PR is merged are not retroactively non-compliant merely because they lack D2 JSON artifacts.

If an older run is later cited as evidence for a new activation, audit, or review decision, the reviewer may request a new run or follow-up evidence artifact. D2A does not rewrite historical compliance.

The D2B implementation PR must update D1 artifact checklists if JSON artifacts become required D1 evidence artifacts.

### Relationship to Existing Text Output

Human-readable text output remains supported. The JSON artifact is the machine-readable representation of the same validation result.

D2A does not change:

- existing `PASS` / `FAIL` text output
- validator exit code behavior
- the active business rule registry
- validator runtime behavior

### Top-level JSON Object

Each JSON artifact must contain:

- `contract_version`
- `tool`
- `run_id`
- `status`
- `generated_at`
- `source_artifact`
- `findings`

Conditional fields:

- `error` is required when `status` is `error`.
- `message` is required when `status` is `fail` and `findings` is empty.
- `error` must be absent when `status` is `pass` or `fail`.

Top-level field semantics:

- `contract_version` must be `"validation-findings-v1"`.
- `tool` must be one of `"schema_validator"` or `"business_validator"`.
- `run_id` must use the D1 format `YYYY-MM-rNN`.
- `status` must be one of `"pass"`, `"fail"`, or `"error"`.
- `generated_at` must be an ISO 8601 UTC timestamp in the format `YYYY-MM-DDTHH:MM:SSZ`.
- `source_artifact` must reference the validation input artifact path, normally `data/runs/<run_id>/extraction/extracted_activity_records.json`.
- `findings` must be an array.
- `message` describes a run-level validation failure that cannot be represented as per-record findings.

### Status Semantics

When `status` is `pass`:

- `findings` must be empty.
- `error` must be absent.
- `message` may be absent.

When `status` is `fail` for normal validation findings:

- `findings` must contain at least one finding.
- `error` must be absent.
- `message` may be absent.

When `status` is `fail` because record enumeration is impossible:

- `findings` may be empty.
- `error` must be absent.
- `message` must be present.
- This preserves compatibility with existing validator behavior where the validator prints `FAIL` and exits with code `1` for input that is valid JSON but not an array of activity records.
- This exception must not be used to hide per-record findings when records can be enumerated.

When `status` is `error`:

- `findings` must be empty.
- `error` must be present.
- `message` may be absent.

### Finding Object

Each finding must use the fields from Finding Contract v1:

- `index`
- `activity_id`
- `rule_id`
- `field`
- `path`
- `severity`
- `message`
- `recommendation`

D2A does not introduce `finding_id`.

### Severity

Use the existing severity enum:

- `critical`
- `high`
- `medium`
- `low`

### Error Object

When `status` is `error`, `error` must contain:

- `type`
- `target`
- `message`

`error.type` must be one of:

- `invalid_arguments`
- `file_not_found`
- `unreadable_file`
- `invalid_json`
- `invalid_schema`
- `execution_error`

`error.target` must be one of:

- `arguments`
- `input`
- `schema`
- `runtime`

Error semantics:

- Use `invalid_schema` when the schema file exists and is readable JSON but fails schema validation as a schema.
- Use `execution_error` only when the failure does not fit a narrower error type.
- An `OSError` while reading input or schema files must use `type: "unreadable_file"` and `target: "input"` or `target: "schema"`, as applicable.
- Unexpected non-file runtime exceptions must use `type: "execution_error"` and `target: "runtime"`.

Error mapping:

| Condition | `error.type` | `error.target` |
| --- | --- | --- |
| Input file not found | `file_not_found` | `input` |
| Schema file not found | `file_not_found` | `schema` |
| Input permission or read error | `unreadable_file` | `input` |
| Schema permission or read error | `unreadable_file` | `schema` |
| Input invalid JSON | `invalid_json` | `input` |
| Schema invalid JSON | `invalid_json` | `schema` |
| Schema exists but fails schema validation | `invalid_schema` | `schema` |
| Argument parsing or invalid invocation | `invalid_arguments` | `arguments` |
| Unexpected runtime failure | `execution_error` | `runtime` |

### Pass Artifact Rule

Once D2B is implemented for a validator, a successful validation must still produce that validator's JSON artifact. Machine consumers must be able to distinguish "validator passed" from "validator did not run".

### Examples

#### Pass Artifact

```json
{
  "contract_version": "validation-findings-v1",
  "tool": "schema_validator",
  "run_id": "2026-07-r01",
  "status": "pass",
  "generated_at": "2026-07-11T08:30:00Z",
  "source_artifact": "data/runs/2026-07-r01/extraction/extracted_activity_records.json",
  "findings": []
}
```

#### Run-level Fail Artifact

```json
{
  "contract_version": "validation-findings-v1",
  "tool": "business_validator",
  "run_id": "2026-07-r02",
  "status": "fail",
  "generated_at": "2026-07-11T08:45:00Z",
  "source_artifact": "data/runs/2026-07-r02/extraction/extracted_activity_records.json",
  "findings": [],
  "message": "Validation input is valid JSON but is not an array of activity records."
}
```

#### Error Artifact: Invalid Schema

```json
{
  "contract_version": "validation-findings-v1",
  "tool": "schema_validator",
  "run_id": "2026-07-r03",
  "status": "error",
  "generated_at": "2026-07-11T09:00:00Z",
  "source_artifact": "data/runs/2026-07-r03/extraction/extracted_activity_records.json",
  "findings": [],
  "error": {
    "type": "invalid_schema",
    "target": "schema",
    "message": "The schema file is readable JSON but is not a valid JSON Schema."
  }
}
```

### D2B Implementation Notes

D2B rejects incomplete or malformed business findings at the JSON boundary instead of silently masking them with normalization defaults. An invariant failure produces an `execution_error` runtime artifact when a valid artifact invocation is available.

Invalid arguments are handled before artifact emission: print a human-readable error to stderr, exit `2`, and write no JSON artifact. A contract-compliant artifact cannot be emitted without a valid `run_id`.

### D2A Scope Guardrails

D2A must not:

- implement JSON output
- change human-readable text output
- change validator exit codes
- define GPT QA findings JSON
- define Human Review decisions JSON
- implement or modify a pipeline runner
- activate BR-006
- change the active business rule registry
- change `schemas/activity.schema.json`
