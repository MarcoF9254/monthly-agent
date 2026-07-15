# Architecture

## Purpose

`monthly-agent` turns elderly centre monthly programme source documents into structured activity records that can be validated, reviewed, and reused for monthly newsletter generation.

The architecture is intentionally small and auditable. Each layer has a narrow responsibility so future agents can change prompts, schemas, validators, or review workflows without mixing concerns.

## Workflow

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

## Layers

### Source and Extraction

Source programme documents are the authority for activity names, dates, times, fees, venues, quotas, eligibility, and registration details.

The Extract Agent uses `prompts/extract-activity-info.md` to create records that conform to `schemas/activity.schema.json`. Missing or unclear source information should remain explicit through `uncertain_fields` rather than being guessed.

### Schema Contract

`schemas/activity.schema.json` defines the record shape. Schema validation answers whether the JSON is structurally valid; it does not decide whether participant-facing details are correct.

### Business Rule Engine

Business rules in `rules/` define deterministic checks that operate on extracted records. Implementations live under `validators/business_rules/` and are registered in `validators/business_rules/__init__.py`.

Business rules should remain per-record unless a rule specification explicitly defines batch-level scope. They must not inspect original source documents unless a future rule explicitly introduces that capability.

### QA and Human Review

QA and Human Review compare extracted records with source evidence. This is where ambiguous source layout, conflicting details, unsupported inferences, and judgement-based review belong.

### Newsletter Generation

Newsletter generation should use approved records only. Record approval is necessary under the current newsletter policy, but `qa_status` does not itself grant newsletter or any other consumer permission. Uncertain or unresolved details should not be published as confirmed participant-facing information.

### Scoped Downstream Eligibility

Downstream use separates closed evidence, explicit owner authority, consumer policy, and a deterministic field-allowlisted projection with separately bound provenance. Eligibility decisions are immutable and append-only; supersession creates a new artifact. Projections are reproducible artifacts with explicit identity and provenance. Both live outside immutable `data/runs/` trees, reference evidence by `run_id` and `activity_id`, fail closed when authority or binding is missing or invalid, and never transfer between consumers.

Stage 1 establishes accepted architecture only. It does not activate a consumer, implement a builder or validator, or change the activity schema.

## Data Flow

- Raw inputs belong under `data/input/`.
- Generated extraction and validation outputs belong under `data/output/`.
- Future consumer eligibility authority belongs under `data/consumer-eligibility/`; future generated projections and provenance belong under `data/projections/`.
- Representative examples belong under `examples/`.
- Contracts and project handoff docs belong under `docs/`.

## Validation Boundaries

- Schema validation checks JSON structure.
- Business validation checks deterministic rules defined in `rules/`.
- QA checks source support and meaning.
- Human Review resolves unclear, conflicting, or source-dependent decisions.

Do not move source-meaning judgement into deterministic validators. Validators should report objective findings and leave interpretation-heavy decisions to QA or Human Review.

## Finding Contract

Validator findings should follow the shared finding fields documented in `docs/output-contracts.md`. The current finding contract is `Finding Contract v1`.

## Change Principles

- Keep changes small and scoped.
- Preserve source meaning.
- Prefer deterministic validation over inferred meaning.
- Keep rule specifications and implementations aligned.
- Add focused tests for validator behavior changes.
