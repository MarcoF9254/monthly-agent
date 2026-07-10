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

Extraction capability does not determine source authority.

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
