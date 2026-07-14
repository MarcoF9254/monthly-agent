# Human Review Decisions — Implemented R02 Replacement Evidence

- Run ID: `2026-06-r02`
- Immutable baseline: `2026-06-r01`
- Status: Owner-approved HR-001 through HR-004 decisions implemented in the r02 extraction; r02 QA and owner closure remain pending.
- Authoritative source: `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`

## HR-001 — Product-purchase notices

- Decision: `HR-001-B` implemented.
- Excluded page-9 purchase notices: `雀巢佳膳`, `雀巢三花`, `倍力康`, and `美國雅培`.
- No commercial product-purchase record was added.

## HR-002 — Calendar-only records

- Decision: owner-approved amended matrix implemented.
- Added exactly 13 page-10 calendar records:
- `2026-06-r02-033` — 毛巾操A班
- `2026-06-r02-034` — 毛巾操B班
- `2026-06-r02-035` — 活力舞 初班
- `2026-06-r02-036` — 活力舞 中班
- `2026-06-r02-037` — 健康活力運動A班
- `2026-06-r02-038` — 健康活力運動B班
- `2026-06-r02-039` — 健腦活腦小組
- `2026-06-r02-040` — 長者普通話班
- `2026-06-r02-041` — 長者英語會話班
- `2026-06-r02-042` — 英文軟筆書法班
- `2026-06-r02-043` — 集體舞 中班
- `2026-06-r02-044` — 啞鈴運動班
- `2026-06-r02-045` — 彈力橡筋操班
- Excluded as workflow/routine service: `「活動抽籤」`, `「活動報名」`, `愛心午餐服務`, `早晨包包`.
- Excluded as internal: `職員會`.
- Excluded as commercial: `護老專門店：雅培`, `護老專門店：倍力康`.
- Missing calendar-only fee, quota, eligibility, staff, and registration details remain empty and are listed in `uncertain_fields`.

## HR-003 — Deterministic traceability corrections

- Decision: `HR-003-A` implemented.
- Corrections were keyed by exact `activity_id` and exact current `source_reference`; advisory indices were not used as mutation keys.
- Only `source_reference` changed in the 32 carried records.

| Activity ID | Exact r01 value | Exact r02 value |
| --- | --- | --- |
| `2026-06-r01-002` | `PDF p.1 最新消息；p.10 6月份例會日期及時間` | `PDF p.1 最新消息；PDF p.10 6月份例會日期及時間，中心例會` |
| `2026-06-r01-015` | `PDF p.4 魔力橋學習場` | `PDF p.4，魔力橋學習場` |
| `2026-06-r01-021` | `PDF p.6 護老家族大本營` | `PDF p.6 護老家族大本營，減壓充電樹遊戲` |
| `2026-06-r01-025` | `PDF p.8 腦友天地` | `PDF p.8 腦友天地，『認知無障礙社區』知多D有獎問答` |
| `2026-06-r01-027` | `PDF p.8 溫馨提示` | `PDF p.8 溫馨提示，『運動、認知和營養訓練班』後測` |
| `2026-06-r01-028` | `PDF p.9 義工團體集會及服務時間` | `PDF p.9 義工團體集會及服務時間，織福兵團` |
| `2026-06-r01-029` | `PDF p.9 義工團體集會及服務時間` | `PDF p.9 義工團體集會及服務時間，量血壓服務` |
| `2026-06-r01-030` | `PDF p.9 義工團體集會及服務時間` | `PDF p.9 義工團體集會及服務時間，眼明手快` |
| `2026-06-r01-031` | `PDF p.9 義工團體集會及服務時間` | `PDF p.9 義工團體集會及服務時間，銀鈴健樂團` |
| `2026-06-r01-032` | `PDF p.9 義工團體集會及服務時間` | `PDF p.9 義工團體集會及服務時間，義工會` |

## HR-004 — Slash fee semantics

- Slash cells remain `amount_text: /`, `amount: null`, with `fee` uncertainty.
- `/` was not interpreted as free or not applicable.
- `量血壓服務` retains `免費` and numeric zero only because the carried r01 record independently contains source-supported free-service evidence.

## Implementation boundary

- Carried records: 32, with existing activity IDs preserved.
- Added records: 13, IDs `2026-06-r02-033` through `2026-06-r02-045`.
- Resulting extraction: 45 records, all `qa_status: pending` before QA.
- No approval artifact exists and no final D1 outcome is assigned.
- Any new QA ambiguity remains subject to Human Review; this artifact does not close the run.
## Fresh GPT QA handoff

- Fresh source QA completed for all 45 records against the authoritative PDF.
- Proposed post-validation mutations: none.
- New unresolved source questions: none.
- The 13 calendar-only records retain owner-approved uncertainty for unavailable details.
- All 45 records remain `qa_status: "pending"` in the validated extraction.
- Owner record-state decisions and final run closure remain pending; no approval artifact or final D1 outcome is created here.

## 2026-07-14 owner decision addendum — HR-005 Page-10 Venue Scope

- Decision status: owner approved.
- Supersedes only the earlier interpretation that `地點：中心活動室` was a calendar-wide venue.
- Authoritative visual-scope finding: on PDF page 10, `地點：中心活動室` belongs only to the separate `6月份例會日期及時間` notice. It does not apply to the 13 calendar-only activities.
- Affected r02 records: `2026-06-r02-033` through `2026-06-r02-045`.
- Required replacement representation for every affected record: set `venue` to the empty string, include the field name `venue` in `uncertain_fields`, and infer no venue from page 10.
- R02 currently contains the unsupported venue value `中心活動室` in all 13 affected records and omits the field name `venue` from their `uncertain_fields`.
- R02 closure is held. R02 is not closure-ready.
- No r02 record, extraction artifact, validation artifact, or `qa_status` was corrected or rewritten by this decision record.
- The original r02 QA observations remain preserved as first recorded, including the inaccurate zero-unsupported-inference and calendar-wide-venue claims; the dated QA addendum identifies and supersedes those claims without deleting them.
- No partial-approval execution, approval artifact, or final D1 outcome is authorized.
- Implementing HR-005 requires a separately authorized `2026-06-r03` replacement evidence run under `docs/run-strategies/2026-06-r03-correction-strategy.md`.
