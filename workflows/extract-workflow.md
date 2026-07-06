# Extract Workflow

## 1. Purpose

Define a practical end-to-end workflow for extracting activity information from elderly centre monthly programme documents into structured records that can be validated, QA checked, reviewed by humans when needed, and later used for newsletter preparation.

The workflow prioritizes accuracy over completeness. Missing, unclear, or ambiguous source details must be preserved as uncertainty rather than guessed.

## 2. Inputs

- Source monthly programme documents, images, PDFs, or exported text stored under `data/input/`.
- Extraction prompt: `prompts/extract-activity-info.md`.
- Activity schema: `schemas/activity.schema.json`.
- Any source context needed to interpret tables, captions, footnotes, legends, or registration notices.

## 3. Outputs

- Structured activity records saved under `data/output/`.
- Each record should follow `schemas/activity.schema.json`.
- Each newly extracted record should use `qa_status: "pending"`.
- Each record should include source-supported practical details where available, such as activity title, date, time, venue, fee, quota, eligibility, registration period, and remarks.
- Missing, unclear, or ambiguous fields should be listed in `uncertain_fields`.

## 4. Step-by-Step Workflow

1. Place the raw source document or exported source text in `data/input/`.
2. Review the source layout before extraction, noting tables, merged cells, captions, footnotes, registration instructions, and repeated date or fee patterns.
3. Run the Extract Agent using `prompts/extract-activity-info.md`.
4. Extract one structured record per activity unless the source clearly describes a single activity with multiple dates, sessions, or fee types.
5. Preserve source wording for titles, dates, times, fees, venues, eligibility, quotas, and registration details where possible.
6. Do not infer missing details from similar activities unless the source explicitly supports the value.
7. Mark unclear or missing details in `uncertain_fields`.
8. Save the extraction result under `data/output/`.
9. Validate the output against `schemas/activity.schema.json`.
10. Hand the validated extraction output and original source to the QA Agent.
11. Send unresolved QA findings to Human Review.
12. Use only records that have passed QA or Human Review for downstream newsletter generation.

## 5. Extract Agent Responsibility

The Extract Agent is responsible for converting the source monthly programme document into structured activity records.

The Extract Agent must:

- Capture every identifiable activity from the source.
- Preserve the original meaning and practical details.
- Support multiple dates, times, fee types, venues, and registration details when the source includes them.
- Set `qa_status` to `pending` for new records.
- Add unclear, missing, or ambiguous fields to `uncertain_fields`.
- Avoid inventing activity details, normalizing away important wording, or silently resolving ambiguity.

## 6. Schema Validation Step

After extraction, validate the output against `schemas/activity.schema.json`.

Validation should confirm:

- The output is valid structured data.
- Required fields are present.
- Field types match the schema.
- Multi-value fields use the expected structure.
- `qa_status` is set to `pending` for newly extracted records.
- `uncertain_fields` is present when source information is missing, unclear, or ambiguous.

If validation fails, fix only the structural issue needed to make the record schema-compliant. Do not add unsupported source details during schema correction.

## 7. QA Handoff

The QA handoff should include:

- The original source document or exported text from `data/input/`.
- The extracted structured records from `data/output/`.
- Any notes about source layout, unclear rows, footnotes, or fields already listed in `uncertain_fields`.

The QA Agent should compare every extracted field against source evidence, identify missing activities, duplicates, incorrect values, unsupported assumptions, and misleading practical-detail errors.

## 8. Human Review Handoff

Send records to Human Review when:

- The source text is unclear, incomplete, or conflicting.
- A table row, caption, merged cell, or footnote cannot be confidently mapped to an activity.
- A key practical detail such as date, time, fee, venue, eligibility, quota, or registration period is missing or ambiguous.
- QA identifies an issue that cannot be resolved from the source alone.

Human Review should decide the final handling of unresolved fields, update the record if needed, and change `qa_status` only when the record is ready.

## 9. Failure Cases

Common failure cases include:

- Source document is missing, unreadable, incomplete, or placed outside `data/input/`.
- OCR or exported text omits rows, columns, footnotes, or Chinese punctuation needed for interpretation.
- Activity boundaries are unclear, causing one activity to be split incorrectly or multiple activities to be merged.
- Dates, times, fees, venues, eligibility, or registration details are inferred without source support.
- Multi-date or multi-fee activities are flattened into a single misleading value.
- Extracted records do not match `schemas/activity.schema.json`.
- QA cannot trace extracted values back to the source.

When a failure occurs, keep the affected fields uncertain, document the issue, and route the record to QA or Human Review instead of guessing.

## 10. Definition of Done

The extraction workflow is done when:

- The source document is stored under `data/input/`.
- All identifiable activities have corresponding structured records.
- The extraction output is saved under `data/output/`.
- Records validate against `schemas/activity.schema.json`.
- New records have `qa_status: "pending"`.
- Missing, unclear, or ambiguous details are listed in `uncertain_fields`.
- The original source and extracted records are ready for QA handoff.
- Any unresolved source interpretation issues are clearly marked for Human Review.
