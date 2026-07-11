# Roadmap

## Current Focus

Milestone 3.7 / D1 — Pipeline Run Contract

This milestone defines the auditable per-run artifact, stage, ownership, failure-boundary, and closure contract without implementing a runner.

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

## Active Milestone

### Milestone 3.7 / D1 — Pipeline Run Contract

- Define the required `data/runs/<run_id>/` artifact layout and commit policy.
- Define pipeline stages, failure boundaries, mutation ownership, record status mapping, run outcomes, and conditional approval artifacts.
- Preserve forward compatibility for D2 without defining machine-readable findings JSON or implementing a runner.

## Paused / Backlog

### BR-006 Per-Session Date Completeness

Implemented, activation held. Requires vertical-slice evidence, indexed marker syntax validation, and explicit owner approval before runtime activation.

## Planned Milestones

### Delivery Naming Map

- D1 = Milestone 3.7 — Pipeline Run Contract
- D2 = future Machine-readable Findings Contract
- D3 = future Indexed Marker Syntax Validation

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
