# Current Project Status

Last Updated: 2026-07-08
Repository: monthly-agent
Default Branch: main

## Purpose

This is an AI handoff dashboard for ChatGPT, Codex, Claude, and future agents. It summarizes the current project state for continuation work and is not a public README.

The project supports an agent workflow for elderly centre monthly programme documents: extract activity records, validate structured data, support QA and Human Review, and prepare approved records for newsletter generation.

## Project Health

The project is in active development and currently focused on the business rule engine.

BR-001 through BR-004 have completed specification, implementation, tests, review, and commit. BR-005 has an accepted specification after the round 2 patch and is ready for implementation. BR-006 exists only as a local untracked draft and must not be modified unless explicitly requested.

## Current Milestone

Milestone 3 — Business Rule Engine

## Business Rule Status

| Rule | Status |
| --- | --- |
| BR-001 Required Fields | Spec, implementation, tests, and review completed |
| BR-002 Fee Uncertainty | Spec, implementation, tests, and review completed |
| BR-003 Registration Period | Spec, implementation, tests, and review completed |
| BR-004 QA Status | Spec, implementation, tests, and review completed |
| BR-005 Source Reference | Specification accepted after round 2 patch; implementation not started |
| BR-006 Per-Session Date Completeness | Draft / not started; local untracked file exists |

## Git State

The latest commit hash is intentionally not tracked in this file because it can become stale after any local commit, push, or branch change.

Future agents must verify Git state locally before work:

```powershell
git rev-parse --short HEAD
git status --short
```

## Local Working Tree Notes

Last-known local untracked files:

- `docs/roadmap.md`
- `rules/BR-006-per-session-date-completeness.md`

These notes may be stale. Verify the local working tree with `git status --short` before starting work. Do not modify these files unless explicitly instructed.

## Current Workflow Stage

Business rule specification and implementation cycle. The next work item is implementation-only for BR-005 using the accepted source-reference specification.

## Current Task

Implement BR-005 Source Reference rule.

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

1. Implement BR-005 with focused tests.
2. Review and commit the BR-005 implementation.
3. Review BR-006 draft and decide scope before implementation.
4. Continue expanding the business rule engine toward downstream QA and newsletter workflows.
