# Roadmap

## OAR closure

The Bounded Calendar Authority Chain v0 architecture is frozen. PR #18 completed and merged the accepted OAR contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures. PR #19 completed and merged the independently reviewed fictional year-2099 offline verifier prototype. PR #21 completed Phase 1A deterministic verifier core hardening. Production operation and activation remain outside all three merges.

## Milestone State

OAR Phase 1B.1 Dependency and Package Foundation completed and became repository-effective when PR #26 merged at `2026-07-17T13:52:58Z` through true merge commit `466ec18c0b232bfa99de1822124e35ae39495def`. Its first parent is `1375235a9e00df5a8e3835fe58a326dc16883874`, and merged head `5c9ffd88246a491eb9bf6043744428c4e2574a9a` is its second parent. The merged-head tree and merge tree are equal, and exactly the approved ten implementation paths landed.

Phase 1B.2 — Versioned Verification Result Contract is `COMPLETED — MERGED IN PR #28 / REPOSITORY-EFFECTIVE`. PR #28 merged at `2026-07-18T00:40:55Z` through true merge commit `b1f7c5ad67a3eb5900b7323f8756ab319e27294c`; its first parent is `3600f4f004ca46ed4392e3b0c4fdff6f3ad6c30a`, and reviewed head `a264d60d943fc9137120dc886eea16c9948bec51` is its second parent. It stabilizes only `verification-result/v1`, keyword-only `VerificationResult` construction, and `to_payload()` as authoritative CLI JSON serialization. It provides no console entry point, package-version change, installed-wheel standalone CLI, runtime resource relocation, repository-root argument, CLI argument redesign, filesystem admission, TOCTOU remediation, symlink policy, production authority, real trust-anchor delivery, schema activation, Phase 2, projection, manifest, downstream activation, BR-006, or D3.

### OD-REVIEW-EVIDENCE-002 publication

Status: `COMPLETED — REPOSITORY-EFFECTIVE`

- PR #24 merged at `2026-07-17T05:47:09Z` through true merge commit `cd30a42bde387b66df0f99e117d7c2fd57b16b88`.
- Its first parent is `fb09d2ea547615a70299986608dba9f459c1e544`; exact doubly reviewed head `9443dd0fc1624b3853cfc7ffbb3a941b4498bf11` is its second parent.
- Fable and Claude each reviewed the same exact head and concluded `APPROVE WITH NON-BLOCKING NOTES`, with zero blocking and zero major findings.
- The reviewed-head tree and merge tree were verified equal, and exactly four authorized documentation paths landed.
- `OD-REVIEW-EVIDENCE-002` is prospective: it does not retroactively invalidate PR #23 or earlier merged PRs and applies to every PR that was unmerged when PR #24 merged and to every future Tier 1 and Tier 2 PR.

Phase 1B.1 is authorized only within its approved boundary. Phase 1B.2 interface stabilization, Phase 2 TOCTOU remediation and secure filesystem admission, production authority, trust-anchor delivery, schema activation, projection or downstream activation, BR-006, D3, manifest activation, deployment activation, real-data activation, Greptile installation or qualification, GOV-DEBT-001, and GOV-DEBT-002 remain deferred or unauthorized.

D2B is completed and merged in PR #10. Validation Findings JSON emission is implemented while preserving existing `PASS` / `FAIL` text structure and exit code semantics. Missing, `None`, or empty `activity_id` values are consistently rendered as `"<missing>"` under Finding Contract v1. D1 JSON artifact requirements are prospective and non-retroactive. No pipeline runner exists.

## Completed Milestones

### OAR Phase 1B.1 - Dependency and Package Foundation

- PR #26 completed and merged the approved dependency and package foundation through true merge commit `466ec18c0b232bfa99de1822124e35ae39495def`.
- Added project metadata, one authoritative universal dependency lock, runtime/test dependency separation, Python 3.11/3.12 support, reproducible installation, locked CI, and development package build/install validation.
- Preserved CLI semantics, the pre-stable public interface, existing runtime resource locations, and all Phase 1A behavior.
- Phase 1B.2 and Phase 2 remain deferred, unauthorized, and inactive.

### OAR Contracts and Fictional Authority Verifier

- PR #18 accepted and merged the OAR contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures.
- PR #19 accepted and merged the fictional offline verifier for the exact year-2099 scope.
- The prototype verifies RFC 8785/SHA-256 identity, a separately supplied trust anchor, publication bootstrap, ordinary membership, subject/envelope binding, revocation-first lifecycle resolution, business-subject supersession, deterministic outcomes, two positive scenarios, and twenty negative first-failure cases.
- Historical PR #19 merge validation baseline: 147 passed, one pre-existing unrelated skip.

