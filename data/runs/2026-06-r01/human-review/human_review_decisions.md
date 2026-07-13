# Human Review Decisions - Owner Approval Recorded

- Run ID: `2026-06-r01`
- Authoritative source: `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`
- Status: all four Human Review decisions approved. Approved corrections and calendar additions remain unapplied.

## HR-001 - Product-purchase notices

- Status: APPROVED
- Owner decision: `HR-001-B`
- Decision: Exclude the four page-9 milk-powder company purchase notices from activity extraction as commercial product-purchase arrangements.
- Owner rationale:
  - Product prices are not programme participation fees.
  - Ticket registration and purchase schedules do not by themselves make these notices programme activities.
  - The current extraction contract does not explicitly include retail product-purchase arrangements.
- Scope: This decision applies only to `2026-06-r01` and any directly derived replacement run for the same source.

## HR-002 - Calendar-only ongoing classes and services

- Status: APPROVED WITH AMENDMENTS
- Owner decision: amended matrix approval
- Evidence: PDF p.10 rotated June calendar.
- Approved `INCLUDE`: 毛巾操A班; 毛巾操B班; 活力舞 初班; 活力舞 中班; 健康活力運動A班; 健康活力運動B班; 健腦活腦小組; 長者普通話班; 長者英語會話班; 英文軟筆書法班; 集體舞 中班; 啞鈴運動班; 彈力橡筋操班.
- Approved `EXCLUDE_WORKFLOW`: 「活動抽籤」; 「活動報名」; 愛心午餐服務; 早晨包包.
- Approved `EXCLUDE_INTERNAL`: 職員會.
- Approved `EXCLUDE_COMMERCIAL`: 護老專門店：雅培; 護老專門店：倍力康.
- Owner rationale for amended exclusions: 愛心午餐服務 and 早晨包包 are routine service items that would not exist in the colleague-submitted activity draft workflow and must not be converted into activity records for this run.
- Conditions for the 13 future records:
  - Use only authoritative PDF page-10 evidence.
  - Preserve uncertainty for unavailable fee, quota, eligibility, staff, registration, and other fields.
  - Do not infer missing participant-facing details.
- Implementation status: approved but not applied. `2026-06-r01` extraction remains unchanged and `2026-06-r02` has not been created.

## HR-003 - Ten BR-005 source-reference corrections

- Status: APPROVED
- Owner decision: `HR-003-A`
- Evidence: business findings for record indices 1, 14, 20, 24, 26-31; exact activity titles are visible on their cited pages.
- Decision: Accept all ten deterministic `source_reference` corrections documented in the Owner Human Review Decision Packet.
- Restrictions:
  - The corrections are traceability metadata only.
  - No participant-facing field may change.
  - No field other than `source_reference` may change under this decision.
  - Each correction must use the exact source anchor already reviewed.
  - Any correction that cannot be applied exactly as reviewed must stop and return to Human Review.
- Implementation status: Authorized future corrections only, pending an owner decision on correction strategy. No correction has been applied to `2026-06-r01`.

## HR-004 - Slash fee semantics in service table

- Status: APPROVED
- Owner decision: `HR-004-B`
- Evidence: PDF p.9 lower table uses `/` for `織福兵團`, `銀鈴健樂團`, and `義工會`; it explicitly says `免費` only for the separate `量血壓服務` row.
- Decision for fee cells printed as `/`:
  - Preserve `/` in `amount_text`.
  - Use `amount: null`.
  - Retain fee uncertainty.
  - Do not interpret `/` as free.
  - Do not interpret `/` as not applicable.
- `量血壓服務` may retain zero fee only because the authoritative PDF explicitly states `免費` in its content, independently of the `/` fee cell.

## Decision Implementation Record

- Decisions accepted: `HR-001-B`, amended `HR-002`, `HR-003-A`, `HR-004-B`.
- Decision pending: none.
- Authorized mutation workflow or replacement run: pending owner correction-strategy decision.
- Resulting record-state changes: none.
- Validation rerun: none.
- Final run outcome: not assigned.
