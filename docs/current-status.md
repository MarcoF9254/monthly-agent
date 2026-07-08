# Current Project Status

Last Updated: 2026-07-08
Repository: monthly-agent
Default Branch: main

## Purpose

This is an AI handoff dashboard for ChatGPT, Codex, Claude, and future agents. It summarizes the current project state for continuation work and is not a public README.

The project supports an agent workflow for elderly centre monthly programme documents: extract activity records, validate structured data, support QA and Human Review, and prepare approved records for newsletter generation.

## Project Health

The project is in active development and currently focused on the business rule engine.

BR-001 through BR-004 have completed specification, implementation, tests, review, and commit. BR-005 needs another specification patch before implementation. BR-006 exists only as a local untracked draft and must not be modified unless explicitly requested.

## Current Milestone

Milestone 3 — Business Rule Engine

## Business Rule Status

| Rule | Status |
| --- | --- |
| BR-001 Required Fields | Spec, implementation, tests, and review completed |
| BR-002 Fee Uncertainty | Spec, implementation, tests, and review completed |
| BR-003 Registration Period | Spec, implementation, tests, and review completed |
| BR-004 QA Status | Spec, implementation, tests, and review completed |
| BR-005 Source Reference | Specification patch committed; spec patch round 2 required before implementation |
| BR-006 Per-Session Date Completeness | Draft / not started; local untracked file exists |

## Latest GitHub Commit

Latest known GitHub commit: `e47bd105`

This value is a handoff note. Codex must verify local Git state separately before local work.

## Local Working Tree Notes

Known current local untracked files:

- `docs/roadmap.md`
- `rules/BR-006-per-session-date-completeness.md`

Do not modify these files unless explicitly instructed. Local working tree status must be verified separately by Codex before starting any local work.

## Current Workflow Stage

Business rule specification and implementation cycle. The next work item is still specification-only for BR-005; implementation should wait until the revised BR-005 spec is accepted.

## Current Task

Patch BR-005 specification round 2:

1. Remove copied source text as an independent anchor.
2. Remove page uniqueness requirement.
3. Keep BR-005 compatible with per-record validators.

## Known Technical Debt

- Some existing files include encoding-sensitive Chinese text; use UTF-8 aware reads and writes.
- Business rule specs and implementations must stay aligned before adding validators.
- BR-005 must remain deterministic and avoid semantic, NLP, or fuzzy judgement.
- BR-006 is not ready for implementation.

## Architecture Principles

- Local Git repository is the source of truth for coding tasks.
- Business rules should be deterministic, auditable, and per-record where possible.
- Do not infer source meaning in validators; unclear or unsupported source details belong to QA or Human Review.
- Keep findings consistent across rules: `index`, `activity_id`, `rule_id`, `field`, `path`, `severity`, `message`, and `recommendation`.
- Preserve existing BR-001 through BR-004 behavior when adding later rules.

## Next Planned Milestones

1. Complete BR-005 specification patch round 2.
2. Review and commit the revised BR-005 spec.
3. Implement BR-005 with focused tests after spec approval.
4. Review BR-006 draft and decide scope before implementation.
5. Continue expanding the business rule engine toward downstream QA and newsletter workflows.
