# Roadmap

## OAR closure

The Bounded Calendar Authority Chain v0 architecture is frozen. PR #18 completed and merged the accepted OAR contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures. PR #19 completed and merged the independently reviewed fictional year-2099 offline verifier prototype. Production operation and activation remain outside both merges.

## Current Focus

No next milestone is selected. OAR contract drafting and the fictional verifier prototype are complete; production authority resolution is not authorized.

D2B is completed and merged in PR #10. Validation Findings JSON emission is implemented while preserving existing `PASS` / `FAIL` text structure and exit code semantics. Missing, `None`, or empty `activity_id` values are consistently rendered as `"<missing>"` under Finding Contract v1. D1 JSON artifact requirements are prospective and non-retroactive. No pipeline runner exists.

## Completed Milestones

### OAR Contracts and Fictional Authority Verifier

- PR #18 accepted and merged the OAR contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures.
- PR #19 accepted and merged the fictional offline verifier for the exact year-2099 scope.
- The prototype verifies RFC 8785/SHA-256 identity, a separately supplied trust anchor, publication bootstrap, ordinary membership, subject/envelope binding, revocation-first lifecycle resolution, business-subject supersession, deterministic outcomes, two positive scenarios, and twenty negative first-failure cases.
- Merge validation baseline: 147 passed, one pre-existing unrelated skip.

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
- Keep real run metadata authority, real trust-anchor delivery, real authority/revocation issuance, registry publication, production hardening, and owner activation acceptance blocked.
- Replace the prototype-only module-global lifecycle trace before concurrent or production use.

### BR-006 Per-Session Date Completeness

Implemented, activation held. Requires vertical-slice evidence, indexed marker syntax validation, and explicit owner approval before runtime activation.

## Planned Milestones

### Delivery Naming Map

- D1 = Milestone 3.7 — Pipeline Run Contract (completed and merged)
- D2A = Milestone 3.8 — Machine-readable Validation Findings Contract
- D2B = Milestone 3.9 — additive validator JSON artifact emission (completed and merged in PR #10)
- D3 = future Indexed Marker Syntax Validation (pending clarification)

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
