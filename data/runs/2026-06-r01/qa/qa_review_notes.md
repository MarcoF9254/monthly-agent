# GPT QA Review Notes

## Summary

- Run ID: `2026-06-r01`
- Authoritative source: `examples/architecture-review/2026-06/final/2026.6月月刊fin2.pdf`
- Total extracted activities: 32
- Missing-activity questions: 2 grouped scope questions (four product-purchase notices; calendar-only ongoing classes)
- Duplicate activities found: 0
- Records with validator findings: 10
- Additional QA finding groups: 3
- Records approved by GPT QA: 0 (QA is recommendation-only)
- Complete PDF reviewed: yes, all 10 pages visually at 180 DPI and against extracted text

## Source and Layout Review

All ten rendered pages were legible. Pages 2-6 use multi-column panels whose text extraction order differs materially from visual reading order; record boundaries were taken from the rendered panels. Page 9 contains two separate tables. Page 10 is a rotated monthly calendar and was treated as a schedule/index for comparison, not as a replacement for the detailed panels. No excluded spreadsheet, draft, or blank form was consulted.

## Record-by-record Accounting

| Index | Activity ID | Title | Source evidence | QA result |
| ---: | --- | --- | --- | --- |
| 0 | 2026-06-r01-001 | 2026至2027年度會員續會/入會 | p.1 membership box | Source-supported; missing quota/staff remain explicit. |
| 1 | 2026-06-r01-002 | 中心例會 | p.1 latest news; p.10 calendar | Participant details supported; BR-005 source anchor needs correction. |
| 2 | 2026-06-r01-003 | 量血壓獎勵計劃-「健康齊打卡」簡介會 | p.2 item 1 | Source-supported; fee absent and flagged. |
| 3 | 2026-06-r01-004 | “爸”氣“粽”動員 | p.2 items 2-6 | Five sessions correctly retained as one source activity. |
| 4 | 2026-06-r01-005 | 心血管測試 | p.3 item 7 | Source-supported; fee absent and flagged. |
| 5 | 2026-06-r01-006 | 美食茶餐廳 | p.3 item 8 | Source-supported. |
| 6 | 2026-06-r01-007 | 魔力橋訓練班 | p.3 item 9 | Three sessions and attendance condition supported. |
| 7 | 2026-06-r01-008 | 評估患骨質疏鬆的風險 | p.3 item 10 | Source-supported; fee absent and flagged. |
| 8 | 2026-06-r01-009 | 美甲初體驗 | p.3 item 11 | Source-supported. |
| 9 | 2026-06-r01-010 | 長者健體計劃 | p.4 item 12 | Source-supported; fee absent and flagged. |
| 10 | 2026-06-r01-011 | 6月魔力橋練習場 | p.4 item 13 | Four sessions supported. |
| 11 | 2026-06-r01-012 | 耆樂齊歡唱 | p.4 item 14 | Source-supported; fee absent and flagged. |
| 12 | 2026-06-r01-013 | 爸爸的杯墊 | p.4 item 15 | Source-supported. |
| 13 | 2026-06-r01-014 | 芬蘭木柱之旅 | p.4 items 16-17 | Two sessions correctly retained as one source activity. |
| 14 | 2026-06-r01-015 | 魔力橋學習場 | p.4 lower-left panel | Details supported; BR-005 source anchor needs correction. |
| 15 | 2026-06-r01-016 | 全身高效爆汗運動操 | p.5 item 18 | Five sessions including July supported. |
| 16 | 2026-06-r01-017 | 收身健美操 | p.5 item 19 | Source-supported. |
| 17 | 2026-06-r01-018 | 數碼諮詢站 | p.5 item 20 | Dates, two slots, and one-session limit supported. |
| 18 | 2026-06-r01-019 | DIY國風手袋 | p.5 item 21 | Source-supported. |
| 19 | 2026-06-r01-020 | 怡景怡情空氣草 | p.5 item 22 | Source-supported; fee absent and flagged. |
| 20 | 2026-06-r01-021 | 減壓充電樹遊戲 | p.6 top panel | Details supported; BR-005 source anchor needs correction. |
| 21 | 2026-06-r01-022 | 初夏浮游花瓶 | p.6 item 23 | Source-supported; fee absent and flagged. |
| 22 | 2026-06-r01-023 | 慢性腰膝疼痛支援小組 | p.6 item 24 | Ten sessions and eligibility notes supported. |
| 23 | 2026-06-r01-024 | 舒緩疲勞足浴鹽（伴樂篇） | p.6 item 25 | Source-supported; fee absent and flagged. |
| 24 | 2026-06-r01-025 | 『認知無障礙社區』知多D有獎問答 | p.8 top panel | Details supported; BR-005 source anchor needs correction. |
| 25 | 2026-06-r01-026 | 關愛兵團聚會 | p.8 item 26 | Source-supported; missing registration/quota/fee explicit. |
| 26 | 2026-06-r01-027 | 『運動、認知和營養訓練班』後測 | p.8 lower panel | Details supported; BR-005 source anchor needs correction. |
| 27 | 2026-06-r01-028 | 織福兵團 | p.9 service table row | Row supported; slash fee remains uncertain; BR-005 anchor needs correction. |
| 28 | 2026-06-r01-029 | 量血壓服務 | p.9 service table row | Free service supported; audience/registration absent; BR-005 anchor needs correction. |
| 29 | 2026-06-r01-030 | 眼明手快 | p.9 service table row | Dates/time/$4 supported; BR-005 anchor needs correction. |
| 30 | 2026-06-r01-031 | 銀鈴健樂團 | p.9 service table row; p.10 venue schedule | Activity supported; slash fee remains uncertain; BR-005 anchor needs correction. |
| 31 | 2026-06-r01-032 | 義工會 | p.9 service table row | Activity supported; slash fee remains uncertain; BR-005 anchor needs correction. |

