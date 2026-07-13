# R02 Correction Strategy — Recommendation Only

- Source run: `2026-06-r01`
- Proposed replacement run: `2026-06-r02`
- Programme month: `2026-06`
- Strategy status: `IMPLEMENTATION NOT AUTHORIZED`
- Current r01 status: `PENDING HUMAN REVIEW / OWNER CLOSURE`

This document plans a replacement evidence run. It does not create `2026-06-r02`, mutate any record, execute a validator, create an approval artifact, or assign a final D1 outcome.

## 1. Source basis

Use only the owner-approved final publication:

`examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`

The r02 source manifest should record the same authoritative PDF identity and SHA-256 as r01, identify r02 as a directly derived replacement evidence run, and cite r01 as the preserved initial evidence run. Source authority remains limited to r01 and its directly derived replacement for this source.

Do not consult or use the spreadsheet, drafts, blank form, or any non-authoritative source to create, supplement, repair, cross-check, or reinterpret r02 records. Do not copy the PDF into the run directory; retain only `source/originals/.gitkeep` under `source/originals/`.

## 2. R01 preservation rule

Treat `data/runs/2026-06-r01/` as immutable initial evidence:

- Do not edit its extraction, validation, QA, Human Review, source, or summary artifacts during r02 implementation.
- Do not overwrite or reuse any r01 validation result.
- Preserve the r01 32-record extraction and its original validator evidence exactly as first observed.
- Build r02 in the new, unused directory `data/runs/2026-06-r02/` only after separate owner authorization and a fresh pre-execution gate.
- Record r01-to-r02 lineage and every approved mutation in r02 Human Review and QA evidence.

To keep changes within the approved decision scope, the recommended derivation is to carry the 32 existing records and their `activity_id` values forward unchanged, except for the ten exact `source_reference` corrections below. Assign the 13 new records new IDs `2026-06-r02-033` through `2026-06-r02-045` in the owner-approved order shown below. A proposal to renumber the 32 existing records would be an additional metadata mutation and should require separate owner approval.

Expected r02 extraction count after the approved additions: **45 records**.

## 3. Approved HR-003 traceability corrections

Apply only these ten deterministic metadata changes to the carried records. Do not change any participant-facing field or any field other than `source_reference`. The r01 index in this table is advisory navigation metadata only: implementation must locate and key each correction by the exact `activity_id` and exact current `source_reference`, never by array index alone. If either key does not match the reviewed r01 record, or if the exact reviewed replacement anchor cannot be applied, stop and return to Human Review.

| Advisory r01 index | Activity ID | Activity title | Exact corrected `source_reference` |
| ---: | --- | --- | --- |
| 1 | `2026-06-r01-002` | 中心例會 | `PDF p.1 最新消息；PDF p.10 6月份例會日期及時間，中心例會` |
| 14 | `2026-06-r01-015` | 魔力橋學習場 | `PDF p.4，魔力橋學習場` |
| 20 | `2026-06-r01-021` | 減壓充電樹遊戲 | `PDF p.6 護老家族大本營，減壓充電樹遊戲` |
| 24 | `2026-06-r01-025` | 『認知無障礙社區』知多D有獎問答 | `PDF p.8 腦友天地，『認知無障礙社區』知多D有獎問答` |
| 26 | `2026-06-r01-027` | 『運動、認知和營養訓練班』後測 | `PDF p.8 溫馨提示，『運動、認知和營養訓練班』後測` |
| 27 | `2026-06-r01-028` | 織福兵團 | `PDF p.9 義工團體集會及服務時間，織福兵團` |
| 28 | `2026-06-r01-029` | 量血壓服務 | `PDF p.9 義工團體集會及服務時間，量血壓服務` |
| 29 | `2026-06-r01-030` | 眼明手快 | `PDF p.9 義工團體集會及服務時間，眼明手快` |
| 30 | `2026-06-r01-031` | 銀鈴健樂團 | `PDF p.9 義工團體集會及服務時間，銀鈴健樂團` |
| 31 | `2026-06-r01-032` | 義工會 | `PDF p.9 義工團體集會及服務時間，義工會` |

These corrections are expected to remove the ten r01 BR-005 findings if the r02 validator applies the same active BR-005 behavior. That expectation is not a substitute for fresh validation.

## 4. Approved HR-002 calendar-only additions

Create one record for each approved label below, using only the visible page-10 calendar evidence. Preserve the printed activity label, dates, and times. Do not infer fee, quota, eligibility, staff, registration method, registration period, or any other unavailable participant-facing detail. Use empty schema-supported values and list the exact missing fields in `uncertain_fields`. Set every new record to `qa_status: "pending"`.