### Phase 1A - Deterministic Verifier Core Hardening

- PR #21 completed and merged at `2026-07-16T12:29:34Z` as `bf5063c2cdcb8d3cf915c5405dfb7fed26648683`.
- Replaced module-global trace state with invocation-local internal/test-only tracing while keeping public verifier and CLI output trace-free.
- Added fixed resource ceilings, distinct `resource_rejection`, fail-closed effective business-key ambiguity, and lifecycle cycle/depth protection.
- Preserved both positive fictional outcomes, all twenty negative first-failure expectations, and OAR-N15 as construction-invariant only.
- Final validation: 172 passed, one pre-existing unrelated skip; Ubuntu and Windows passed on Python 3.11 and 3.12.
- Independent review: `APPROVE WITH NON-BLOCKING NOTES`; zero blocking findings, zero major findings, and P1A-F01 genuinely resolved.
- P21-F01 and P21-F02 remain accepted non-blocking notes concerning a pre-stable positional result field and the defensive depth ceiling. Neither is a production blocker or architecture reopening.
- Scope remains fictional year-2099 only; no schema, authority, production operation, or downstream activation was accepted.

### Milestone 1 - Foundation

- Repository structure established.
- Extraction and QA workflow documents started.
- Initial project plan documented.

### Milestone 2 - Validation Engine

- Activity schema defined.
- Schema validator added.
- Output contracts documented.
- Regression test foundation added.

### Milestone 3 - Business Rule Engine

- BR-001 Required Fields completed.
- BR-002 Fee Uncertainty completed.
- BR-003 Registration Period completed.
- BR-004 QA Status completed.
- BR-005 Source Reference completed.
- Milestone 3.6F BR-006 Activation Hold completed; implementation and direct unit coverage are retained while runtime activation remains held.

### Milestone 3.7 / D1 — Pipeline Run Contract

Status: Completed and merged — the auditable per-run artifact, stage, ownership, failure-boundary, and closure contract is defined.

## D2 Delivery Track

### Milestone 3.8 / D2A — Machine-readable Validation Findings Contract

- Define the future `schema_findings.json` and `business_findings.json` artifact contracts.
- Define status semantics, error taxonomy, the run-level `fail` / `message` exception, and non-retroactive requiredness.
- Do not implement JSON output or change validators.

Status: Completed and merged — D2A remains the contract-only design baseline.

### Milestone 3.9 / D2B — Machine-readable Validation Findings Emission

Status: Completed and merged in PR #10.

- Add optional `--run-id` and `--json-output` arguments to both existing validators.
- Emit Validation Findings JSON Contract v1 pass, fail, and error artifacts.
- Preserve existing `PASS` / `FAIL` text structure, validation precedence, and exit code semantics, with Finding Contract v1 normalization of unavailable `activity_id` values to `"<missing>"`.
- Keep invalid arguments pre-artifact and keep BR-006 inactive.

## Paused / Backlog

### Scoped Downstream Eligibility Implementation

Option D and ADR-007 are accepted architecture. Builder and consumer-validator implementation, runtime artifacts, migration, and activation remain pending separate authorization.

### Calendar-Only Vertical Slice Contracts

Status: historical contract drafting completed. Direction remains per-activity canonical projections plus a monthly manifest bound exactly to a separate externally authorized monthly selection.

- Draft eligibility, authority registry, monthly selection, projection, and manifest schemas at `0.x`.
- Keep exact-field eligibility permission separate from monthly publication inclusion.
- Require external revocation verification and complete selection-to-manifest and manifest-to-projection binding.
- Require typed non-transferable authority purposes and exact canonical authorization-subject digest binding.
- Design fictional positive and negative fixtures without creating R03 artifacts.
- Require implementation validation, independent review, and owner acceptance before runtime activation.
- The fictional authority/revocation verifier blocker was resolved by PR #19. Real authoritative inputs, production trust-anchor delivery, real registry publication, downstream provenance, and activation remain blocked.

### Bounded Authority Input and Registry Publication

Status: contract package and fictional executable verification completed. Draft schemas remain inactive; production acceptance and operation remain unauthorized.

- Require exactly one externally supplied trust anchor and one self-contained verified resolution bundle.
- Bind a logical `registry_id` to immutable published `snapshot_id` versions without treating them as synonyms.
- Use separate `calendar-registry-publication` authority and a non-circular subject-to-artifact digest construction.
- Define closed-world snapshot lifecycle, rollback detection, deterministic inventory, run/month equality, and single-primary enforcement ownership.
- Keep real run metadata authority, real trust-anchor delivery, real authority/revocation issuance, registry publication, remaining production hardening, and owner activation acceptance blocked.

