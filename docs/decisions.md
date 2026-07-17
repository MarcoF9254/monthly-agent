# Architecture Decision Records

## OD-REVIEW-POLICY-001: Risk-Based Independent Review Policy

Status: Accepted

Ratified by: Marco

### Decision

Adopt Option C, the Risk-Based Independent Review Policy:

- every PR requires author-external independent review;
- high-risk changes require dual independent review;
- an author-external independent reviewer decides and records classification;
- reviewer identity considers work-product authorship and substantive initiation, not Git metadata alone;
- review and CI bind to the exact head, and any new commit requires re-review of that new head;
- gated PRs require true merge commits;
- Tier 2 review for production authority, security, destructive operations, or real-data activation is non-waivable;
- absence of a qualified replacement reviewer stops the PR; and
- break-glass handling is neither authorized nor defined by this decision.

### Review evidence

- First architecture draft: ChatGPT.
- First independent policy review: Claude — YELLOW, identifying two required corrections concerning Owner-reviewer independence and merge-method head-pinning.
- Those required corrections were incorporated, together with non-blocking recommendations concerning the default second reviewer, Tier 1 audits, and exact-source evidence.
- Second independent policy review: Claude — GREEN WITH NON-BLOCKING NOTES.
- Blocking findings: zero.
- Major findings at the pre-publication policy-review stage: zero.
- The Owner selected the strict non-waivable high-risk Tier 2 rule.

### Consequences

The policy is prospective and does not retroactively invalidate PR #22 or earlier PRs. Its repository-publication PR is Tier 2, and future policy amendments are Tier 2. CI, review, Owner approval, and merge verification remain separate controls.

## OD-REVIEW-EVIDENCE-002: Review Evidence and Factual-Gate Procedures

Status: Repository-effective through merged PR #24.

Version: Revised Candidate v3

Ratified by: Marco

Independent focused confirmations: Claude and Fable, each `RATIFICATION-READY` with zero blocking and zero major findings.

### Decision

Adopt the minimum procedures in `docs/governance.md` for:

- complete base-to-head stale-state searches and author-external confirmation;
- exact-base and exact-head current-head validation;
- identity-bound live PR review-evidence submission through reviewer-attributed native, reviewer-controlled shared-credential, or Owner-authorized mechanical full-text transcription modes;
- capability and credential-provenance disclosure;
- evidence-insufficiency stop rules;
- complete invalidation and renewed review after any new commit; and
- audit and evidence retention.

The decision preserves all controls in `OD-REVIEW-POLICY-001`, including author-external independence, dual review for Tier 2, exact-head binding, anti-self-certification, Owner approval separation, and true merge-commit proof.

### Roles for publication

- Work-product implementation author: Codex.
- Substantive initiator and governance facilitator: ChatGPT.
- Owner, final approval authority, and merge authority: Marco.
- Required independent perspectives: Fable and Claude, covering the same exact head.

ChatGPT is not a required independent-review perspective for the publication PR. Marco is a substantive initiator and cannot count as an independent perspective. Owner approval cannot replace Fable or Claude review.

### Effect and boundaries

Repository effectiveness began when PR #24 merged at GitHub `merged_at` `2026-07-17T05:47:09Z` through true merge commit `cd30a42bde387b66df0f99e117d7c2fd57b16b88`. Its first parent is `fb09d2ea547615a70299986608dba9f459c1e544`, and exact reviewed head `9443dd0fc1624b3853cfc7ffbb3a941b4498bf11` is its second parent. The decision is prospective and does not retroactively invalidate PR #23 or any earlier merged PR. It applies to every PR that was unmerged when PR #24 merged and to every future Tier 1 and Tier 2 PR.

This decision grants no production authority, security activation, destructive-operation authority, real-data activation, Phase 1B activation, Phase 2 activation, trust-anchor delivery, schema activation, projection or downstream activation, BR-006 activation, D3 resolution, manifest activation, deployment activation, or Greptile qualification.

## OAR owner decisions

`OD-OAR-PHASE-1B1-001` approves the narrow Option B implementation of OAR Phase 1B.1 Dependency and Package Foundation. The authorized scope is project metadata, one authoritative cross-platform dependency lock, runtime/test dependency separation, explicit Python 3.11 and 3.12 support, reproducible fresh-environment installation, CI installation from the lock, development package build/install validation, and strictly necessary documentation and validation tooling. The exact implementation allowlist is `.gitignore`, `.github/workflows/tests.yml`, `README.md`, `docs/current-status.md`, `docs/decisions.md`, `docs/roadmap.md`, `pyproject.toml`, `requirements.txt`, `tools/check_package_install.py`, and `uv.lock`.

The decision does not authorize Phase 1B.2 interface stabilization, `VerificationResult` redesign or public-contract stabilization, CLI semantic changes, resource relocation, Phase 2 secure filesystem admission, production authority, trust-anchor delivery, schema or real-data activation, projection, manifest, downstream or deployment activation, BR-006, D3, GOV-DEBT-001, or GOV-DEBT-002. A built distribution validates metadata and inclusion of existing Python sources only; it is not a production deployment artifact and does not establish an installed CLI, stable public API, or resource-independent runtime contract. Implementation must stop rather than expand scope if truthful validation requires any excluded change.

