# Current Project Status

## Governance publication

`OD-REVIEW-POLICY-001` became repository-effective when PR #23 merged as `fb09d2ea547615a70299986608dba9f459c1e544` at `2026-07-17T01:40:28Z`.

`OD-REVIEW-EVIDENCE-002` — Review Evidence and Factual-Gate Procedures became repository-effective when PR #24 merged at `2026-07-17T05:47:09Z` through true merge commit `cd30a42bde387b66df0f99e117d7c2fd57b16b88`. Its first parent is `fb09d2ea547615a70299986608dba9f459c1e544`, and doubly reviewed head `9443dd0fc1624b3853cfc7ffbb3a941b4498bf11` is its second parent. The reviewed-head tree and merge tree were verified equal, and exactly `docs/current-status.md`, `docs/decisions.md`, `docs/governance.md`, and `docs/roadmap.md` landed.

The PR #24 publication roles were: Codex as work-product implementation author; ChatGPT as substantive initiator and governance facilitator; Marco as Owner, final approval authority, and merge authority; and Fable and Claude as the two required independent perspectives on the same exact head. Both independent perspectives concluded `APPROVE WITH NON-BLOCKING NOTES` with zero blocking and zero major findings.

OAR Phase 1B.1 Dependency and Package Foundation is completed and repository-effective. PR #26 merged at `2026-07-17T13:52:58Z` through true merge commit `466ec18c0b232bfa99de1822124e35ae39495def`. Its first parent is `1375235a9e00df5a8e3835fe58a326dc16883874`, and merged head `5c9ffd88246a491eb9bf6043744428c4e2574a9a` is its second parent. The merged-head tree and merge tree are equal, and exactly the approved ten implementation paths landed.

Phase 1B.2 — Versioned Verification Result Contract is `COMPLETED — MERGED IN PR #28 / REPOSITORY-EFFECTIVE`. PR #28 merged at `2026-07-18T00:40:55Z` through true merge commit `b1f7c5ad67a3eb5900b7323f8756ab319e27294c`. Its first parent is `3600f4f004ca46ed4392e3b0c4fdff6f3ad6c30a`, and reviewed head `a264d60d943fc9137120dc886eea16c9948bec51` is its second parent. Exactly `README.md`, `docs/current-status.md`, `docs/decisions.md`, `docs/roadmap.md`, `tests/test_oar_result_contract.py`, `tools/oar_verifier/errors.py`, `tools/oar_verifier/verifier.py`, and `tools/verify_fictional_authority.py` landed.

Its scope is result/interface contract stabilization only: `verification-result/v1`, keyword-only `VerificationResult` construction, and authoritative CLI JSON serialization through `to_payload()`. It provides no console entry point, package-version change, installed-wheel standalone CLI, runtime resource relocation, repository-root argument, CLI argument redesign, filesystem admission, TOCTOU remediation, symlink policy, production authority, real trust-anchor delivery, schema activation, Phase 2, projection, manifest, downstream activation, BR-006, or D3.

## OAR Phase 1A closure

The Bounded Calendar Authority Chain v0 architecture is frozen. PR #18 merged the accepted OAR contracts, inactive Draft 0.x schemas, and fictional authority and revocation fixtures. PR #19 merged the independently reviewed fictional year-2099 offline verifier prototype. PR #21 merged Phase 1A deterministic verifier core hardening at `2026-07-16T12:29:34Z` as merge commit `bf5063c2cdcb8d3cf915c5405dfb7fed26648683`. Its first parent is `7ee1650ba099234b21c6c94025d0ba6fa8486fd8`, and reviewed head `77d6554ada8f432ecc743b9c8115cc9d31d1a416` is its second parent. Phase 1A is closed.

The final suite was 172 passed with one pre-existing unrelated skip. All four Ubuntu/Windows and Python 3.11/3.12 CI jobs passed. Independent review concluded `APPROVE WITH NON-BLOCKING NOTES`, with zero blocking and zero major findings; P1A-F01 was genuinely resolved.

Last Updated: 2026-07-18
Repository: monthly-agent
Default Branch: main

## Purpose

This is an AI handoff dashboard for ChatGPT, Codex, Claude, and future agents. It summarizes the current project state for continuation work and is not a public README.

