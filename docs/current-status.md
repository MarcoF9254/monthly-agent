# Current Project Status

## OAR contracts and fictional verifier

The Bounded Calendar Authority Chain v0 architecture is frozen. PR #18 merged the accepted OAR contracts, inactive Draft 0.x schemas, and fictional authority and revocation fixtures. PR #19 merged the independently reviewed fictional year-2099 offline verifier prototype. The prototype is executable fictional evidence only; it is not a production authority resolver or an activation of any draft schema.

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

Scoped Downstream Eligibility Stage 1 architecture is accepted. The Architecture Owner explicitly accepted Option D and ADR-007. The fictional OAR verifier prototype is complete, but production authority resolution, migration, eligibility issuance, projection generation, manifest generation, and downstream activation remain unimplemented and unauthorized.

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

No next milestone has been selected. The current factual baseline is the completed fictional OAR chain: the offline verifier checks RFC 8785/SHA-256 bindings, a separately supplied trust anchor, the non-self-authorizing publication bootstrap, ordinary closed-world membership, exact subject/envelope binding, authorized revocation before authority supersession, independent business-subject supersession, and deterministic fictional run metadata, eligibility, and selection outcomes. It executes two positive scenarios and twenty negative first-failure cases. The merge validation baseline was 147 passed with one pre-existing unrelated skip.

This closure does not provide real trust-anchor delivery, real registry publication, real run metadata authority, authority or revocation issuance, R03 eligibility or selection, projection or manifest activation, calendar downstream activation, BR-006 activation, D3 resolution, or published-output recall. All OAR schemas remain inactive Draft 0.x artifacts.

## Known Technical Debt

- Some existing files include encoding-sensitive Chinese text; use UTF-8 aware reads and writes.
- Business rule specs and implementations must stay aligned before adding validators.
- BR-005 must remain deterministic and avoid semantic, NLP, or fuzzy judgement.
- BR-006 runtime activation remains held pending vertical-slice evidence, indexed marker syntax validation, and owner approval.
- The fictional verifier module-global lifecycle trace supports test introspection only and is not concurrency-safe. It does not affect authority outcomes, is acceptable for this prototype, and must be removed or redesigned before concurrent or production use.

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

1. Keep the next milestone undecided until a separate owner decision.
2. Keep D3 / indexed marker syntax validation pending clarification; do not begin implementation without separate approval.
3. Plan real vertical-slice evidence only with separate owner approval.
4. Require real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval before BR-006 runtime activation.