## Findings and Proposed Corrections

### QA-001 - BR-005 deterministic anchors

- Severity: medium
- Affected records: indices 1, 14, 20, 24, 26, 27, 28, 29, 30, 31
- Current values: source references named sections or tables but did not contain a BR-005 v1 deterministic title/item/row anchor.
- Proposed action: after Human Review, replace each affected `source_reference` with a page plus exact activity title or page plus table-row title, preserving all other fields.
- Evidence: the exact titles are visibly present on the cited pages.
- Human Review required: yes; extraction is not mutated by QA.

### QA-002 - Page 9 product-purchase notices omitted

- Severity: medium
- Affected path: extraction batch completeness
- Current value: no records for the four milk-powder company registration/purchase notices (`雀巢佳膳`, `雀巢三花`, `倍力康`, `美國雅培`).
- Proposed action: owner decides whether product-purchase notices fall within the extraction prompt's `notice` scope. If yes, add four records in an approved correction workflow.
- Evidence: PDF p.9 upper table contains registration periods, purchase dates/times, prices, and a four-can limit.
- Reason: these are participant-facing notices but are product purchases rather than programme activities.
- Human Review required: yes.

### QA-003 - Calendar-only ongoing entries omitted

- Severity: medium
- Affected path: extraction batch completeness
- Current value: page-10 entries without a detailed panel/table elsewhere were not promoted into records.
- Examples: `毛巾操A班/B班`, `活力舞初班/中班`, `愛心午餐服務`, `健康活力運動A班/B班`, `健腦活腦小組`, `長者普通話班`, `長者英語會話班`, `英文軟筆書法班`, `集體舞中班`, `啞鈴運動班`, `彈力橡筋操班`, `早晨包包`.
- Proposed action: owner determines whether the calendar alone establishes extractable activity records or is a schedule/index for existing programmes.
- Evidence: PDF p.10 rotated monthly calendar; many entries provide only a title, time, and occurrence marker.
- Reason: creating full records would require numerous unknown fields and risks conflating ongoing class sessions with new June enrolment activities.
- Human Review required: yes.

## Validation Findings Accounting

- Schema: pass, 0 findings.
- Business: fail, 10 findings, all BR-005 medium-severity source-reference anchors.
- BR-006 findings: 0; BR-006 was not in the runtime registry.
- No validator finding was silently corrected.

## Unsupported Inference and Source-conflict Review

- No values were taken from excluded files.
- No duplicate activity records were found.
- The PDF contains no direct conflict among the extracted detailed panels and service rows.
- General registration timing from p.1/p.2 was applied only where the publication visibly labels activities as draw-based or first-come registration. Human Review may confirm this mapping before any correction/approval step.
- Slash (`/`) fee entries in the p.9 service table were preserved as source wording and marked uncertain; they were not converted to free.

## Human Review Needed

1. Decide the page-9 product-purchase notice scope.
2. Decide the page-10 calendar-only activity scope.
3. Authorize or reject the ten proposed deterministic source-reference corrections.
4. Confirm whether slash (`/`) in p.9 service rows should remain unknown or be interpreted as no fee.