The project supports an agent workflow for elderly centre monthly programme documents: extract activity records, validate structured data, support QA and Human Review, and prepare approved records for newsletter generation.

## Project Health

The project has completed D2B machine-readable validation findings emission. Further milestone work remains subject to separate clarification and owner approval.

BR-001 through BR-005 are implemented, tested, and active in the runtime registry. BR-006 is implemented with direct unit coverage, but it is not registered or runtime active.

## Milestone Status

Scoped Downstream Eligibility Stage 1 architecture is accepted. The Architecture Owner explicitly accepted Option D and ADR-007. The fictional OAR verifier prototype and Phase 1A deterministic core hardening are complete, but production authority resolution, migration, eligibility issuance, projection generation, manifest generation, and downstream activation remain unimplemented and unauthorized.

OAR Phase 1B.1 is completed and merged through PR #26. Phase 1B.2 Versioned Verification Result Contract is completed, merged through PR #28, and repository-effective. No later implementation milestone is selected or authorized.

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

## D3 Pilot Status

D3 — Indexed Marker Syntax Validation is completed, merged in PR #32, and repository-effective as a syntax-only pilot artifact. PR #32 merged at `2026-07-18T12:55:52Z` through true merge commit `f2677698d0d0e7599e5e8e686c6eb38bf9bc3a35`; its first parent is pre-merge main `9774c569fa3d631ee4ad56e0d865595b26c4f2d6`, and exact reviewed head `8b4c3e525cec7d9c0ee82437f39981ae25d7e01d` is its second parent. Exactly the six authorized PR #32 paths landed. The pilot scope is:

- Indexed marker syntax validation contract defined (`docs/d3-indexed-marker-syntax-contract.md`). Matching `<field>[<zero-based-index>].<subfield>` establishes syntax only and grants no rule-specific, schema-level, runtime, or activation authority; rule-specific indexed-marker authorization remains a separate fail-closed semantic gate.
- Validation logic implemented as a standalone module (`validators/d3_indexed_marker_validator.py`). Not registered in the active business-rule registry.
- Automated test suite: 22 tests passing (positive paths for ADR-006 approved forms, rejection of wildcards, empty indices, ranges, JSONPath, unknown-index placeholders, fuzzy/semantic indices, missing subfields, leading/trailing delimiters).
- Full locked suite: 202 tests pass, with 1 pre-existing unrelated skip; no regression.
- No BR-006 activation, real-data processing, production activation, schema changes, or downstream activation.
- Exact-head CI run `29644480824` completed successfully.
- Final Tier 2 review on the exact head concluded `APPROVE WITH NON-BLOCKING NOTES` from Claude / Anthropic Sonnet 5 class (blocking 0, major 0, minor 0) and Qwen3-Max via Nous/Hermes (blocking 0, major 0, one non-blocking Minor). The Owner qualified Qwen3-Max via Nous/Hermes as Perspective 2, treating Hermes as an execution/orchestration shell and explicitly accepting the shared operator context as non-disqualifying. D3-M01 was `ACCEPTED MAJOR`, corrected, and independently confirmed `FULLY RESOLVED`.

The D3 pilot contract and validator remain fictional/test-only, outside the active business-rule registry, and not runtime active. D3 validates attempted indexed-marker syntax only. Syntax validity grants no schema, rule-specific, runtime, BR-006, production, downstream, or activation authority, and bare top-level markers remain outside D3 adjudication authority.

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

## OAR Phase 1B.1 closure

PR #26 completed OAR Phase 1B.1 within its exact ten-path allowlist: project metadata, one authoritative universal dependency lock, runtime/test dependency separation, Python 3.11/3.12 support, reproducible installation, CI installation from the lock, and development package build/install validation. It did not relocate runtime resources, change CLI semantics, stabilize a public interface, or expand into Phase 1B.2 or Phase 2. The existing fictional OAR chain and closed Phase 1A behavior remain unchanged: the offline verifier checks RFC 8785/SHA-256 bindings, a separately supplied trust anchor, the non-self-authorizing publication bootstrap, ordinary closed-world membership, exact subject/envelope binding, authorized revocation before authority supersession, independent business-subject supersession, and deterministic fictional run metadata, eligibility, and selection outcomes. It executes two positive scenarios and preserves all twenty negative first-failure expectations.

