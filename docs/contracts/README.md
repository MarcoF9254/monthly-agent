# Contract Index

## Active Contracts

- `docs/pipeline-run-contract.md` — D1 auditable run contract.
- `docs/output-contracts.md` — validator output contracts.

## Accepted Architecture, Draft Executable Contracts

- `docs/contracts/scoped-consumer-eligibility-contract.md`
- `docs/contracts/external-authority-registry-contract.md`
- `docs/contracts/calendar-monthly-selection-contract.md`
- `docs/contracts/calendar-projection-contract.md`
- `docs/contracts/calendar-only-vertical-slice-contract.md`

Draft executable schemas:

- `schemas/drafts/calendar-only/scoped-eligibility-decision.schema.json`
- `schemas/drafts/calendar-only/external-authority-registry.schema.json`
- `schemas/drafts/calendar-only/calendar-monthly-selection.schema.json`
- `schemas/drafts/calendar-only/calendar-activity-projection.schema.json`
- `schemas/drafts/calendar-only/calendar-monthly-manifest.schema.json`

They are version `0.x`, are not accepted or runtime-active, and are not inputs to existing validators. `OD-CAL-ARCH-003` is accepted contract clarification only.

## Fictional Test Design

- `docs/contracts/calendar-only-fictional-fixture-test-matrix.md`

## Gate 2 Bounded Authority Input Drafts

Contracts:

- `docs/contracts/authority-resolution-input-contract.md`
- `docs/contracts/trust-anchor-contract.md`
- `docs/contracts/registry-snapshot-contract.md`
- `docs/contracts/registry-publication-contract.md`
- `docs/contracts/resolution-bundle-contract.md`
- `docs/contracts/run-metadata-binding-contract.md`
- `docs/contracts/authority-resolution-enforcement-matrix.md`
- `docs/contracts/bounded-authority-fictional-fixture-test-matrix.md`

Draft schemas:

- `schemas/drafts/bounded-authority-input/trust-anchor.schema.json`
- `schemas/drafts/bounded-authority-input/authority-registry-snapshot.schema.json`
- `schemas/drafts/bounded-authority-input/registry-publication-authority.schema.json`
- `schemas/drafts/bounded-authority-input/resolution-bundle-root.schema.json`
- `schemas/drafts/bounded-authority-input/authoritative-run-metadata.schema.json`

`OD-BAI-ARCH-001` accepts the external-anchor and bounded-bundle direction with owner changes. `OD-BAI-CONTRACT-001` authorizes drafting only. These `0.x` schemas and fictional fixtures are inactive, not accepted as executable, and are not runtime validator inputs.

The positive `valid-resolution-chain` fixture directory represents a valid Gate 2 resolution-input chain only. It covers trusted-tip anchoring, registry publication, closed-world snapshot identity, bounded bundle completeness, ordering, and run-metadata binding. It does not provide executable end-to-end verification of the separate owner-authority artifacts referenced by eligibility or monthly-selection decisions. Those schemas, fixtures, and verifiers remain a separate blocker requiring separate owner authorization.

Architecture acceptance does not activate a contract. Draft schemas require implementation validation, independent review, and explicit owner acceptance before runtime use.
