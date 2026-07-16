# Governance

## Purpose

This document defines the architecture governance for `monthly-agent`.

Governance is a meta-layer. It governs how architecture, specifications, implementation, and validation evolve. It is not part of the runtime pipeline, not another architecture layer, and not a runtime component.

Governance is never considered complete. It evolves together with the project.

## Governance Position

Governance governs the following workflow:

```text
Architecture
        |
        v
Specification
        |
        v
Implementation
        |
        v
Validation
```

Governance applies across every stage above. Governance is not part of the workflow itself.

## Relationship to Existing Documents

`docs/architecture.md` defines the system architecture, pipeline, and runtime responsibilities.

`docs/decisions.md` records accepted architecture decisions as ADRs. It does not contain proposals.

`docs/governance.md` defines cross-cutting governance principles. It governs how architecture decisions are proposed, reviewed, approved, implemented, and maintained.

This document defines governance only.

It does not redefine:

- runtime architecture
- pipeline
- schemas
- ADR content

Those responsibilities remain within their respective documents.

This document should reference existing architecture and decision records rather than duplicating them.

## Architecture Principles

1. Specification before implementation.

2. Boundary documents define contracts, not runtime components.

3. Evidence precedes policy.

4. Business authority decisions require human approval.

5. ADRs record accepted architecture, not proposals.

6. Implementation follows architecture.

7. Every accepted policy must be traceable to repository evidence, or be explicitly marked as pending. Evidence supports correctness; authority approves adoption.

8. Format acceptance does not determine source authority.

Evidence demonstrating that a phenomenon exists does not itself authorize adoption. Authority decisions still follow Principle 4.

Accepted input formats describe extractor capability only. They do not determine which source is authoritative.

## Evidence Hierarchy

### Observational Evidence

Observational evidence shows that a phenomenon exists.

Examples include the architecture-review corpus.

Observational evidence is not authoritative. It cannot by itself justify policy adoption.

### Contractual Evidence

Contractual evidence represents approved project agreements.

Examples include:

- `docs/architecture.md`
- `docs/decisions.md`
- schemas
- output contracts
- approved ADRs

The evidence hierarchy is:

```text
Observational Evidence
        |
        v
Contractual Evidence
        |
        v
Approved Policy
```

Observational evidence never becomes approved policy without human approval.

## Decision Hierarchy

Authority decisions override evidence sufficiency.

A proposal may have complete evidence while still remaining:

```text
DECISION PENDING — Requires Human Approval
```

until approved.

## Pending Decision Convention

Pending decisions must always contain:

- options
- trade-offs
- one recommendation

Pending decisions must use this label:

```text
DECISION PENDING — Requires Human Approval
```

Architecture documents SHOULD group pending decisions together near the end of the document unless there is a strong documented reason otherwise.

## Review Workflow

### Architecture Lead

Responsibilities:

- architecture coherence
- authoring
- integration

### Independent Architecture Review

Responsibilities:

- challenge hidden assumptions
- identify wording that unintentionally creates policy
- identify governance drift

### Implementation

Responsibilities:

- implement approved specifications only

Role separation is a governance mechanism, not a capability hierarchy.

Role separation exists to reduce authorship bias. It is not a ranking of model capability.

No role should both author and independently review the same architecture artefact.

## ADR Policy

ADRs are recorded in `docs/decisions.md`.

ADRs record accepted architecture only.

They never record:

- proposals
- pending decisions
- discussion notes

## Draft Executable Contract Lifecycle

Accepted architecture may authorize contract drafting without activating an executable contract. Draft JSON Schemas must use a `0.x` version and remain outside runtime validator inputs.

A draft executable contract cannot become runtime-active until:

1. implementation validation is complete;
2. independent review is complete; and
3. the owner explicitly accepts activation.

Architecture acceptance, schema validity, and fictional-fixture success do not themselves grant business authority or downstream activation.

For calendar contract drafting, eligibility, monthly publication selection, and authority revocation are separate typed, non-transferable authority purposes. Every verification must match expected, registry, and externally verified artifact purposes and the exact canonical authorization-subject digest and scope. Registry metadata cannot authenticate a grant or revocation. `OD-CAL-ARCH-002` approves selection and binding revision; `OD-CAL-ARCH-003` accepts this contract clarification only, without accepting or activating any executable schema.
