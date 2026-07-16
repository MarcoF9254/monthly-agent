# Architecture

## Owner authority resolution

The Bounded Calendar Authority Chain v0 is architecture-frozen. OAR uses a generic authority envelope over separately hashed purpose-specific subjects. Ordinary authority derives from membership in one externally anchored closed-world snapshot. Registry publication is a non-self-authorizing bootstrap exception whose production trust ultimately reduces to an owner-controlled trust-anchor delivery channel. Revocation precedes authority supersession; business-subject supersession is independent.

PR #18 accepted the contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures. PR #19 accepted a fictional year-2099 offline verifier that executes the frozen chain with a caller-supplied fictional trust anchor. That fixture input is not operational trust-anchor delivery. The prototype is executable evidence, not production authority resolution or schema activation.

PR #21 completed Phase 1A deterministic core hardening for that fictional verifier. Verification state and the internal test trace are invocation-local; public `verify()` results and CLI output remain trace-free, and ordinary lifecycle order remains fixed and non-configurable. Multiple effective run-metadata, monthly-selection, or eligibility subjects for one complete business key fail closed. Admission and snapshot, authority, and business-subject lifecycle traversal are deterministically resource-bounded, with semantic and resource rejection distinguished.

The fixed ceilings are 64 inventory artifacts, 256 KiB per admitted JSON file, 2 MiB total admitted JSON, 256 snapshot entries, and lifecycle/supersession depth 64. The depth ceiling is defensive and independently enforced; it does not prove that an accepted 64-link scenario exists. These checks do not solve TOCTOU or provide secure filesystem admission. Phase 1A remains fictional-only and adds no production trust-anchor delivery, authority operation, schema activation, or new architecture layer.

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

For the calendar-only vertical slice, `OD-CAL-ARCH-001` approves per-activity canonical projections plus a monthly manifest. `OD-CAL-ARCH-002` adds a separately authorized monthly selection decision. `OD-CAL-ARCH-003` clarifies contracts only: authority purposes are typed and non-transferable, and external authority binds the digest of the exact canonical authorization subject. Eligibility grants exact-field permission, selection records publication intent, projections carry validated per-activity payloads, and the manifest binds the complete effective selection artifact to valid projections. Calendar projection and monthly-manifest schemas remain inactive Draft 0.x artifacts. No production calendar consumer resolver, projection builder, renderer, manifest validator, migration, or activation exists, and no real authority, eligibility, or monthly selection exists. The PR #19 fictional OAR verifier does exist; it neither activates the calendar-only projection or manifest schemas nor constitutes production authority resolution.

Historically, Gate 2 bounded authority input followed `OD-BAI-ARCH-001`, accepted with owner changes: production authority resolution requires one externally supplied trust anchor plus one self-contained verified resolution bundle. The anchor identifies the authorized immutable registry-snapshot tip and expected complete artifact digest. Internal hashes prove integrity but not current authorization; rollback detection depends on the external anchor. The later fictional verifier implements this chain only for approved year-2099 fixtures. No executable schema activation, real authority issuance, real publication, migration, downstream activation, or operational trust-anchor delivery is accepted or implemented.

`registry_id` is the logical registry identity. `snapshot_id` is one immutable published version identity. The existing external authority registry is not the Gate 2 authorized closed-world registry publication snapshot, and Gate 2 does not activate or replace the existing calendar-only draft.

## Data Flow

- Raw inputs belong under `data/input/`.
- Generated extraction and validation outputs belong under `data/output/`.
- Future authority registry and artifacts belong under `data/authority/`; consumer eligibility belongs under `data/consumer-eligibility/`; calendar selection belongs under `data/calendar-selections/`; generated projections, provenance, and manifests belong under `data/projections/`. All remain outside `data/runs/`.
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