- `OD-OAR-ARCH-001`: approved with scope rulings.
- `OD-OAR-DESIGN-001`: approved.
- `OD-OAR-CONTRACT-001`: approved.
- `OD-OAR-CONTRACT-AUTHOR-001`: inactive contract drafting only.

Resolved rulings cover structural reason identifiers, predecessor evidence, omission of audit/source references, trust-anchor transition for publication revocation, and downstream provenance deferral.

`OD-OAR-CONTRACT-ACCEPT-001` accepted and merged PR #18: the OAR contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures. `OD-OAR-PROTOTYPE-ACCEPT-001` accepted and merged PR #19: the fictional year-2099 offline verifier prototype and its independently reviewed positive, negative, canonicalization, lifecycle, and fail-closed tests. The Bounded Calendar Authority Chain v0 architecture is frozen.

`OD-OAR-PROTOTYPE-N15-001` classifies OAR-N15 as a construction-invariant test of one shared immutable revocation-first stage order. It is not runtime input or verifier configuration. Prototype acceptance supplies executable fictional evidence only; it grants no production authority, schema activation, real trust-anchor delivery, real registry publication, real authority or revocation issuance, R03 decision, downstream activation, or authority for a future milestone.

The Architecture Owner accepted and merged PR #21 as fictional-only Phase 1A deterministic verifier core hardening. Accepted decisions are: trace remains internal/test-only and invocation-local; ordinary lifecycle order is fixed; resource exhaustion is a distinct `resource_rejection`; multiple effective candidates for the complete run-metadata, monthly-selection, or eligibility business key fail closed; and CI covers Ubuntu and Windows on Python 3.11 and 3.12. Programming defects are not ordinary verification rejections, and rule, component, and stage identifiers are not yet a stable public compatibility contract.

Phase 1A acceptance does not activate schemas or production authority. Dependency locking, package metadata, installation reproducibility, safer or versioned result interfaces, and related interface work are deferred to an inactive, separately authorized Phase 1B. TOCTOU remediation and secure filesystem admission are deferred to an inactive, separately authorized Phase 2. No ordering between those deferred milestones or next implementation milestone is accepted.

Independent review of PR #21 concluded `APPROVE WITH NON-BLOCKING NOTES`, with zero blocking and zero major findings. P1A-F01 was genuinely resolved. P21-F01 accepts the positional placement of `VerificationResult.classification` only for the current pre-stable interface; P21-F02 accepts depth 64 as a defensive secondary ceiling whose enforcement is tested without claiming an accepted 64-link scenario. Neither note reopens architecture or requires a PR #21 correction.

This file records lightweight architecture decisions for `monthly-agent`. It preserves project decisions that affect future implementation, validation, and agent handoff work.

## ADR-001: Activity ID Format

Status: Accepted

### Context

Activity records need stable identifiers for validation output, QA review, and downstream newsletter workflows. Human-facing programme documents may use circled numbers or visual labels, but those are not reliable system identifiers.

### Decision

Use plain string IDs such as `2026-04-001` or `sample-2026-04-001`.

Do not use circled numbers as system identifiers.

### Consequences

Plain string IDs are easier to compare, serialize, validate, and reference in findings. Circled numbers may still be used for display if needed, but not as primary keys.

## ADR-002: Validation Exit Codes

Status: Accepted

### Context

Automation needs to distinguish records that fail validation from tools that fail to run.

### Decision

Use these validator exit codes:

- `0` = PASS
- `1` = validation failure
- `2` = tool execution error

### Consequences

Future runners can reliably separate record validation failures from invalid input, unreadable files, malformed JSON, missing schemas, or runtime errors.

## ADR-003: Severity Defaults

Status: Accepted

### Context

Schema validation and business validation represent different types of problems and should not default to the same severity model.

### Decision

- Schema validation findings use severity `critical`.
- Business validation findings use severity defined by BR rule files.

### Consequences

Structural schema errors should stop downstream processing. Business-rule severity remains tied to each rule's participant-facing risk and workflow impact.

## ADR-006: Indexed Uncertainty Paths

Status: Accepted

### Context

`uncertain_fields` currently records fields that are missing, unclear, or require human review. Existing active rules use top-level uncertainty markers, and BR-002's top-level `"fee"` convention remains valid within BR-002.

BR-006 requires per-element uncertainty marking for individual `dates[]` entries, but implementation was held until the uncertainty path semantics were approved.

### Decision

`uncertain_fields` may contain exact deterministic indexed paths only for rules that explicitly require per-element uncertainty marking.

Approved path shape:

```text
<field>[<zero-based-index>].<subfield>
```

Initial approved examples:

- `dates[0].date_text`
- `dates[1].date_text`

