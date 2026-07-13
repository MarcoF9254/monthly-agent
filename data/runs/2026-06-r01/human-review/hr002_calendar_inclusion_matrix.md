# HR-002 Calendar Record Inclusion Matrix - Owner Decision Recorded

- Run ID: `2026-06-r01`
- Run status: `PENDING HUMAN REVIEW / OWNER CLOSURE`
- Decision status: `APPROVED WITH AMENDMENTS — Implementation Pending`
- Authoritative evidence: PDF page 10, `六月一覽表`, from `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`
- Excluded sources were not consulted.

## Method

The review identified 51 distinct normalized calendar labels. Printed lesson suffixes such as `-7`, `-8`, and `(完)` are grouped into one recurring label. Thirty-one labels have clear matches among the existing 32 records and are counted as `ALREADY_REPRESENTED`; they are not repeated as unmatched rows below. The remaining 20 labels are classified individually. `下午休息`, the 19 June holiday cell, category symbols, and the calendar footer are annotations rather than activity labels and are not counted. Missing activity details do not by themselves justify exclusion.

## Summary

| Classification | Count |
| --- | ---: |
| Total distinct calendar labels reviewed | 51 |
| `ALREADY_REPRESENTED` | 31 |
| `INCLUDE` | 13 |
| `EXCLUDE_WORKFLOW` | 4 |
| `EXCLUDE_INTERNAL` | 1 |
| `EXCLUDE_COMMERCIAL` | 2 |
| `HUMAN_REVIEW_REQUIRED` | 0 |

The 31 represented labels were matched to record indices 1-31 except the membership record at index 0. Matches include detailed multi-session records such as “爸”氣“粽”動員, 魔力橋訓練班, 6月魔力橋練習場, 慢性腰膝疼痛支援小組, and 芬蘭木柱之旅; creating new calendar records for those labels would duplicate existing records.

## Inclusion matrix for calendar-only labels

| Label as printed | Page | Visible date/time evidence | Already represented? | Recommendation | Reason | Extraction implication if later approved | Uncertainty / missing fields |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 毛巾操A班-7/-8/-9/-10/-11(完) | p.10 | 6/1, 8, 15, 22, 29 at 09:00 | No | `INCLUDE` | Participant-facing recurring exercise class with five sessions. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported by footer as 中心活動室. |
| 毛巾操B班-10/-11/-12(完) | p.10 | 6/4, 11, 18 at 09:00 | No | `INCLUDE` | Participant-facing recurring exercise class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 活力舞 初班-6/-7/-8(完) | p.10 | 6/2, 9, 30 at 09:00 | No | `INCLUDE` | Participant-facing recurring dance class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 活力舞 中班-6/-7/-8(完) | p.10 | 6/2, 9, 30 at 10:00 | No | `INCLUDE` | Participant-facing recurring dance class distinct from 初班. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 愛心午餐服務 | p.10 | Weekdays at 11:00: 6/1-5, 8-12, 15-18, 22-26, 29-30 | No | `EXCLUDE_WORKFLOW` | Owner classified this as a routine service item outside the colleague-submitted activity draft workflow. | Add no activity record for this run. | Participant-facing service details remain outside activity extraction scope. |
| 健康活力運動A班-7/-8/-9/-10(完) | p.10 | 6/8, 15, 22, 29 at 14:00 | No | `INCLUDE` | Participant-facing recurring exercise class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 健康活力運動B班-6/-7(完) | p.10 | 6/17 and 24 at 15:00 | No | `INCLUDE` | Participant-facing recurring exercise class distinct from A班. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 健腦活腦小組3/4/5/6 | p.10 | 6/4, 11, 18, 25 at 14:00 | No | `INCLUDE` | Participant-facing recurring group under the 腦友天地 symbol. | Add one recurring group record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 長者普通話班-7/-8(完) | p.10 | 6/4 and 11 at 14:00 | No | `INCLUDE` | Participant-facing language class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 長者英語會話班-7/-8(完) | p.10 | 6/5 and 12 at 14:00 | No | `INCLUDE` | Participant-facing language class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 英文軟筆書法班-7/-8(完) | p.10 | 6/5 and 26 at 14:00 | No | `INCLUDE` | Participant-facing calligraphy class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 集體舞 中班-8/-9/-10(完) | p.10 | 6/5, 12, 26 at 10:00 | No | `INCLUDE` | Participant-facing recurring dance class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 啞鈴運動班 (5)/(6)/(7)完 | p.10 | 6/10, 17, 24 at 14:00 | No | `INCLUDE` | Participant-facing recurring exercise class. | Add one recurring class record. | Fee, quota, eligibility, staff, registration; venue supported. |
| 彈力橡筋操班-7/-8(完) | p.10 | 6/5 and 26 at 09:00 | No | `INCLUDE` | Participant-facing exercise class distinct from the p.2 one-off introduction. | Add one recurring class record; do not merge with index 2 / `2026-06-r01-003`. | Fee, quota, eligibility, staff, registration; venue supported. |
| 早晨包包 | p.10 | Legend: 逢星期一至五, 上午10時正至10時30分 | No | `EXCLUDE_WORKFLOW` | Owner classified this as a routine service item outside the colleague-submitted activity draft workflow. | Add no activity record for this run. | Participant-facing service details remain outside activity extraction scope. |
| 「活動抽籤」 | p.10 | 6/1 and 29 at 10:00 | No activity record; p.2 documents the workflow | `EXCLUDE_WORKFLOW` | Administrative ballot process rather than participant-facing programme content. | Add no record; retain as workflow evidence only. | The 6/29 draw's related batch is not identified. |
| 「活動報名」 | p.10 | 6/23 at 14:00 | No activity record; p.1 documents registration arrangements | `EXCLUDE_WORKFLOW` | Administrative registration marker, not a standalone activity. | Add no record. | Related later activities are not identified in the calendar. |
| 職員會 | p.10 | 6/18 at 15:30 | No | `EXCLUDE_INTERNAL` | Explicit staff-only meeting. | Add no record. | None material to participant extraction. |
| 護老專門店：雅培 | p.10 | 6/3 at 09:00 | No; corresponds to p.9 美國雅培 purchase schedule | `EXCLUDE_COMMERCIAL` | Commercial vendor purchase arrangement excluded by approved HR-001-B. | Add no record. | Venue not separately printed. |
| 護老專門店：倍力康 | p.10 | 6/10 at 09:00 | No; corresponds to p.9 倍力康 purchase schedule | `EXCLUDE_COMMERCIAL` | Commercial vendor purchase arrangement excluded by approved HR-001-B. | Add no record. | Calendar shows 09:00; p.9 gives 09:00-10:30 window. |

