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

The Owner may act as an independent reviewer only when the Owner did not materially initiate the reviewed claims or decision content. When the Owner is a substantive initiator, the Owner cannot serve as or count toward any required independent review perspective. Tier 1 therefore requires another qualified reviewer; Tier 2 requires two qualified reviewers who are not the Owner, the work-product author, or another substantive initiator. The Owner may still comment and retain final approval and merge authority, but those actions do not satisfy or replace an independent-review gate. The substantive-initiator determination and rationale must be recorded.

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

The default second independent model is Claude. If Claude is unavailable, the Owner designates another qualified independent model or reviewer and records the reason and replacement identity. A replacement reviewer cannot be the work-product author or any substantive initiator. If the Owner is a substantive initiator, the Owner also cannot serve as the replacement reviewer. The work-product author cannot approve the replacement reviewer.

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

Only the Owner may grant a permitted one-time exception outside the non-waivable categories. Work-product authors and substantive initiators cannot self-grant an exception. The exception record requires author-external independence review; if the exception changes this policy, it requires Tier 2 review. Non-waivable categories remain non-waivable, and no exception may replace required real-time independent review for production authority, security, destructive operations, or real-data activation.

Each permitted exception records:

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

## Review Evidence and Factual-Gate Procedures

Status: Accepted under `OD-REVIEW-EVIDENCE-002` (Revised Candidate v3).

These procedures define the minimum stale-state search for factual reconciliation, exact-head current-head validation, and independent-review evidence submission, attribution, fallback, retention, and invalidation. They preserve every control in `OD-REVIEW-POLICY-001` and do not weaken anti-self-certification.

### Stale-state search

Any PR classified as Tier 1 factual reconciliation must run and record a stale-state search over the complete base-to-head artifact. The search must:

- cover superseded states and known synonymous wording;
- cover relevant old SHAs, PR states, test counts, milestone states, and deferred-versus-active descriptions;
- inspect current status, roadmap, decisions, architecture, and relevant contract indexes for contradictions; and
- prove for every replaced current-state claim that current documents retain only the new state, any retained old state is explicitly historical, and no unexplained contradiction remains.

The work-product author or another executor may run the search. The classification record identifies the executor, search scope, principal terms, identifiers and synonyms, every hit, the disposition of every hit, and any unresolved hits with rationale. An author-external independent reviewer must confirm the final conclusion. The work-product author cannot self-confirm this gate. Recording only `search passed` is insufficient. No single fixed command is mandatory because the search terms depend on the reconciliation.

### Current-head validation

Current-head validation is bound to the exact base SHA and exact head SHA and includes at minimum:

- repository and PR identity;
- exact base and head identity;
- commit count, order, and parent chain;
- the complete changed-path list;
- renewed tier, trigger, and classification determination;
- required tests and checks bound to the exact head;
- whitespace and diff integrity;
- resolvable repository references;
- protected, inactive, and deferred boundaries;
- review evidence applicable to the same exact head;
- absence of requested changes, a blocking review, blocking comment, or blocking thread;
- mergeability; and
- where applicable, local working-tree, index, and remote-tracking consistency.

For a local executor, the remote-tracking ref must equal the live PR exact head, and the working tree and index must be clean unless an approved workflow explicitly permits otherwise. A remote-only reviewer may use live PR base/head, commits, diff, and checks instead of local working-tree inspection, but must state that local-environment validation was not performed.

Any new commit invalidates previous validation and merge eligibility. Validation must be rerun completely for the new head. Recording only `validation passed` is insufficient.

### Review-evidence submission modes

Each independent perspective requires a separate, identity-bound, exact-head-bound live PR record using one of these modes.

#### Reviewer-attributed native submission

The reviewer uses a platform identity attributable to that reviewer and directly submits a GitHub review or PR comment. `APPROVE`, `REQUEST_CHANGES`, and `COMMENT` are all acceptable; the policy does not require formal platform approval support.

#### Reviewer-controlled shared-credential submission

The reviewer personally submits from the reviewer's own session while the platform displays the Owner, a shared service account, an application, or another shared credential. The record discloses:

- platform credential identity;
- actual reviewer identity;
- that the reviewer personally submitted from the reviewer's own session;
- reviewer independence;
- that the shared credential does not mean the Owner authored, approved, or changed the conclusion;
- exact base and exact head;
- reviewed scope;
- findings; and
- verdict.

Tier 2 perspectives may use the same shared credential only through separate records that clearly identify each actual reviewer. A stable, non-sensitive, sustainably referenceable producing-session identifier should be included when available. Otherwise the record states `producing-session provenance unavailable`. Credentials, access tokens, private session content, and non-public internal identifiers must never be recorded.

