# Interim Run Summary

**Run status: PENDING HUMAN REVIEW / OWNER CLOSURE**

This is an interim D1 summary. No final D1 run outcome has been assigned.

## Source

- Run ID: `2026-06-r01`
- Programme month: `2026-06`
- Sole authoritative source: `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`
- SHA-256: `7DC41C29D5F492E32FF57122066E4753075EF369A4DD01E7EDAC4D14E8751C48`
- File size: 1,766,478 bytes
- Excluded: `examples/architecture-review/2026-06/excel/6月一覽表n1.xlsm`, all `examples/architecture-review/2026-06/drafts/*`, and the blank form.
- No original source was copied into the run directory.

## Temporary Rendering Environment

- Virtual environment: `%TEMP%\monthly-agent-pdf-render-venv`
- Render directory: `%TEMP%\monthly-agent-2026-06-r01-pages`
- Python: 3.14.6
- pip: 26.1.2
- PyMuPDF: 1.26.3
- Installation command: `python -m pip install PyMuPDF==1.26.3` executed through the temporary environment's Python.
- Rendering: all 10 pages rendered at 180 DPI using PyMuPDF `Page.get_pixmap()`.
- Visual inspection: complete; no blank, corrupt, clipped, or unreadable page.
- Layout note: text extraction order differed materially from visual panel order on pages 2-6 and from the rotated calendar layout on page 10; visual layout governed interpretation.
- Cleanup: pending; temporary environment and rendered pages remain outside the repository for owner review/debugging.

## Artifact Inventory

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

## Extraction

- Record count: 32
- Unique activity IDs: 32
- All records remain `qa_status: "pending"`.
- HR-002 is owner-approved with amendments: 13 calendar-only labels are approved for future inclusion; 愛心午餐服務 and 早晨包包 join 「活動抽籤」 and 「活動報名」 as excluded workflow/routine-service items. No calendar record has been added.
- HR-001-B excludes the four page-9 milk-powder company notices as commercial product-purchase arrangements for this run and any directly derived replacement run using the same source.
- No excluded source was used.

## Validation Commands and Results

Schema command:

```powershell
python tools/validate_schema.py data/runs/2026-06-r01/extraction/extracted_activity_records.json --run-id 2026-06-r01 --json-output data/runs/2026-06-r01/validation/schema_findings.json
```

- Exit code: 0
- Text status: PASS
- JSON status: `pass`
- Finding count: 0

Business command:

```powershell
python tools/validate_business_rules.py data/runs/2026-06-r01/extraction/extracted_activity_records.json --run-id 2026-06-r01 --json-output data/runs/2026-06-r01/validation/business_findings.json
```

- Exit code: 1
- Text status: FAIL
- JSON status: `fail`
- Finding count: 10
- Finding rules: BR-005 only
- BR-006 findings: 0

JSON contract-check command:

```powershell
python -c "import json, sys; from pathlib import Path; from tools.validation_findings_json import validate_validation_artifact; [validate_validation_artifact(json.loads(Path(p).read_text(encoding='utf-8-sig'))) for p in sys.argv[1:]]; print('PASS')" data/runs/2026-06-r01/validation/schema_findings.json data/runs/2026-06-r01/validation/business_findings.json
```

- Exit code: 0
- Result: PASS
- Text, JSON, and validator exit semantics agree.

## Non-mutation Check

- Extraction SHA-256 before validation: `2AF185BE9F2D181C9A9660BDCAC856F92F00552FD809672B32324701A1B20554`
- Extraction SHA-256 after validation: `2AF185BE9F2D181C9A9660BDCAC856F92F00552FD809672B32324701A1B20554`
- Result: validators did not mutate the extraction artifact.

## QA and Human Review

- QA actionable finding groups: 13 (10 record-level BR-005 findings plus 3 QA groups).
- Missing/duplicate review: 2 grouped scope questions; 0 duplicates.
- Human Review decisions approved: 4 (HR-001-B, amended HR-002, HR-003-A, HR-004-B).
- Unresolved Human Review decisions: 0.
- The HR-002 owner-decision matrix is present at `human-review/hr002_calendar_inclusion_matrix.md`; its 13 approved additions remain unimplemented and `2026-06-r02` has not been created.
- HR-003 corrections are authorized as future traceability-metadata corrections but remain unapplied. The recommendation-only r02 strategy is at `docs/run-strategies/2026-06-r02-correction-strategy.md`; implementation has not started.
- GPT QA approved records: 0; QA remained recommendation-only.
- No proposed correction was applied to the validated extraction.

## Missing or Conditional Artifacts

- `approval/approved_records.json`: not created; not authorized and no approval decision exists.
- `approval/blocked_records.md`: not created; not authorized and no final run outcome exists.
- `approval/blocked_run_summary.md`: not created; not authorized and no final run outcome exists.
- No empty approval artifacts were created.

## Boundaries

- BR-006 did not execute and remains absent from the runtime registry.
- This run does not activate BR-006.
- D3 remains unresolved.
- No pipeline runner or FormatChecker was implemented.
- The run has not been committed, pushed, published, or submitted as a pull request.
- Owner Human Review and final closure remain pending.

