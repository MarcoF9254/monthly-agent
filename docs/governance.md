# Governance

## OAR boundary

OAR drafts confer no implementation or operational authority. Reason-code values require separate governance. Artifact integrity is not independent authentication. Real authority, revocation, publication, run metadata, activation, BR-006, and D3 remain unauthorized.

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

## Risk-Based Independent Review Policy

Status: Accepted under `OD-REVIEW-POLICY-001` (Option C).

### Purpose and control separation

No pull request is review-exempt. CI, independent review, Owner approval, and merge verification are separate controls:

- CI cannot replace independent review.
- Review approval cannot replace Owner merge authorization.
- Review must bind the repository, PR, exact base SHA, exact head SHA, changed-path scope, tier, reviewer identity, and verdict.

### Identities and substantive initiation

Each review record distinguishes:

- Git commit author;
- work-product author;
- substantive initiator;
- independent reviewer;
- second independent reviewer when Tier 2 requires one;
- Owner / Final Approval Authority; and
- Merge Authority.

A substantive initiator is a person or agent who materially determines specific claims, decision content, authority direction, or a normative outcome, even when not the Git author. General milestone authorization, scope limits, factual sources, or acceptance criteria do not automatically make the Owner the work-product author. Predetermining a decision conclusion, policy text, authority rule, review verdict, or disputed final claim normally makes that person a substantive initiator.

### Independence

Every PR requires at least one qualified reviewer independent from its work-product author. Difference in Git authorship alone does not establish independence.

The Owner may act as an independent reviewer only when the Owner did not materially initiate the reviewed claims or decision content. When the Owner is a substantive initiator:

- the Owner cannot be the sole independent reviewer;
- an additional qualified independent reviewer is required; and
- the substantive-initiator determination and rationale must be recorded.

### Classification ownership

The work-product author may propose a tier but cannot make the final downgrade decision. An author-external independent reviewer records:

- tier and triggered gates;
- why Tier 2 is or is not required;
- exact base SHA and reviewed head SHA;
- changed paths;
- Git author and work-product author;
- substantive initiator and rationale; and
- reviewer-independence conclusion.

### Tier 1

Tier 1 requires one qualified author-external independent reviewer, exact diff and scope review, applicable current-head validation and CI, Owner approval, a true merge commit, and post-merge identity and landed-scope verification. Tier 1 is neither review exemption nor reduced-quality review.

### Tier 2

Tier 2 requires two qualified independent review perspectives covering the same exact head, finding adjudication, applicable current-head CI, Owner final approval, a true merge commit, and post-merge verification.

The default second independent model is Claude. If Claude is unavailable, the Owner designates another qualified independent model or reviewer and records the reason and replacement identity. The replacement cannot be the work-product author or substantive initiator, and the work-product author cannot approve the replacement.

### Automatic Tier 2 triggers

Tier 2 is automatic for:

- modification of `docs/governance.md`;
- review, approval, merge, or exception-policy changes;
- evidence-hierarchy or decision-hierarchy changes;
- semantic changes to an ADR or Owner Decision;
- contract or schema semantic changes;
- activation or deactivation of executable contracts;
- authority, trust, revocation, authentication, identity, custody, access-control, signature, fail-open/fail-closed, filesystem-security, or production-threat changes;
- production runtime, migration, real-data write, external publication, destructive action, or downstream activation;
- a blocking or major review finding;
- correction of a high-risk finding;
- unresolved doubt about reviewer independence; or
- Owner-requested Tier 2 review.

Pure contract-index navigation changes are inspection signals, not automatic Tier 2 triggers by themselves.

### Factual reconciliation gates

A factual reconciliation may be Tier 1 only when all of these conditions hold:

- exact path allowlist;
- exact accepted source for every new current-state claim;
- no proposal, option, recommendation, or unapproved policy;
- no new authority, scope, or exception;
- no contract, schema, runtime, or governance semantic change;
- milestone or activation status records only an already-completed Owner decision;
- historical and current states remain distinct;
- stale-state search passes;
- protected paths remain unchanged;
- an independent reviewer confirms classification;
- current-head validation and repository references pass; and
- substantive-initiator and independence determinations are recorded.

Claims of completed Owner decisions cite exact evidence such as an ADR ID, Owner Decision ID, exact `docs/decisions.md` entry, approved PR and reviewed head, dated Owner approval record, or merge commit and date.

### Classification signals

Changes to `docs/decisions.md` default to Tier 2. They may be Tier 1 only when recording an already-approved decision with exact source mapping and no change to decision semantics.

Changes to `docs/contracts/README.md`, and terms including authority, scope, activation, milestone, trust, revocation, production, exception, and override, require explicit inspection. They do not determine the tier unless another automatic trigger applies.

### New-head rule

Any commit added after review invalidates prior merge eligibility. The new exact head requires re-review, current-head CI, and renewed path, scope, and tier verification. An earlier GREEN or APPROVE is not inherited. Both Tier 2 reviewers must cover the new head.

### Merge method and post-merge proof

Tier 1 and Tier 2 PRs require a true merge commit. Squash and rebase merges are prohibited.

Post-merge verification requires:

- exactly two merge parents;
- first parent equal to the authorized base;
- second parent equal to the authorized reviewed head; and
- landed diff equal to reviewed scope.

If repository merge methods change, an equivalent approved head-pinning proof must exist before squash or rebase may be used. Changing this merge-method rule is itself a Tier 2 governance change.

### Non-waivable high-risk Tier 2 review

Tier 2 requirements involving production authority, security, destructive operations, or real-data activation cannot be waived. If Claude is unavailable, another qualified independent reviewer must be designated. If none is available, the PR stops. The Owner, work-product author, or substantive initiator cannot replace real-time independent review with self-certification.

Break-glass incident handling is outside this policy and requires a separate Tier 2-reviewed governance decision.

### Exceptions for other categories

Any permitted one-time exception outside the non-waivable categories records:

- exact PR and head;
- waived requirement;
- reason and known risk;
- compensating controls;
- one-time scope or expiry;
- independence record; and
- an explicit statement that no general precedent is created.

Exception-policy changes require Tier 2 review.

### Tier 1 audits

The Owner may periodically audit merged Tier 1 PRs for classification correctness, factual-gate evidence, source mapping, substantive-initiator determination, reviewer independence, exact-head review and CI evidence, and missed Tier 2 triggers.

Audits do not retroactively invalidate a merged PR. They provide policy-health feedback, may trigger future issues, supplemental review, policy revision, or corrective milestones, and should retain a concise record.

### Required PR classification record

Each gated PR records:

~~~text
Tier:
Git author:
Work-product author:
Substantive initiator and rationale:
Independent reviewer:
Second independent reviewer:
Automatic triggers:
Tier 2 rationale:
Base SHA:
Reviewed head SHA:
Changed paths:
Current-head validation:
Owner approval:
True merge commit:
~~~

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

Under `OD-BAI-ARCH-001`, trust-anchor delivery, bundle verification, snapshot validation, publication-authority verification, lifecycle resolution, artifact-authority verification, and run-metadata validation remain separate accountable boundaries. Each blocking rule has exactly one primary enforcing component. Storage location never confers authority. `OD-BAI-CONTRACT-001` authorizes inactive drafting, not executable acceptance or implementation.
