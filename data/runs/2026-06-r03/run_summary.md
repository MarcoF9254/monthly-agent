# Interim Run Summary

**Run status: PENDING HUMAN REVIEW / OWNER CLOSURE**

This is an interim D1 summary for replacement evidence run `2026-06-r03`. No record approval or final D1 outcome has been assigned.

## Source and lineage

- Programme month: `2026-06`.
- Sole authoritative source: `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`.
- Source SHA-256: `7DC41C29D5F492E32FF57122066E4753075EF369A4DD01E7EDAC4D14E8751C48`; size: 1,766,478 bytes.
- Direct parent: preserved, non-closure-ready `2026-06-r02`; initial evidence baseline: preserved `2026-06-r01`.
- Authority: owner-approved HR-005 and `docs/run-strategies/2026-06-r03-correction-strategy.md`.
- No source original was copied into r03. Spreadsheets, drafts, blank forms, ZIPs, and other non-authoritative sources were excluded.

## R02 preservation identities

- Committed Git LF identity: `88F32202E7C16AA000ADEE6440C29555E1D1F148E8A80657BE0944FEC999666F`.
- Historical Windows CRLF validator-execution identity: `57511548C647CE1ADB8F1AC9BE62B111CC9F8D79DB6585F05762817D9D3DAE0F`.
- These byte hashes are not equal; the representations parse as semantically identical JSON.
- No r01 or r02 file was modified.

## Extraction and exact mutation scope

- Records: 45; unique IDs: 45; pending statuses: 45.
- Records 001–032: zero field changes.
- Records 033–045: exactly 13 `venue` replacements from `中心活動室` to empty string and exactly 13 additions of `venue` to `uncertain_fields`.
- Changed records: 13; unchanged records: 32; total authorized effects: 26; unapproved differences: 0.
- HR-001 through HR-004 remain in force; HR-005 is implemented exactly.

## Validation

- Pre-validation extraction SHA-256: `0C1262A144EDE7142390B8FC676D255726C6701991D2EADCACAF612448A3172C`.
- Schema command: `python tools/validate_schema.py data/runs/2026-06-r03/extraction/extracted_activity_records.json --run-id 2026-06-r03 --json-output data/runs/2026-06-r03/validation/schema_findings.json`.
- Schema result: PASS; exit code 0; JSON status `pass`; findings 0; Validation Findings JSON Contract v1 PASS.
- Business command: `python tools/validate_business_rules.py data/runs/2026-06-r03/extraction/extracted_activity_records.json --run-id 2026-06-r03 --json-output data/runs/2026-06-r03/validation/business_findings.json`.
- Business result: PASS; exit code 0; JSON status `pass`; findings 0; Validation Findings JSON Contract v1 PASS.
- Text status, JSON status, finding count, and exit semantics agree for both validators.
- Active registry: BR-001 through BR-005 only. BR-006 was inactive and produced no finding.
- Post-validation extraction SHA-256: `0C1262A144EDE7142390B8FC676D255726C6701991D2EADCACAF612448A3172C`.
- Pre/post hashes are identical; validators did not mutate the extraction. Each validator was executed exactly once.

## Fresh QA and Human Review

- All ten authoritative PDF pages and all 45 records were freshly reviewed.
- Missing in-scope activities: 0; duplicates: 0; source-reference traceability: 45/45.
- HR-003 corrections and HR-004 fee handling remain correct; approved exclusions remain absent.
- All 13 calendar additions match their visible titles, dates, and times.
- Page 10 visually confirms `地點：中心活動室` belongs only to the separate centre-meeting notice. All 13 target venues are empty and marked uncertain; no calendar-wide venue is inferred.
- Unsupported participant-facing inference findings: 0; proposed post-validation mutations: 0.
- HR-001 through HR-004 are carried forward and HR-005 is recorded as implemented.
- New unresolved Human Review questions: none. Record states and closure remain pending.

## Guardrails

- No approval directory or artifact exists; no final D1 outcome is assigned.
- BR-006 remains inactive. No D3, pipeline-runner, or FormatChecker work is included.
- At the time the pre-closure evidence was completed, r03 had not yet been committed or submitted for review. Evidence completion alone did not approve records or authorize downstream use.

**Pre-closure run status at evidence completion: PENDING HUMAN REVIEW / OWNER CLOSURE**

## Owner closure - partial approval

**Final run status: PARTIALLY APPROVED - OWNER CLOSURE COMPLETE**

- Final D1 outcome: `partially_approved`.
- Approved: 32; `needs_review`: 13; pending: 0; rejected: 0.
- Approved IDs: `2026-06-r01-001` through `2026-06-r01-032`.
- Withheld IDs: `2026-06-r02-033` through `2026-06-r02-045`.
- Validated pre-closure extraction identity: `0C1262A144EDE7142390B8FC676D255726C6701991D2EADCACAF612448A3172C`.
- Closed extraction SHA-256 after the authorized `qa_status` transitions: `930F2A5CE090CE085890A1CD6270C942BC7ED0C5D1769D13455790484E1D579B`.
- The hashes differ because owner-authorized workflow-state transitions occurred after validation. Validator evidence applies to the validated pre-closure extraction; owner closure authority establishes the final record states. No validator was rerun after closure.
- `approval/approved_records.json` contains exact closed-extraction copies of the 32 approved records in original order.
- `approval/blocked_records.md` accounts for all 13 withheld records.
- `approval/blocked_run_summary.md` is intentionally absent because no unresolved run-level blocker exists.
- For approved records, downstream use is limited to source-supported fields. Every field named in `uncertain_fields` must be omitted without semantic substitution or affirmative inference.
- Calendar-only records 033-045 remain withheld from approved-only downstream use pending separately governed limited-use policy work. They are not rejected for factual inaccuracy.
- Closure changed only `qa_status`; no source-derived participant-facing field or uncertainty marker changed.
- At the time of owner closure implementation, r03 had not yet been committed or submitted for review.