#### Owner-authorized mechanical full-text transcription

If the reviewer cannot personally submit, an authorized transcriber may mechanically place the external review artifact into the PR only under the full-text transcription controls below.

### Capability declaration

Before review, the reviewer states whether GitHub write capability exists, the credential identity displayed by the platform, whether reviewer-attributed native submission is possible, whether only shared-credential submission is available, and whether the reviewer cannot personally submit. A reviewer without write capability may still review but must deliver a complete identity-bound, exact-head-bound artifact.

The merge gate must not mislabel shared-credential submission as reviewer-attributed native submission or transcription as reviewer-personal submission.

### Owner-authorized mechanical full-text transcription

Mechanical full-text transcription is permitted only when the reviewer cannot personally submit and requires:

- explicit Owner authorization;
- a separate PR comment for each perspective;
- disclosure of actual reviewer, reviewer independence, external delivery, transcriber, Owner authorization, and non-native provenance;
- complete reproduction of the review rather than a verdict summary;
- ordered comments or a sustainably accessible complete artifact if one comment cannot hold it;
- integrity evidence;
- a transcriber fidelity statement;
- no change or reclassification of verdict, severity, scope, or reviewer conclusion;
- PR-body links to the evidence record; and
- base/head revalidation after transcription.

The transcriber performs no repository content changes. Transcription adds only evidence comments and PR-body links. The work-product author may perform mechanical transcription but cannot identify as reviewer, change review content, approve the fallback, or describe transcription as native reviewer submission.

The preferred integrity record is SHA-256 of the byte-exact artifact delivered by the reviewer. The preserved or attached artifact records media type and, for text, encoding and observed line-ending convention. If stable original bytes are unavailable, the transcriber creates and preserves a canonical textual copy using UTF-8 without BOM, LF line endings, and exactly one trailing LF; discloses that canonicalization; and records the SHA-256 of the canonical bytes. A hash without the corresponding preserved artifact or canonical copy is insufficient. A hash does not replace full text, an accessible artifact, Owner authorization, or the fidelity statement.

### Evidence-insufficiency stop rules

Ready or merge stops when any of these conditions applies:

- a required review or merge gate is actually incomplete;
- the live PR record contradicts actual gate state, including a stale statement that a completed review is pending or that an incomplete gate is complete;
- exact base or exact head is absent;
- reviewer identity or reviewer independence is absent;
- submission mode or credential provenance is unclear;
- Tier 2 records cover different heads;
- verdict, scope, or severity is unclear;
- transcription lacks full text, an accessible artifact, or fidelity evidence;
- the external artifact conflicts with the live PR record;
- a new commit exists while old review is still relied upon; or
- required evidence was deleted or is inaccessible.

Owner approval cannot replace missing independent review or missing review evidence.

### New-head evidence rule

Any new commit preserves old records as history but marks them superseded or invalid for merge. It requires review of the complete base-to-new-head artifact rather than only the correction commit, complete current-head validation, and new records from both Tier 2 perspectives. No earlier `GREEN`, `APPROVE`, or Owner merge approval is inherited.

### Audit and retention

After merge, retain native reviews and comments, shared-credential disclosures, transcription comments, full review artifacts, artifact hashes, the exact-head classification record, Owner approval, CI and check identity, merge-parent proof, and landed-scope proof.

Do not delete or rewrite old evidence to manufacture a clean record. If comment editing is possible, substantive correction requires an explicit correction note. Never silently change an original verdict or severity.

### Scope and prospective effect

PR #23 merged through `fb09d2ea547615a70299986608dba9f459c1e544` at GitHub `merged_at` `2026-07-17T01:40:28Z`. `OD-REVIEW-EVIDENCE-002` does not retroactively invalidate PR #23 or any earlier merged PR. It becomes repository-effective only when its publication PR merges and then applies to every then-unmerged and future Tier 1 and Tier 2 PR.

This decision does not alter production authority or security boundaries; authorize destructive operations or real-data activation; or start Phase 1B or Phase 2. It does not authorize trust-anchor delivery, schema activation, projection or downstream activation, BR-006, D3, manifest activation, deployment activation, or Greptile qualification.

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
Stale-state search executor:
Stale-state search scope:
Search terms, identifiers, and synonyms:
Search hits:
Disposition of every hit:
Unresolved hits and rationale:
Author-external stale-state confirmation:
Current-head validation checklist:
Review-evidence submission mode:
Platform credential identity:
Actual reviewer identity:
Transcription provenance, if applicable:
Artifact hash, if applicable:
Exact reviewed base:
Exact reviewed head:
Superseded records, if applicable:
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