Each `source_reference` should be anchored as `PDF p.10 六月一覽表，<exact activity title>` so the page and visible label remain auditable and the exact title forms a deterministic BR-005 anchor.

| Proposed ID | Label | Visible p.10 dates | Visible time | Planned extraction |
| --- | --- | --- | --- | --- |
| `2026-06-r02-033` | 毛巾操A班 | 6/1, 6/8, 6/15, 6/22, 6/29 | 09:00 | One recurring class record |
| `2026-06-r02-034` | 毛巾操B班 | 6/4, 6/11, 6/18 | 09:00 | One recurring class record |
| `2026-06-r02-035` | 活力舞 初班 | 6/2, 6/9, 6/30 | 09:00 | One recurring class record |
| `2026-06-r02-036` | 活力舞 中班 | 6/2, 6/9, 6/30 | 10:00 | One recurring class record distinct from 初班 |
| `2026-06-r02-037` | 健康活力運動A班 | 6/8, 6/15, 6/22, 6/29 | 14:00 | One recurring class record |
| `2026-06-r02-038` | 健康活力運動B班 | 6/17, 6/24 | 15:00 | One recurring class record distinct from A班 |
| `2026-06-r02-039` | 健腦活腦小組 | 6/4, 6/11, 6/18, 6/25 | 14:00 | One recurring group record |
| `2026-06-r02-040` | 長者普通話班 | 6/4, 6/11 | 14:00 | One recurring class record |
| `2026-06-r02-041` | 長者英語會話班 | 6/5, 6/12 | 14:00 | One recurring class record |
| `2026-06-r02-042` | 英文軟筆書法班 | 6/5, 6/26 | 14:00 | One recurring class record |
| `2026-06-r02-043` | 集體舞 中班 | 6/5, 6/12, 6/26 | 10:00 | One recurring class record |
| `2026-06-r02-044` | 啞鈴運動班 | 6/10, 6/17, 6/24 | 14:00 | One recurring class record |
| `2026-06-r02-045` | 彈力橡筋操班 | 6/5, 6/26 | 09:00 | One recurring class record; do not merge with the p.2 one-off introduction |

Use page-10 venue text only where its visual scope unambiguously applies to the particular label. Otherwise leave `venue` empty and mark it uncertain. Do not turn calendar lesson-number suffixes into unsupported programme details; preserve them in `date_text`, recurrence wording, or notes only when their mapping is visually explicit.

## 5. Explicit exclusions

Do not create r02 activity records for:

- `愛心午餐服務` — owner-approved workflow/routine-service exclusion.
- `早晨包包` — owner-approved workflow/routine-service exclusion.
- `「活動抽籤」` — administrative workflow marker.
- `「活動報名」` — administrative workflow marker.
- `職員會` — internal staff activity.
- `護老專門店：雅培` — commercial purchase arrangement.
- `護老專門店：倍力康` — commercial purchase arrangement.

Continue to exclude the four page-9 milk-powder/product-purchase notices under HR-001-B: `雀巢佳膳`, `雀巢三花`, `倍力康`, and `美國雅培`. A date, time, price, ticket process, or purchase schedule does not convert those notices into programme activities.

HR-004 requires carried slash fee cells to preserve `amount_text: "/"`, `amount: null`, and fee uncertainty. `/` must never be interpreted as free or not applicable. The carried `量血壓服務` zero-fee exception may be retained only if the r01 record already contains source-supported `免費` evidence independently of the `/` fee cell; if that precondition is not met exactly, stop and return to Human Review rather than adding or inferring a zero fee.

## 6. Expected r02 artifact plan

After separate implementation authorization, create:

```text
data/runs/2026-06-r02/
├── source/
│   ├── source_manifest.json
│   └── originals/
│       └── .gitkeep
├── extraction/
│   └── extracted_activity_records.json
├── validation/
│   ├── schema_validation.txt
│   ├── schema_findings.json
│   ├── business_validation.txt
│   └── business_findings.json
├── qa/
│   └── qa_review_notes.md
├── human-review/
│   └── human_review_decisions.md
└── run_summary.md
```

The r02 Human Review artifact should record the implemented HR-001 through HR-004 decisions, the r01-to-r02 mutation map, the ten before/after source references, and the 13 added records. The interim summary should record commands, exit codes, hashes, counts, findings, QA results, and closure status. Do not create any `approval/` artifact unless a later owner-authorized closure outcome makes the applicable D1 artifact necessary.

## 7. Validation and QA plan

