# QA Workflow

## 1. Purpose

Define a practical workflow for checking extracted elderly centre monthly programme activity records against the original source document.

The QA workflow exists to confirm that every extracted value is supported by the source, identify missing or duplicate activities, flag misleading practical-detail errors, and prepare unresolved items for Human Review.

## 2. Inputs

- Original monthly programme source document, image, PDF, or exported text from `data/input/`.
- Extracted structured activity records from `data/output/`.
- QA prompt: `prompts/qa-check-monthly-info.md`.
- Activity schema: `schemas/activity.schema.json`.
- Any extraction notes about unclear source layout, table structure, captions, footnotes, merged cells, or uncertain fields.

## 3. Outputs

- QA findings for each reviewed activity record.
- Updated `qa_status` values where appropriate.
- A list of missing activities, duplicate records, unsupported values, and source interpretation issues.
- Severity labels for identified issues.
- Human Review notes for records that cannot be confidently resolved by QA alone.

## 4. Step-by-Step QA Workflow

1. Confirm the original source file and extracted records are available.
2. Review the source layout before checking records, including tables, section headings, captions, footnotes, registration instructions, and repeated values.
3. Validate that extracted records follow `schemas/activity.schema.json`.
4. Compare the list of extracted activity titles against the source to identify missing activities or duplicate records.
5. For each record, check every field against source evidence.
6. Confirm practical participant details, including date, time, venue, fee, quota, eligibility, registration period, and remarks.
7. Check that multi-date, multi-session, multi-fee, and multi-venue activities have not been flattened into misleading single values.
8. Confirm that unclear, missing, or ambiguous details are listed in `uncertain_fields`.
9. Flag unsupported inferences, normalized wording that changes meaning, and values copied from nearby rows without source support.
10. Assign a severity level to each issue.
11. Mark records as approved only when key fields are source-supported and no unresolved high-impact issues remain.
12. Send unresolved or ambiguous cases to Human Review with concise notes and source references.

## 5. Severity Levels

- `critical`: The record should not be used downstream because the activity identity is wrong, the record describes an activity not supported by the source, or multiple activities have been incorrectly merged in a way that cannot be safely corrected without review.
- `high`: A key participant-facing detail is wrong, missing, or misleading, such as date, time, venue, fee, eligibility, quota, or registration period.
- `medium`: A non-key field is incorrect, incomplete, or ambiguous, or a key detail needs clarification but is already clearly marked in `uncertain_fields`.
- `low`: Formatting, wording, or minor consistency issue that does not change source meaning or participant instructions.

## 6. Common Issue Types

- Missing activity from the extraction output.
- Duplicate activity record.
- Incorrect activity title or title copied from the wrong row.
- Wrong date, time, venue, fee, quota, eligibility, or registration period.
- Missing practical detail that is present in the source.
- Unsupported value inferred from another activity or repeated table pattern.
- Multi-date, multi-session, multi-fee, or multi-venue information flattened into a misleading value.
- Source footnote, caption, heading, or registration instruction not applied correctly.
- Ambiguous source detail not listed in `uncertain_fields`.
- Record does not comply with `schemas/activity.schema.json`.
- `qa_status` set to approved before source support is confirmed.

## 7. Human Review Handoff

Send a record or issue to Human Review when:

- The source is unreadable, incomplete, conflicting, or too ambiguous for QA to resolve.
- It is unclear whether a table row, merged cell, caption, or footnote applies to one activity or multiple activities.
- A key participant-facing detail is missing from the source but required for downstream use.
- QA finds conflicting evidence for date, time, venue, fee, eligibility, quota, or registration period.
- Correcting the issue would require interpretation beyond direct source evidence.

Human Review notes should include:

- The affected record.
- The field or issue needing review.
- The relevant source location or wording when available.
- The QA severity.
- The specific decision needed.

## 8. Definition of Done

The QA workflow is done when:

- The original source and extracted records have both been reviewed.
- Every extracted record has been checked against source evidence.
- Missing activities and duplicate records have been identified.
- Incorrect, unsupported, unclear, or misleading fields have QA findings with severity levels.
- Records are marked approved only when key fields are source-supported.
- Unresolved issues are clearly routed to Human Review.
- The reviewed output is ready for correction or record approval according to `qa_status`. Downstream use additionally requires applicable consumer policy and scoped eligibility.