Module-global `_LAST_TRACE` was removed. Trace is invocation-local and available only through a private test helper; public verification and CLI output remain trace-free. Success, `semantic_rejection`, and `resource_rejection` are distinguishable. Multiple effective business-key candidates fail closed, and snapshot, authority, and business-subject lifecycle traversal has cycle and depth protection. Fixed artifact-nonconfigurable ceilings cover 64 inventory artifacts, 256 KiB per JSON file, 2 MiB total admitted JSON, 256 snapshot entries, and depth 64. The depth ceiling is defensive and does not evidence an accepted 64-link scenario; resource checks do not solve TOCTOU.

This closure does not provide real trust-anchor delivery, real registry publication, real run metadata authority, authority or revocation issuance, R03 eligibility or selection, projection or manifest activation, calendar downstream activation, BR-006 activation, D3 resolution, or published-output recall. All OAR schemas remain inactive Draft 0.x artifacts.

## Known Technical Debt

- Some existing files include encoding-sensitive Chinese text; use UTF-8 aware reads and writes.
- Business rule specs and implementations must stay aligned before adding validators.
- BR-005 must remain deterministic and avoid semantic, NLP, or fuzzy judgement.
- BR-006 runtime activation remains held pending vertical-slice evidence, indexed marker syntax validation, and owner approval.
- P21-F01 is addressed by the repository-effective Phase 1B.2 contract: `VerificationResult` construction is keyword-only and serialization is versioned as `verification-result/v1`.
- P28-F01 remains accepted non-blocking debt: `VerificationResult` classification and cross-field invariants are not runtime-enforced. This is separately authorized future hardening, not completed work.
- P28-N01 remains optional future test hardening: explicit automated tests for contract-version non-overridability and frozen immutability.
- The Greptile test-completeness note remains accepted non-blocking future test hardening: the success payload test does not explicitly assert that all rejection fields are null.
- P21-F02 is accepted non-blocking debt: lifecycle depth 64 is a defensive secondary ceiling constrained by inventory and multi-artifact chain structure. Enforcement is independently tested at all three traversal locations; no accepted 64-link scenario is claimed.
- Phase 1B.1 dependency and package foundation is completed and repository-effective through merged PR #26.
- Phase 1B.2 is limited to the selected versioned result contract; remaining interface work and Phase 2 secure filesystem admission remain deferred, unauthorized, and inactive.

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
- D3 = Indexed Marker Syntax Validation (syntax-only pilot artifact completed and repository-effective through merged PR #32)

Next steps:

1. No later implementation milestone is selected or authorized.
2. `OD-REVIEW-QUALIFICATION-001` Option D, Revised Candidate v2 is completed, merged in PR #30, and repository-effective. PR #30 merged at `2026-07-18T10:47:04Z` through true merge commit `66eca55b18d44d9ed5a7044ecc878ce1677541c2`; its first parent is `d21ea123091bf5159a3eb500602062157154d103`, and exact reviewed head `ba5a24a6ea563fed8c0d8bc2067dd97f9a50f235` is its second parent. The reviewed-head tree and merge tree are both `774631205803536b7fc76831c04f0919374e750f`, and exactly `docs/current-status.md`, `docs/decisions.md`, `docs/governance.md`, and `docs/roadmap.md` landed. Exact-head CI run `29626802862` completed successfully. Fable and Claude both concluded `APPROVE WITH NON-BLOCKING NOTES`, with zero blocking and zero major findings; P30-F01 remains carried as a non-gating Minor. The decision applies prospectively and non-retroactively and does not authorize Phase 2, any runtime or production activation, or any later implementation milestone.
3. D3 / indexed marker syntax validation is completed and repository-effective through merged PR #32. It remains a standalone fictional/test-only syntax validator outside the active registry and grants no schema, rule-specific, runtime, BR-006, production, downstream, or activation authority.
4. Plan real vertical-slice evidence only with separate owner approval.
5. Require real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval before BR-006 runtime activation.
6. Keep Phase 2 and all scope beyond the completed Phase 1B.2 result contract deferred, unauthorized, and inactive until separately approved.
