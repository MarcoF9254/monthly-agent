# Interim Run Summary

**Run status: PENDING HUMAN REVIEW / OWNER CLOSURE**

This is an interim D1 summary for replacement evidence run `2026-06-r02`. No final D1 run outcome has been assigned.

## Source and lineage

- Run ID: `2026-06-r02`
- Programme month: `2026-06`
- Immutable baseline run: `2026-06-r01`
- Baseline merge commit: `b0b5f4bb94b8bfac84e89fa1bf79965e883fbfe3`
- Implementation strategy: `docs/run-strategies/2026-06-r02-correction-strategy.md`
- Sole authoritative source: `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`
- Source SHA-256: `7DC41C29D5F492E32FF57122066E4753075EF369A4DD01E7EDAC4D14E8751C48`
- Source file size: 1,766,478 bytes
- Excluded sources: spreadsheet, drafts, blank form, ZIP files, and every non-authoritative source.
- No source original was copied into r02; `source/originals/` contains only `.gitkeep`.

## Artifact inventory

- `source/source_manifest.json`
- `source/originals/.gitkeep`
- `extraction/extracted_activity_records.json`
- `validation/schema_validation.txt`
- `validation/schema_findings.json`
- `validation/business_validation.txt`
- `validation/business_findings.json`
- `qa/qa_review_notes.md`
- `human-review/human_review_decisions.md`
- `run_summary.md`

## Extraction and mutation scope

- Total records: 45
- Unique activity IDs: 45
- Carried records: 32, preserving their r01 activity IDs.
- HR-003 corrections: exactly 10 `source_reference`-only changes keyed by exact activity ID and exact current r01 value.
- HR-002 additions: exactly 13 page-10 records, IDs `2026-06-r02-033` through `2026-06-r02-045`.
- Unapproved differences in the first 32 records: 0.
- All 45 records remain `qa_status: "pending"`.
- Approved HR-001 and amended HR-002 exclusions remain absent.
- HR-004 slash/free semantics are preserved exactly.

## Construction execution note

All in-memory mutation assertions passed before the first r02 write. After the initial manifest, extraction, Human Review lineage, and `.gitkeep` were written, a console-only reporting expression failed because shell quoting removed dictionary-key quotes. The initial artifacts were not overwritten or regenerated. Read-only verification then confirmed 45 records, 45 unique IDs, 10 approved metadata corrections, 13 approved additions, zero unapproved differences, and zero excluded titles before validation.

## Validation

- Pre-validation extraction SHA-256: `57511548C647CE1ADB8F1AC9BE62B111CC9F8D79DB6585F05762817D9D3DAE0F`
- Schema command: `python tools/validate_schema.py data/runs/2026-06-r02/extraction/extracted_activity_records.json --run-id 2026-06-r02 --json-output data/runs/2026-06-r02/validation/schema_findings.json`
- Schema exit code: 0; text PASS; JSON `pass`; findings: 0.
- Business command: `python tools/validate_business_rules.py data/runs/2026-06-r02/extraction/extracted_activity_records.json --run-id 2026-06-r02 --json-output data/runs/2026-06-r02/validation/business_findings.json`
- Business exit code: 0; text PASS; JSON `pass`; findings: 0.
- Active registry: BR-001 through BR-005 only; BR-006 findings: 0.
- Validation Findings JSON Contract v1: PASS for both artifacts.
- The first contract-check attempt had a shell quoting syntax error and did not read or modify artifacts; the corrected command passed.
- Post-validation extraction SHA-256: `57511548C647CE1ADB8F1AC9BE62B111CC9F8D79DB6585F05762817D9D3DAE0F`
- Pre/post hashes are identical; validators did not mutate extraction.

## Fresh GPT QA

- All 10 PDF pages visually inspected; the PDF remains authoritative.
- Records accounted for: 45 of 45.
- Missing in-scope activities: 0; duplicates: 0; unsupported inference findings: 0; source conflicts: 0.
- Proposed extraction mutations: 0.
- Retained calendar uncertainty observations: 13.
- New Human Review source questions: 0.
- QA remained recommendation-only and did not mutate the validated extraction.

## Human Review and closure boundary

- HR-001 through HR-004 are implemented and recorded for r02.
- No new source ambiguity was identified by fresh QA.
- Owner record-state decisions and final closure remain pending.
- No approval artifact exists and no final D1 outcome is assigned.

## Guardrails

- BR-006 did not execute and remains inactive.
- D3 remains unresolved.
- No pipeline runner or FormatChecker was implemented.
- r01 was not modified.
- r02 has not been committed, pushed, published, or submitted in a pull request.

## 2026-07-14 evidence-status addendum — HR-005

- Owner-approved HR-005 determines that page-10 text `地點：中心活動室` belongs only to the separate `6月份例會日期及時間` notice, not to the calendar-only activities.
- The earlier Fresh GPT QA claims of zero unsupported inference, zero new Human Review questions, and a calendar-wide venue are inaccurate and are superseded by the dated addendum in `qa/qa_review_notes.md`; the original claims remain preserved as first observed.
- Records `2026-06-r02-033` through `2026-06-r02-045` contain the unsupported venue value `中心活動室` and omit required `venue` uncertainty.
- R02 is not closure-ready and closure is held.
- R02 extraction and validation evidence remain preserved exactly; no r02 record was corrected, no validator was rerun, and no `qa_status` changed.
- No partial approval, approval artifact, or final D1 outcome is authorized.
- The correction is planned only in `docs/run-strategies/2026-06-r03-correction-strategy.md`; creating or implementing r03 requires separate owner authorization.
