# Roadmap

## Current Focus

Milestone 3.8 / D2A — Machine-readable Validation Findings Contract

This contract-only milestone defines future machine-readable schema and business validation findings artifacts without implementing JSON output or changing validators.

## Completed Milestones

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

## Active Milestone

### Milestone 3.8 / D2A — Machine-readable Validation Findings Contract

- Define the future `schema_findings.json` and `business_findings.json` artifact contracts.
- Define status semantics, error taxonomy, the run-level `fail` / `message` exception, and non-retroactive requiredness.
- Do not implement JSON output or change validators.

## Paused / Backlog

### BR-006 Per-Session Date Completeness

Implemented, activation held. Requires vertical-slice evidence, indexed marker syntax validation, and explicit owner approval before runtime activation.

## Planned Milestones

### Delivery Naming Map

- D1 = Milestone 3.7 — Pipeline Run Contract (completed and merged)
- D2A = Milestone 3.8 — Machine-readable Validation Findings Contract
- D2B = future implementation, only after separate approval
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
- Preserve participant-facing practical details.
- Avoid publishing unresolved uncertainty.
