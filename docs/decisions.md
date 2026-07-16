# Architecture Decision Records

## OAR owner decisions

- `OD-OAR-ARCH-001`: approved with scope rulings.
- `OD-OAR-DESIGN-001`: approved.
- `OD-OAR-CONTRACT-001`: approved.
- `OD-OAR-CONTRACT-AUTHOR-001`: inactive contract drafting only.

Resolved rulings cover structural reason identifiers, predecessor evidence, omission of audit/source references, trust-anchor transition for publication revocation, and downstream provenance deferral.

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
