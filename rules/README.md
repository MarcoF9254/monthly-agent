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
- `BR-006-per-session-date-completeness.md` - implemented, activation held; the validator exists but is not registered or runtime active. Future activation requires real vertical-slice evidence, indexed marker syntax validation in place before or together with activation, and explicit owner approval.
- [`docs/d3-indexed-marker-syntax-contract.md`](../docs/d3-indexed-marker-syntax-contract.md) - the merged, repository-effective PR #32 pilot artifact defines indexed marker syntax only; the validator (`validators/d3_indexed_marker_validator.py`) exists as a standalone fictional/test-only module and is not registered or runtime active.

## Usage

Use these rules after schema validation. A record can be valid JSON and still fail business rule validation if it is incomplete, misleading, or not ready for QA or newsletter use.

Business rule findings should preserve source meaning. Do not fix a failed rule by inventing missing activity details.
