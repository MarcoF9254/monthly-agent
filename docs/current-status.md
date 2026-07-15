# Current Project Status

Last Updated: 2026-07-15
Repository: monthly-agent
Default Branch: main

## Purpose

This is an AI handoff dashboard for ChatGPT, Codex, Claude, and future agents. It summarizes the current project state for continuation work and is not a public README.

The project supports an agent workflow for elderly centre monthly programme documents: extract activity records, validate structured data, support QA and Human Review, and prepare approved records for newsletter generation.

## Project Health

The project has completed D2B machine-readable validation findings emission. Further milestone work remains subject to separate clarification and owner approval.

BR-001 through BR-005 are implemented, tested, and active in the runtime registry. BR-006 is implemented with direct unit coverage, but it is not registered or runtime active.

## Current Milestone

Scoped Downstream Eligibility Stage 1 is authorized for architecture drafting only. Option D is the drafting direction; final acceptance, implementation, and activation remain pending.

Milestone 3.9 / D2B — Machine-readable Validation Findings Emission (completed and merged in PR #10)

## Business Rule Status

| Rule | Status |
| --- | --- |
| BR-001 Required Fields | Spec, implementation, tests, and review completed |
| BR-002 Fee Uncertainty | Spec, implementation, tests, and review completed |
| BR-003 Registration Period | Spec, implementation, tests, and review completed |
| BR-004 QA Status | Spec, implementation, tests, and review completed |
| BR-005 Source Reference | Spec, implementation, tests, and review completed |
| BR-006 Per-Session Date Completeness | Implemented with direct unit tests; activation held and not in the runtime registry |

## Git State

The latest commit hash is intentionally not tracked in this file because it can become stale after any local commit, push, or branch change.

Future agents must verify Git state locally before work:

```powershell
git rev-parse --short HEAD
git status --short
```

## Current Workflow Stage

Milestone 3.7 / D1 Pipeline Run Contract, D2A, and D2B are completed and merged. D2B implements Validation Findings JSON emission while preserving existing `PASS` / `FAIL` text structure, validation ordering, and exit code semantics. Missing, `None`, or empty `activity_id` values are consistently rendered as `"<missing>"` under Finding Contract v1. D1 JSON artifact requirements are prospective and non-retroactive. No pipeline runner exists.

BR-006 implementation and direct unit coverage are retained while runtime activation remains held. Active runtime rules are BR-001 through BR-005. Future BR-006 activation requires real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval.

## Current Task

Document the separation of record review, owner authority, consumer policy, and generated projection. No runtime implementation is authorized.

No implementation milestone is currently active. D3 clarification or vertical-slice evidence planning remains subject to separate owner approval.

## Known Technical Debt

- Some existing files include encoding-sensitive Chinese text; use UTF-8 aware reads and writes.
- Business rule specs and implementations must stay aligned before adding validators.
- BR-005 must remain deterministic and avoid semantic, NLP, or fuzzy judgement.
- BR-006 runtime activation remains held pending vertical-slice evidence, indexed marker syntax validation, and owner approval.

## Architecture Principles

- Local Git repository is the source of truth for coding tasks.
- Business rules should be deterministic, auditable, and per-record where possible.
- Do not infer source meaning in validators; unclear or unsupported source details belong to QA or Human Review.
- Keep findings consistent across rules: `index`, `activity_id`, `rule_id`, `field`, `path`, `severity`, `message`, and `recommendation`.
- Preserve existing BR-001 through BR-004 behavior when adding later rules.

## Next Planned Milestones

Naming map:

- D1 = Milestone 3.7 — Pipeline Run Contract (completed and merged)
- D2 = Machine-readable Validation Findings delivery track
  - D2A = Milestone 3.8 — Machine-readable Validation Findings Contract
  - D2B = Milestone 3.9 — additive validator JSON artifact emission (completed and merged in PR #10)
- D3 = future Indexed Marker Syntax Validation (pending clarification)

Next steps:

1. Keep D3 / indexed marker syntax validation pending clarification; do not begin implementation without separate approval.
2. Plan real vertical-slice evidence only with separate owner approval.
3. Require real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval before BR-006 runtime activation.