### OAR hardening sequence

Phase 1B.1 — Dependency and Package Foundation: `COMPLETED — MERGED IN PR #26 / REPOSITORY-EFFECTIVE`. This completed milestone covers dependency locking, runtime/test dependency separation, Python 3.11/3.12 support, reproducible installation, locked CI, package metadata, and development package build/install validation.

Phase 1B.2 — Versioned Verification Result Contract: `COMPLETED — MERGED IN PR #28 / REPOSITORY-EFFECTIVE`. The completed scope stabilizes `verification-result/v1`, makes `VerificationResult` construction keyword-only, and makes `to_payload()` the authoritative serializer used by CLI JSON. Exactly `README.md`, `docs/current-status.md`, `docs/decisions.md`, `docs/roadmap.md`, `tests/test_oar_result_contract.py`, `tools/oar_verifier/errors.py`, `tools/oar_verifier/verifier.py`, and `tools/verify_fictional_authority.py` landed. A console entry point, package-version change, installed-wheel standalone CLI, runtime resource relocation, repository-root argument, CLI argument redesign, filesystem admission, TOCTOU remediation, symlink policy, production authority, real trust-anchor delivery, schema activation, Phase 2, projection, manifest, downstream activation, BR-006, and D3 are excluded.

Phase 2 — Secure Filesystem Admission: `DEFERRED — NOT AUTHORIZED / NOT ACTIVE`. Potential future scope, subject to separate owner approval, includes TOCTOU remediation, immutable or staged input acquisition, descriptor-based safe reads where appropriate, symlink and intermediate-directory policy, secure trust-anchor filesystem custody, and filesystem race/mutation testing.

Phase 1B.2 is completed and repository-effective through merged PR #28. No later implementation milestone is selected or authorized; Phase 2 remains deferred, unauthorized, and inactive.

`OD-REVIEW-QUALIFICATION-001` Option D, Revised Candidate v2 is `COMPLETED — MERGED IN PR #30 / REPOSITORY-EFFECTIVE`. PR #30 merged at `2026-07-18T10:47:04Z` through true merge commit `66eca55b18d44d9ed5a7044ecc878ce1677541c2`; its parents are authoritative base `d21ea123091bf5159a3eb500602062157154d103` and exact reviewed head `ba5a24a6ea563fed8c0d8bc2067dd97f9a50f235`, whose tree equals the merge tree at `774631205803536b7fc76831c04f0919374e750f`. Exactly `docs/current-status.md`, `docs/decisions.md`, `docs/governance.md`, and `docs/roadmap.md` landed. Its effect is prospective and non-retroactive; P30-F01 remains carried as a non-gating Minor. It authorizes no Phase 2, production, runtime, schema, real-data, projection, manifest, downstream, BR-006, or D3 activation and selects or authorizes no later implementation milestone.

### BR-006 Per-Session Date Completeness

Implemented, activation held. Requires vertical-slice evidence, indexed marker syntax validation, and explicit owner approval before runtime activation.

## Planned Milestones

### Delivery Naming Map

- D1 = Milestone 3.7 — Pipeline Run Contract (completed and merged)
- D2A = Milestone 3.8 — Machine-readable Validation Findings Contract
- D2B = Milestone 3.9 — additive validator JSON artifact emission (completed and merged in PR #10)
- D3 = Indexed Marker Syntax Validation (syntax-only bounded pilot in Draft PR #32 on branch `pilot/d3-indexed-marker-syntax`; automatic Tier 2 for new contract semantics, with both reviewer perspectives pending)

### Milestone 3.5B - BR-006 Specification Review

Status: Completed — the BR-006 specification was reviewed and aligned before implementation.

- Review BR-006 draft.
- Patch the specification if required.
- Confirm whether the rule is per-record, per-session, or batch scoped.

### Milestone 3.6 - BR-006 Implementation

Status: Completed — BR-006 was implemented with focused direct unit coverage.

- Implement BR-006 only after specification approval.
- Add focused validator tests.
- Run full regression tests.

### Milestone 3.6F - BR-006 Activation Hold

Status: Completed — BR-006 remains implemented with direct unit coverage but is not included in the active runtime registry.

- Runtime activation remains held.
- Activation still requires real vertical-slice evidence, D3 indexed marker syntax validation in place before or together with activation, and explicit owner approval.

### Milestone 4 - QA Engine

- Define QA finding contracts.
- Add source-comparison workflow support.
- Clarify Human Review handoff outputs.

### Milestone 5 - Newsletter Generation

- Use approved records only.
- Require consumer-scoped owner eligibility; record approval alone is not permission.
- Preserve participant-facing practical details.
- Avoid publishing unresolved uncertainty.
