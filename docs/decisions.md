# Architecture Decision Records

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
