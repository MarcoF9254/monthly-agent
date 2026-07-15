# Project Plan

## Objective

Build a repeatable workflow for extracting activity information from elderly centre monthly programme documents, checking the extracted information, and preparing reliable structured data for newsletter generation.

## Scope

The first version focuses on:

- Collecting source monthly programme documents.
- Extracting structured activity records.
- Running QA checks against source material.
- Producing clean output files that can later feed newsletter generation.

## Proposed Workflow

1. Add source files to `data/input/`.
2. Use `prompts/extract-activity-info.md` to extract activity records.
3. Save structured extraction results to `data/output/`.
4. Use `prompts/qa-check-monthly-info.md` to check completeness and accuracy.
5. Resolve flagged issues.
6. Mark record review state independently from consumer-specific newsletter authorization.

## Data Quality Priorities

- Correct dates, times, venues, and fees.
- Clear distinction between confirmed and uncertain information.
- Traceability back to source text or page references.
- Consistent field names and output format.

## Future Enhancements

- Add sample input and output files.
- Define a formal JSON schema for activity records.
- Add automated validation checks.
- Add newsletter generation prompts and templates.
- Add regression examples for prompt changes.
