# Business Rule Library

This folder defines monthly-agent business rules that go beyond JSON schema validation.

The rules are intended for future use by:

- Validators
- QA agents
- Human review workflows
- Regression tests for prompts, schemas, and workflows

## Rule Index

- `BR-001-required-fields.md` - key participant-facing fields must be present or flagged as uncertain.
- `BR-002-fee-uncertainty.md` - unclear fees must be listed in `uncertain_fields`.
- `BR-003-registration-period.md` - missing or unclear registration periods must be flagged.
- `BR-004-qa-status.md` - QA status must reflect the current workflow stage.
- `BR-005-source-reference.md` - extracted records must include traceable source references.

## Draft / Held Rules

- `BR-006-per-session-date-completeness.md` - per-session date completeness.
  - Status: Specification alignment pending / semantics resolved by ADR-006
  - Implementation: Pending validator implementation, tests, and active rule registration

## Usage

Use these rules after schema validation. A record can be valid JSON and still fail business rule validation if it is incomplete, misleading, or not ready for QA or newsletter use.

Business rule findings should preserve source meaning. Do not fix a failed rule by inventing missing activity details.