Explicitly not approved:

- wildcards
- empty index notation
- ranges
- JSONPath syntax
- unknown-index placeholders
- regex paths
- fuzzy paths
- semantic paths

This decision is prospective.

Existing active rules do not need to migrate.

BR-002's top-level `"fee"` convention remains valid within BR-002.

This decision does not approve source authority or activity classification.

This decision does not implement BR-006 by itself. BR-006 implementation still requires contract updates and implementation work.

### Consequences

Rules that use `uncertain_fields` must explicitly declare whether they accept top-level markers, indexed markers, or both with precedence rules.

Indexed uncertainty paths reuse a narrow deterministic path vocabulary already used by validation findings, but `uncertain_fields` must not be treated as full JSONPath or as a fuzzy or semantic path language.

## ADR-007: Scoped Downstream Eligibility

Status: Accepted

### Context

`qa_status` describes record review state and does not grant universal downstream permission. Different consumers may safely use different source-supported field subsets, while closed run evidence must remain immutable.

The Architecture Owner reviewed four options: eligibility in the activity schema; eligibility in an approval or authority artifact alone; projection alone; and policy plus scoped approval plus generated projection. An authority artifact alone does not define deterministic least-data delivery or projection provenance. A projection alone cannot grant or prove owner authority. Embedding eligibility in the activity schema couples mutable consumer policy to evidence.

### Decision

The Architecture Owner explicitly accepted Option D: separate closed evidence, owner authority, consumer policy, generated projection, and projection provenance.

- Eligibility decisions are immutable, append-only, consumer-scoped authority artifacts outside `data/runs/`.
- Only a verifiable accepted owner decision for an exact `run_id`, `activity_id`, and `consumer_id` can grant its exact `allowed_fields`; everything else fails closed.
- Supersession or revocation creates a new decision artifact and never overwrites history.
- Consumer projections are deterministic, field-allowlisted, reproducible artifacts outside `data/runs/`, with separately bound provenance.
- Decisions do not transfer between consumers or mutate `qa_status`, closed evidence, or approval artifacts.
- Future authority artifacts belong under `data/consumer-eligibility/<consumer_id>/`; future projections and provenance belong under `data/projections/<consumer_id>/`.

This decision accepts architecture only. It does not implement or activate either draft contract, issue an eligibility decision, generate a projection, authorize migration, change existing consumer behavior, or activate downstream use.

### Consequences

Future implementation requires an immutable decision lifecycle, verifiable owner authority, deterministic decision-chain resolution, consumer-specific validation, strict field allowlists, RFC 8785 payload canonicalization, payload hashes, stable projection identity, and provenance binding.

Missing, malformed, unverifiable, unmatched, duplicated, cyclic, cross-scope, revoked, or otherwise broken authority fails closed. Missing or mismatched projection/provenance binding also fails closed.

Existing closed runs remain unchanged. In particular, R03 remains `partially_approved`: 32 records are approved, 13 records remain `needs_review`, and no eligibility decision or downstream activation is created by this ADR.

`OD-CAL-ARCH-001` subsequently approved the calendar-only implementation architecture direction for contract drafting: per-activity canonical projections plus a monthly manifest.

`OD-CAL-ARCH-002` approved a contract revision that separates exact-field calendar eligibility from externally authorized monthly publication selection. The manifest must bind exactly the effective selection to valid eligible projections, including selection identity and canonical content hash. It also requires external evidence for registry revocation, exact calendar source-field grants, complete projection revalidation, and explicit authorized-empty selection semantics.

These owner decisions accept architecture direction only. They do not accept or activate draft executable schemas, start implementation, issue authority, eligibility, or selection decisions, generate projections or manifests, migrate a consumer, or activate downstream use.

`OD-CAL-ARCH-003` is accepted as contract clarification only. It requires typed, non-transferable purposes `calendar-eligibility`, `calendar-monthly-selection`, and `calendar-authority-revocation`; exact equality of expected, registry, and external-artifact purpose; and external binding to the digest of the exact canonical authorization subject. Selection and eligibility subjects exclude authority-reference metadata, while revocation binds the original authority identifier, digest, purpose, and exact scope. This does not accept an executable schema, verifier, implementation, or activation.

## Gate 2 Owner Decisions: Bounded Authority Input

`OD-BAI-ARCH-001` is accepted with owner changes. Production resolution must receive exactly one external trust anchor and one self-contained verified resolution bundle. The trust anchor binds the authorized `snapshot_id` and complete snapshot artifact digest for one logical `registry_id` and exact scope. A valid internal digest cannot prove that a snapshot is the currently authorized tip; stale-snapshot and rollback detection depend on the independently supplied anchor.

`OD-BAI-CONTRACT-001` approves drafting the inactive Gate 2 contracts and draft `0.x` schemas. It does not accept executable schemas, implementation, real run metadata authority, real authority or decision issuance, registry publication, downstream activation, BR-006 activation, or D3 resolution.