Before validation, calculate and record the r02 extraction SHA-256. Execute each existing validator exactly once against the completed 45-record r02 batch, with BR-001 through BR-005 only:

```powershell
$schemaText = & python tools/validate_schema.py `
  data/runs/2026-06-r02/extraction/extracted_activity_records.json `
  --run-id 2026-06-r02 `
  --json-output data/runs/2026-06-r02/validation/schema_findings.json 2>&1
$schemaExitCode = $LASTEXITCODE
$schemaText | Set-Content -Encoding utf8 data/runs/2026-06-r02/validation/schema_validation.txt
```

```powershell
$businessText = & python tools/validate_business_rules.py `
  data/runs/2026-06-r02/extraction/extracted_activity_records.json `
  --run-id 2026-06-r02 `
  --json-output data/runs/2026-06-r02/validation/business_findings.json 2>&1
$businessExitCode = $LASTEXITCODE
$businessText | Set-Content -Encoding utf8 data/runs/2026-06-r02/validation/business_validation.txt
```

Then:

1. Record both exit codes immediately; treat exit 0 as pass, exit 1 as valid fail evidence, and exit 2 as a run-level blocker.
2. Recalculate the extraction SHA-256 and require an exact pre/post match.
3. Validate both JSON artifacts with `validate_validation_artifact()` from `tools.validation_findings_json`.
4. Require text status, JSON status, finding counts, and exit semantics to agree.
5. Confirm the business artifact contains findings from the active BR-001 through BR-005 registry only and no BR-006 result.
6. Perform fresh GPT QA against the authoritative PDF for all 45 records, including completeness, duplicates, source support, uncertainty, the ten metadata corrections, all 13 page-10 additions, and all approved exclusions.
7. Keep QA recommendation-only and route any new ambiguity to Human Review. Do not silently mutate the validated r02 extraction.

## 8. Open risks and stop conditions

| Risk | Likely effect | Planned control |
| --- | --- | --- |
| Schema-required strings are absent from page 10 | Empty values remain schema-valid strings, but omission handling can be inconsistent | Use empty strings only where the schema requires a value and list every missing field in `uncertain_fields`; never invent content |
| `dates` and `fee` require non-empty arrays | A missing array or empty array causes schema failure | Preserve every visible calendar date; include one schema-shaped unknown fee entry and mark `fee` uncertain |
| Missing fee text or `amount: null` | BR-002 finding if fee uncertainty is omitted | Add exact `fee` uncertainty; do not label a missing fee as free, `/`, or not applicable |
| Missing registration timing | BR-003 finding if `registration_period` uncertainty is omitted | Leave unsupported registration values empty and include `registration_period` in `uncertain_fields` |
| Missing required practical fields | BR-001 findings if an empty field is not named uncertain | Include the exact schema field names for all unavailable required details, especially venue, target participants, fee, quota, registration method, and registration period |
| Premature record state | BR-004 finding | Set all 13 new records to `qa_status: "pending"`; do not approve records during extraction |
| Calendar traceability anchor is not deterministic | BR-005 finding | Use p.10 plus the exact visible activity title as a separately delimited source-reference anchor |
| Calendar label/session suffix mapping is ambiguous | Incorrect dates, recurrence, or duplicate records | Stop on any mismatch with the reviewed matrix; do not infer lesson sequencing |
| Page-10 footer or legend scope is ambiguous | Unsupported venue/category content | Use it only when its visual scope is explicit; otherwise retain uncertainty and route to QA/Human Review |
| Existing 32 records are accidentally altered during derivation | Evidence-preservation failure | Compare r01 and r02 field-by-field; permit only the ten reviewed `source_reference` changes plus the 13 appended records |
| Existing IDs are renumbered without approval | Additional unreviewed metadata mutation | Preserve the 32 existing IDs; seek separate owner approval before any renumbering policy change |
| An approved correction anchor differs from the reviewed text | HR-003 condition violated | Stop before validation and return the mismatch to Human Review |

An exit-1 validation result may remain valid evidence if findings are complete and contract-compliant. An exit-2 result, missing JSON artifact, extraction hash change, unexpected BR-006 result, unapproved field difference, or inability to trace a calendar record to page 10 is a run-level stop condition. Never overwrite r02 to conceal an initial result; use a later unused replacement run ID only under separate owner direction.

## Recommendation

When implementation is separately authorized, create r02 as a controlled, fully auditable derivative: preserve r01 unchanged, carry forward its 32 records with only the ten approved traceability corrections, append the 13 approved page-10 records, generate fresh D1/D2B evidence, and keep closure pending until r02 QA and any resulting Human Review are complete.
