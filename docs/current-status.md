# Current Project Status

## OAR drafting

`OD-OAR-CONTRACT-AUTHOR-001` authorizes inactive Draft 0.x contracts and fictional fixtures only. No executable validator, resolver, builder, real authority artifact, or activation exists.

Last Updated: 2026-07-16
Repository: monthly-agent
Default Branch: main

## Purpose

This is an AI handoff dashboard for ChatGPT, Codex, Claude, and future agents. It summarizes the current project state for continuation work and is not a public README.

The project supports an agent workflow for elderly centre monthly programme documents: extract activity records, validate structured data, support QA and Human Review, and prepare approved records for newsletter generation.

## Project Health

The project has completed D2B machine-readable validation findings emission. Further milestone work remains subject to separate clarification and owner approval.

BR-001 through BR-005 are implemented, tested, and active in the runtime registry. BR-006 is implemented with direct unit coverage, but it is not registered or runtime active.

## Current Milestone

Scoped Downstream Eligibility Stage 1 architecture is accepted. The Architecture Owner explicitly accepted Option D and ADR-007. No implementation milestone is active; contracts, runtime behavior, migration, eligibility issuance, projection generation, and downstream activation remain unimplemented and unauthorized.

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

Closed R03 baseline: 45 records total; 32 approved; 13 `needs_review`; final D1 outcome `partially_approved`; downstream not activated. The 13 withheld calendar-only records remain outside `approved_records.json` and have no consumer eligibility decision.

Milestone 3.7 / D1 Pipeline Run Contract, D2A, and D2B are completed and merged. D2B implements Validation Findings JSON emission while preserving existing `PASS` / `FAIL` text structure, validation ordering, and exit code semantics. Missing, `None`, or empty `activity_id` values are consistently rendered as `"<missing>"` under Finding Contract v1. D1 JSON artifact requirements are prospective and non-retroactive. No pipeline runner exists.

BR-006 implementation and direct unit coverage are retained while runtime activation remains held. Active runtime rules are BR-001 through BR-005. Future BR-006 activation requires real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval.

## Current Task

Gate 2 bounded authority input contract drafting is active under `OD-BAI-ARCH-001` (accepted with owner changes) and `OD-BAI-CONTRACT-001` (drafting approved). The direction requires one external trust anchor plus one self-contained verified bundle; rollback detection depends on the anchor. All new schemas remain inactive, unaccepted draft `0.x`. No implementation milestone is active; no real trust anchor, registry publication, run metadata authority, authority, eligibility, selection, projection, manifest, migration, or activation artifact exists. R03 remains `partially_approved`; downstream and BR-006 remain inactive, D3 remains unresolved, and approved-only newsletter behavior is unchanged.

The positive fictional `valid-resolution-chain` is valid only as a Gate 2 bounded-input envelope chain. It does not prove executable end-to-end verification of the separate owner-authority artifacts referenced by eligibility or monthly selection. Owner-authority artifact schemas, fictional fixtures, and verifiers remain separately blocked and require separate owner authorization.

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
