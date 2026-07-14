# R03 Correction Strategy — HR-005 Page-10 Venue Scope

- Source lineage: `2026-06-r01` → preserved `2026-06-r02` → proposed `2026-06-r03`
- Programme month: `2026-06`
- Strategy status: `IMPLEMENTATION NOT AUTHORIZED`
- Current r02 status: `NOT CLOSURE-READY — CLOSURE HELD`
- Document scope: documentation-only repository planning artifact; not an r03 run artifact and not implementation authorization.

This strategy records the exact proposed replacement-run correction for owner-approved HR-005. It does not create `data/runs/2026-06-r03`, mutate r02, execute a validator, change `qa_status`, create an approval artifact, assign a D1 outcome, or authorize partial approval.

## 1. Authority and source boundary

HR-005 determines that the page-10 text `地點：中心活動室` belongs only to the separate `6月份例會日期及時間` notice. It is not a calendar-wide venue and does not apply to the 13 calendar-only activities represented by r02 IDs `2026-06-r02-033` through `2026-06-r02-045`.

Use only the authoritative final PDF:

`examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`

Do not use the spreadsheet, drafts, blank form, ZIP files, or any other source to supplement, repair, or reinterpret r03. Retain the source identity and r01/r02 lineage in the future r03 source manifest without copying the PDF into the run directory.

HR-001 through HR-004 remain in force exactly as implemented in preserved r02. HR-005 authorizes only the venue correction defined below.

## 2. Evidence preservation and lineage

- Preserve all r01 evidence unchanged.
- Preserve the complete r02 extraction, validation text, validation JSON, original QA observations, Human Review history, and interim summary.
- Do not overwrite r02 to conceal the unsupported venue inference or the earlier inaccurate QA conclusion.
- Derive r03 from the preserved r02/r01 lineage only after separate implementation authorization.
- Never overwrite an initially written r03 extraction or validator artifact. If initial r03 evidence is incorrect or a stop condition occurs after writing, preserve it and require a later unused replacement run ID under separate owner direction.

## 3. Exact planned record derivation

Expected r03 result:

- Total records: **45**.
- Unique activity IDs: **45**.
- First 32 detailed records: carry forward from r02 with zero field changes.
- Thirteen calendar-only records: carry forward with exactly the HR-005 mutation below and no other field change.
- All 45 records: retain pending `qa_status` before validation.

For each record `2026-06-r02-033` through `2026-06-r02-045`:

1. Require the r02 precondition: the `venue` value is exactly "中心活動室".
2. Set `venue` to "" (the empty string).
3. Require that the field name `venue` is absent from the r02 `uncertain_fields` array.
4. Add exactly one `venue` field-name entry to `uncertain_fields`.
5. Preserve every other field and array element exactly, including `activity_id`, title, category, description, dates, time, participant fields, fee, quota, registration fields, staff, notes, source reference, existing uncertainty entries, and `qa_status`.

No venue may be inferred from page 10 for these records. Insert the field name `venue` deterministically after `description` to match schema-field order; do not reorder any pre-existing uncertainty entry.

## 4. Exact pre-execution gate

Before any r03 directory or artifact is created, a read-only gate must establish all of the following:

1. `data/runs/2026-06-r03` does not exist.
2. The preserved r02 extraction SHA-256 is exactly `57511548C647CE1ADB8F1AC9BE62B111CC9F8D79DB6585F05762817D9D3DAE0F`.
3. R02 contains exactly 45 records and exactly 45 unique `activity_id` values.
4. The first 32 records are the detailed-record set and will be carried forward unchanged.
5. Exactly 13 records have IDs `2026-06-r02-033` through `2026-06-r02-045`, with no missing or additional ID in that interval.
6. Every affected record has the exact `venue` value "中心活動室".
7. Every affected record lacks the field name `venue` in `uncertain_fields`.
8. Every r02 record has pending `qa_status`.
9. HR-001 through HR-004 lineage and exclusions match the preserved r02 evidence.
10. The active business-rule registry remains BR-001 through BR-005 and excludes BR-006.

If any gate assertion fails, stop before creating r03 and return the mismatch to Human Review/owner review.

## 5. Construction assertions

An authorized implementation must build the complete r03 extraction in memory and assert before its first write:

