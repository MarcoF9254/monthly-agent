# Extraction Boundary

## Purpose

This document defines the extraction boundary for `monthly-agent`.

The extraction boundary describes what extraction may produce, what it must preserve, and what decisions it must not make.

This is a boundary document, not a runtime component.

## Governance Relationship

This document follows `docs/governance.md`.

It does not redefine governance, architecture, ADR policy, evidence hierarchy, decision hierarchy, review workflow, or approval authority.

Governance remains defined only in `docs/governance.md`.

## Architecture Relationship

This document refines the boundary around the Source and Extraction stage described in `docs/architecture.md`.

It does not change the approved runtime pipeline.

The approved pipeline remains:

The following pipeline is reproduced from `docs/architecture.md` for local readability.

```text
Monthly programme source
        |
        v
Extract Agent
        |
        v
Structured activity JSON
        |
        v
Schema Validator
        |
        v
Business Rule Validator
        |
        v
GPT QA / Human Review
        |
        v
Approved newsletter-ready records
```

## Boundary Position

Extraction sits between source programme material and structured activity records.

```text
Source programme material
        |
        v
Extraction boundary
        |
        v
Structured activity records
```

The extraction boundary governs the meaning-preserving conversion from source material into structured records.

It does not govern schema validation, business rule validation, QA review, human approval, or newsletter generation.

## In Scope

Extraction may:

- identify activity-like entries from source programme material
- copy participant-facing details into structured fields
- preserve source wording where meaning may be lost by paraphrase
- record activity names, dates, times, venues, fees, quotas, eligibility, staff-in-charge, remarks, and registration details when present
- record missing, unclear, or conflicting information as uncertainty
- preserve source evidence references where the extraction output contract requires them

Extraction may produce candidate structured records only.

## Out of Scope

Extraction must not:

- decide which source document is authoritative when multiple source documents conflict
- convert observational evidence into approved policy
- approve participant-facing information for publication
- silently repair source errors
- infer missing details from habit, prior months, layout expectation, or common sense
- resolve ambiguous source meaning without marking uncertainty
- perform schema validation
- perform business rule validation
- perform QA review
- perform human approval
- generate final newsletter content
- create or modify ADRs
- introduce runtime architecture changes

## Source Meaning Preservation

Extraction should preserve source meaning rather than normalize it into a cleaner but unsupported interpretation.

If a source field is missing, unclear, visually ambiguous, or internally conflicting, the extracted record should make that uncertainty explicit.

Uncertainty is an extraction output, not an extraction failure.

## Authority Boundary

Per governance Principle 8, extraction capability does not determine source authority.

A format that can be extracted is not automatically authoritative.

When two extractable sources disagree, extraction may surface the disagreement, but must not decide which source overrides the other.

Authority decisions require the approved governance and review process.

## Validation Boundary

Extraction produces structured candidate records.

Schema validation decides whether the record shape is structurally valid.

Business rule validation decides whether deterministic approved rules are violated.

QA and Human Review decide whether source support, meaning, and unresolved ambiguity are acceptable for downstream use.

Extraction must not absorb these downstream responsibilities.

## Classification Boundary

Extraction may identify entries that appear to be activity-like.

It must not create a final policy boundary between activity, information block, announcement, and ignored content unless that boundary is approved elsewhere.

Where classification is unclear, extraction should preserve the candidate entry and mark the uncertainty for QA or Human Review.

## Pending Boundary Decisions

The pending decision candidates in this section are not approved architecture decisions.

They are recorded here only to anchor unresolved extraction-boundary questions until human approval is given.

If approved, they should be converted into accepted ADRs in `docs/decisions.md`.

### ADR-004 Candidate: Source Authority

```text
DECISION PENDING — Requires Human Approval
```

Question

Which source should be authoritative when multiple extractable sources disagree about the same activity detail?

Options

- Treat one approved source type as authoritative over others.
- Treat the latest dated source as authoritative.
- Treat all disagreements as unresolved until QA or Human Review confirms authority.

Trade-offs

- A fixed source hierarchy can make extraction output more consistent, but it may encode policy before the project has approved source authority.
- Latest-source precedence can be simple to apply, but it may be wrong when later material is partial, promotional, or not intended to supersede the original programme source.
- Deferring disagreements preserves source meaning and avoids premature policy, but it requires QA or Human Review to resolve more records.

Recommendation

Preserve the current boundary: extraction may surface disagreements between extractable sources, but must not decide which source overrides another until source authority is approved.

### ADR-005 Candidate: Activity Classification Boundary

```text
DECISION PENDING — Requires Human Approval
```

Question

How should extraction handle candidate entries whose status as activities is unclear from the source document?

Options

- Include only entries that clearly match the approved activity definition.
- Exclude unclear entries during extraction.
- Preserve unclear candidate entries and mark classification uncertainty for QA or Human Review.

Trade-offs

- Including only clearly matching entries can keep output cleaner, but it may miss source content that should be reviewed.
- Excluding unclear entries can reduce review volume, but it risks silent omission and makes extraction less auditable.
- Preserving unclear candidate entries improves auditability and keeps unresolved policy visible, but it requires downstream review before publication.

Recommendation

Preserve the current boundary: extraction should preserve unclear candidate entries and mark classification uncertainty for QA / Human Review rather than silently ignoring or finalizing them.

## Review Triggers

Extraction output should be reviewed when:

- source documents conflict
- required participant-facing details are missing
- layout makes field ownership unclear
- one visual block appears to contain multiple activities
- one activity appears across multiple visual blocks
- dates, times, fees, quotas, or eligibility are inconsistent
- extracted content requires interpretation beyond copying source meaning

## Non-Goals

This document does not specify prompts, schemas, validators, test fixtures, storage design, export design, UI design, or implementation steps.

Those responsibilities belong to their respective project documents and approved specifications.
