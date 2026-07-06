# Schema Validation

## Purpose

Schema validation checks whether extracted monthly programme activity records are structurally valid before QA review or downstream newsletter use.

This validation does not decide whether the content is correct. It only confirms that the data shape, required fields, field types, and allowed values match the project schema.

## Input

- Extracted activity records, usually saved under `data/output/`.
- The schema file: `schemas/activity.schema.json`.

The input may be a single activity record or a collection of activity records, depending on the extraction output format used for a task.

## Output

Schema validation should produce one of the following:

- Pass: the record or records match the schema.
- Fail: one or more records do not match the schema.

For failures, the output should include:

- The affected record or activity identifier when available.
- The field path with the issue.
- The validation error message.
- The expected type, required field, or allowed value when available.

## Use of `schemas/activity.schema.json`

`schemas/activity.schema.json` is the source of truth for the activity record structure.

Validation should check:

- All required fields are present.
- No unsupported top-level fields are added.
- Field values use the expected types.
- `dates` is an array with at least one date object.
- Each date object includes `date_text`.
- `fee` is an array with at least one fee object.
- Each fee object includes `fee_type` and `amount_text`.
- `qa_status` uses one of the allowed values: `pending`, `approved`, `needs_review`, or `rejected`.
- `uncertain_fields` is an array with unique string values.

## Pass Criteria

A record passes schema validation when:

- It contains every required field.
- Every field matches the type defined in `schemas/activity.schema.json`.
- Nested `dates` and `fee` entries match their required structures.
- No additional top-level or nested object properties are present where the schema disallows them.
- `qa_status` is one of the schema-approved values.

## Fail Criteria

A record fails schema validation when:

- A required field is missing.
- A field has the wrong type.
- A nested date or fee object is missing a required field.
- An unexpected property is present.
- `qa_status` has a value outside the schema enum.
- `dates`, `fee`, or another required array is empty when the schema requires at least one item.

## Example Validation Errors

- Missing required field:
  - Record `sample-2026-04-001` is missing `source_reference`.
- Wrong field type:
  - `quota` is `20`, but the schema expects a string such as `"20人"`.
- Invalid QA status:
  - `qa_status` is `"checked"`, but allowed values are `pending`, `approved`, `needs_review`, and `rejected`.
- Missing nested field:
  - `dates[0]` is missing required field `date_text`.
- Unexpected property:
  - `fee[0]` contains unsupported property `discount_code`.
- Empty required array:
  - `fee` is empty, but at least one fee entry is required.