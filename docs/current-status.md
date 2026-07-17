# Current Project Status

## Governance publication

`OD-REVIEW-POLICY-001` became repository-effective when PR #23 merged as `fb09d2ea547615a70299986608dba9f459c1e544` at `2026-07-17T01:40:28Z`.

`OD-REVIEW-EVIDENCE-002` — Review Evidence and Factual-Gate Procedures became repository-effective when PR #24 merged at `2026-07-17T05:47:09Z` through true merge commit `cd30a42bde387b66df0f99e117d7c2fd57b16b88`. Its first parent is `fb09d2ea547615a70299986608dba9f459c1e544`, and doubly reviewed head `9443dd0fc1624b3853cfc7ffbb3a941b4498bf11` is its second parent. The reviewed-head tree and merge tree were verified equal, and exactly `docs/current-status.md`, `docs/decisions.md`, `docs/governance.md`, and `docs/roadmap.md` landed.

The PR #24 publication roles were: Codex as work-product implementation author; ChatGPT as substantive initiator and governance facilitator; Marco as Owner, final approval authority, and merge authority; and Fable and Claude as the two required independent perspectives on the same exact head. Both independent perspectives concluded `APPROVE WITH NON-BLOCKING NOTES` with zero blocking and zero major findings.

Phase 1B and Phase 2 remain deferred and inactive. Production authority, trust-anchor delivery, security or schema activation, destructive operations, real-data activation, projection, manifest, downstream or deployment activation, BR-006, D3, and Greptile qualification remain unauthorized. The next implementation milestone remains undecided.

## OAR Phase 1A closure

The Bounded Calendar Authority Chain v0 architecture is frozen. PR #18 merged the accepted OAR contracts, inactive Draft 0.x schemas, and fictional authority and revocation fixtures. PR #19 merged the independently reviewed fictional year-2099 offline verifier prototype. PR #21 merged Phase 1A deterministic verifier core hardening at `2026-07-16T12:29:34Z` as merge commit `bf5063c2cdcb8d3cf915c5405dfb7fed26648683`. Its first parent is `7ee1650ba099234b21c6c94025d0ba6fa8486fd8`, and reviewed head `77d6554ada8f432ecc743b9c8115cc9d31d1a416` is its second parent. Phase 1A is closed.

The final suite was 172 passed with one pre-existing unrelated skip. All four Ubuntu/Windows and Python 3.11/3.12 CI jobs passed. Independent review concluded `APPROVE WITH NON-BLOCKING NOTES`, with zero blocking and zero major findings; P1A-F01 was genuinely resolved.

Last Updated: 2026-07-17
Repository: monthly-agent
Default Branch: main

## Purpose

This is an AI handoff dashboard for ChatGPT, Codex, Claude, and future agents. It summarizes the current project state for continuation work and is not a public README.

The project supports an agent workflow for elderly centre monthly programme documents: extract activity records, validate structured data, support QA and Human Review, and prepare approved records for newsletter generation.

## Project Health

The project has completed D2B machine-readable validation findings emission. Further milestone work remains subject to separate clarification and owner approval.

BR-001 through BR-005 are implemented, tested, and active in the runtime registry. BR-006 is implemented with direct unit coverage, but it is not registered or runtime active.

## Current Milestone

Scoped Downstream Eligibility Stage 1 architecture is accepted. The Architecture Owner explicitly accepted Option D and ADR-007. The fictional OAR verifier prototype and Phase 1A deterministic core hardening are complete, but production authority resolution, migration, eligibility issuance, projection generation, manifest generation, and downstream activation remain unimplemented and unauthorized.

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

No next implementation milestone has been selected. The current factual baseline is the completed fictional OAR chain plus closed Phase 1A hardening: the offline verifier checks RFC 8785/SHA-256 bindings, a separately supplied trust anchor, the non-self-authorizing publication bootstrap, ordinary closed-world membership, exact subject/envelope binding, authorized revocation before authority supersession, independent business-subject supersession, and deterministic fictional run metadata, eligibility, and selection outcomes. It executes two positive scenarios and preserves all twenty negative first-failure expectations.

Module-global `_LAST_TRACE` was removed. Trace is invocation-local and available only through a private test helper; public verification and CLI output remain trace-free. Success, `semantic_rejection`, and `resource_rejection` are distinguishable. Multiple effective business-key candidates fail closed, and snapshot, authority, and business-subject lifecycle traversal has cycle and depth protection. Fixed artifact-nonconfigurable ceilings cover 64 inventory artifacts, 256 KiB per JSON file, 2 MiB total admitted JSON, 256 snapshot entries, and depth 64. The depth ceiling is defensive and does not evidence an accepted 64-link scenario; resource checks do not solve TOCTOU.

This closure does not provide real trust-anchor delivery, real registry publication, real run metadata authority, authority or revocation issuance, R03 eligibility or selection, projection or manifest activation, calendar downstream activation, BR-006 activation, D3 resolution, or published-output recall. All OAR schemas remain inactive Draft 0.x artifacts.

## Known Technical Debt

- Some existing files include encoding-sensitive Chinese text; use UTF-8 aware reads and writes.
- Business rule specs and implementations must stay aligned before adding validators.
- BR-005 must remain deterministic and avoid semantic, NLP, or fuzzy judgement.
- BR-006 runtime activation remains held pending vertical-slice evidence, indexed marker syntax validation, and owner approval.
- P21-F01 is accepted non-blocking debt: `VerificationResult.classification` is the second positional dataclass field in a pre-stable interface. Phase 1B may evaluate keyword-only construction and a versioned result interface if it becomes an external contract.
- P21-F02 is accepted non-blocking debt: lifecycle depth 64 is a defensive secondary ceiling constrained by inventory and multi-artifact chain structure. Enforcement is independently tested at all three traversal locations; no accepted 64-link scenario is claimed.
- Phase 1B dependency/interface reproducibility and Phase 2 secure filesystem admission remain deferred, inactive, and subject to separate owner approval.

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
5. Keep Phase 1B and Phase 2 deferred and inactive until separately authorized; their ordering is not selected.