- 45 records and 45 unique IDs.
- Zero changes to every field of the first 32 records.
- Exactly 13 changed records and no others.
- For each changed record, the only scalar-field difference is `venue`: "中心活動室" → "".
- For each changed record, the only array difference is one added `venue` field-name entry in `uncertain_fields`; all pre-existing entries and their order remain unchanged.
- No duplicate `venue` field-name marker.
- All 45 records retain pending `qa_status`.
- HR-001 through HR-004 remain implemented without alteration.
- HR-005 is implemented exactly and no page-10 venue is inferred for a calendar-only record.

Any other difference is outside owner authority and is a stop condition.

## 6. Fresh validation evidence plan

After separate implementation authorization and the one-time initial r03 extraction write:

1. Calculate and record the pre-validation extraction SHA-256.
2. Run the existing schema validator exactly once against r03 and write fresh human-readable and Validation Findings JSON Contract v1 artifacts under `data/runs/2026-06-r03/validation/`.
3. Run the existing business validator exactly once against r03 and write fresh human-readable and Validation Findings JSON Contract v1 artifacts under the same directory.
4. Record each command and exit code immediately.
5. Require text status, JSON status, finding counts, and exit semantics to agree.
6. Validate both JSON artifacts against the repository contract.
7. Confirm only BR-001 through BR-005 executed and BR-006 produced no execution or result.
8. Calculate the post-validation extraction SHA-256 and require exact equality with the pre-validation hash.

Do not reuse or relabel r02 validator outputs as r03 evidence. Do not run either validator more than once merely to obtain a preferred result.

## 7. Fresh QA plan

Perform fresh QA for all 45 r03 records against only the authoritative final PDF. QA must explicitly:

- visually inspect page 10 in the correct orientation;
- verify that `地點：中心活動室` is scoped only to `6月份例會日期及時間`;
- verify "" (empty) `venue` plus `venue` uncertainty for all 13 calendar-only records;
- reject any global or proximity-based venue inference;
- compare the first 32 records field-by-field with preserved r02 and confirm zero changes;
- compare the 13 calendar records field-by-field and confirm only the authorized HR-005 changes;
- recheck completeness, duplicates, source support, HR-001 through HR-004 decisions, exclusions, and traceability;
- remain recommendation-only and route every new ambiguity to Human Review.

Final closure must remain pending after validation and QA. No approval artifact or D1 outcome is part of this strategy.

## 8. Stop conditions

Stop and preserve evidence without repair or overwrite if any of the following occurs:

- R03 already exists before authorized implementation.
- The r02 extraction hash differs from the approved precondition.
- Any affected r02 ID, record count, unique-ID count, venue value, or uncertainty precondition differs.
- Any of the first 32 records changes.
- The mutation set is not exactly IDs `2026-06-r02-033` through `2026-06-r02-045`.
- Any field other than `venue` and `uncertain_fields` changes in those 13 records.
- An affected record retains or gains an inferred venue.
- The field name `venue` is missing from or duplicated in an affected record's `uncertain_fields`.
- Any record does not retain pending `qa_status` before validation.
- HR-001 through HR-004 behavior changes or HR-005 is not implemented exactly.
- A validator executes more than once, exits with tool-error code `2`, fails to produce fresh JSON evidence, or produces inconsistent text/JSON evidence.
- BR-006 executes or appears in validation results.
- The pre-validation and post-validation r03 extraction hashes differ.
- QA does not explicitly verify page-10 venue scope or reports an unsupported venue as supported.
- Any initial r02 or r03 evidence would need to be overwritten to continue.

An exit-code `1` validation result may remain valid evidence when findings are complete and contract-compliant; it must not be concealed by rerunning or overwriting artifacts. A stop condition requires Human Review/owner direction and, where initial r03 evidence already exists, a later unused replacement run rather than mutation of that evidence.

## 9. Authorization and closure boundary

Strategy status: **IMPLEMENTATION NOT AUTHORIZED**.

Separate owner authorization is required before creating `data/runs/2026-06-r03` or executing any construction, validation, or QA step. This strategy does not authorize partial approval. R03 record-state decisions, approval artifacts, and the final D1 outcome remain unresolved and must be decided only after fresh evidence is complete.