## Already-represented match audit

The following 31 normalized labels are classified `ALREADY_REPRESENTED` and require no new record:

| Calendar label | Existing index / activity ID |
| --- | --- |
| 中心例會（第一場／第二場） | 1 / `2026-06-r01-002` |
| 「健康齊打卡」簡介會 | 2 / `2026-06-r01-003` |
| “爸”氣“粽”動員（第一至第五場） | 3 / `2026-06-r01-004` |
| 心血管測試 | 4 / `2026-06-r01-005` |
| 美食茶餐廳 | 5 / `2026-06-r01-006` |
| 魔力橋訓練班-1/-2/-3(完) | 6 / `2026-06-r01-007` |
| 評估患骨質疏鬆的風險（雅培） | 7 / `2026-06-r01-008` |
| 美甲初體驗 | 8 / `2026-06-r01-009` |
| 長者健體計劃 | 9 / `2026-06-r01-010` |
| 6月魔力橋練習場 | 10 / `2026-06-r01-011` |
| 耆樂齊歡唱 | 11 / `2026-06-r01-012` |
| 爸爸的杯墊 | 12 / `2026-06-r01-013` |
| 芬蘭木柱之旅（一／二） | 13 / `2026-06-r01-014` |
| 魔力橋學習場 | 14 / `2026-06-r01-015` |
| 全身高效爆汗運動操-1/-2/-3 | 15 / `2026-06-r01-016` |
| 收身健美操 | 16 / `2026-06-r01-017` |
| 數碼諮詢站 | 17 / `2026-06-r01-018` |
| DIY國風手袋 | 18 / `2026-06-r01-019` |
| 怡景怡情空氣草（照顧者加油站） | 19 / `2026-06-r01-020` |
| 減壓充電樹遊戲 | 20 / `2026-06-r01-021` |
| 初夏浮游花瓶 | 21 / `2026-06-r01-022` |
| 慢性腰膝疼痛支援小組-1/-2/-3/-4 | 22 / `2026-06-r01-023` |
| 舒緩疲勞足浴鹽 | 23 / `2026-06-r01-024` |
| 『認知無障礙社區』知多D有獎問答 | 24 / `2026-06-r01-025` |
| 關愛兵團聚會 | 25 / `2026-06-r01-026` |
| 『運動、認知和營養訓練班』後測 | 26 / `2026-06-r01-027` |
| 織福兵團 | 27 / `2026-06-r01-028` |
| 量血壓服務 | 28 / `2026-06-r01-029` |
| 眼明手快 | 29 / `2026-06-r01-030` |
| 銀鈴健樂團練習 | 30 / `2026-06-r01-031` |
| 「義工會」 | 31 / `2026-06-r01-032` |

## Recommendation boundary

HR-002 is owner-approved with amendments: 13 labels are approved for future inclusion, four are excluded as workflow/routine-service items, one is excluded as internal, two are excluded as commercial, and 31 are already represented. No record has been created or changed. Implementation requires separate authorization and a correction strategy. The run remains `PENDING HUMAN REVIEW / OWNER CLOSURE`; no final outcome is assigned.
