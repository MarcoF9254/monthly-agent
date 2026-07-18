# D3 — Indexed Marker Syntax Validation Contract

## Purpose

This contract defines the validation rules for indexed marker syntax used in `uncertain_fields` entries.

Indexed markers extend the available `uncertain_fields` syntax so that per-element uncertainty can be expressed for individual entries without generalizing to the entire field.

This contract answers syntax only. A marker that matches the approved shape is syntactically valid, but that result grants no rule-specific, schema-level, runtime, or activation authority for its field or subfield. Rule-specific indexed-marker authorization remains a separate, fail-closed semantic gate. This contract does not activate any business rule or change runtime validator behavior.

Bare top-level markers are outside D3 adjudication authority. D3 does not maintain, derive, or consult a vocabulary or registry of valid top-level field names, and an empty D3 finding result for a bare marker conveys no field-name, schema, rule, runtime, or activation authority.

## Relationship to ADR-006

ADR-006 approves a narrow deterministic indexed path shape. This contract defines only the validation logic that checks whether an attempted indexed `uncertain_fields` entry conforms to that shape. It does not determine whether a business rule may use the syntactically valid marker.

## Approved Path Shape

An indexed marker must match this pattern:

```text
<field>[<zero-based-index>].<subfield>
```

Where:

- `<field>` is an identifier-shaped field name (e.g. `dates`, `fee`). D3 does not determine whether the named field is schema-valid or indexable.
- `<zero-based-index>` is a non-negative integer (e.g. `0`, `1`, `17`).
- `<subfield>` is an identifier-shaped subfield name (e.g. `date_text`, `amount_text`). D3 does not determine whether the named subfield exists in any schema.

### Examples

Valid indexed markers:

- `dates[0].date_text`
- `dates[1].date_text`
- `fee[0].amount_text`
- `date_text[0].value` (syntactically valid only; not thereby authorized for BR-006 or runtime use)

### Explicitly Invalid Indexed Forms

The following attempted indexed markers must be rejected:

- Wildcards: `dates[*].date_text`
- Empty index: `dates[].date_text`
- Ranges: `dates[0:2].date_text`
- JSONPath syntax: `$..dates[*].date_text`
- Unknown-index placeholders: `dates[?].date_text`
- Regex paths: `dates/\\d+/.date_text`
- Fuzzy paths: `dates[approx].date_text`
- Semantic paths: `dates[first].date_text`
- Bare indexed fields without subfield: `dates[0]`
- Leading dots or slashes: `.dates[0].date_text`, `/dates[0].date_text`
- Trailing dots or slashes: `dates[0].date_text.`

## Validation Scope

### In Scope

- Syntax validation of `uncertain_fields` string entries that attempt the approved ADR-006 indexed shape.
- Acceptance of any identifier-shaped field and subfield that match the approved shape, including `date_text[0].value`, without conferring semantic authorization.
- Rejection of wildcard, range, JSONPath, regex, fuzzy, semantic, and other unapproved indexed forms.
- Rejection of indexes that are not zero-based non-negative integers.
- Rejection of missing subfield after an attempted indexed path.
- Fictional/test-only validation logic.

### Out of Scope

- Recognition, validation, or authorization of bare top-level field names.
- Any hardcoded, schema-derived, or semantic registry of allowed top-level field names.
- BR-006 activation.
- Real-data processing or validation.
- Runtime or production activation.
- Schema changes to `schemas/activity.schema.json`.
- Projection, manifest, or downstream activation.
- Trust-anchor delivery.
- Phase 2 secure filesystem admission.
- Any business rule registration or activation.
- Rule-specific authorization of any indexed field or subfield.
- Schema-level determination that the named field is an array or that the named subfield exists.

## Syntax and Semantic Authorization Boundary

`date_text[0].value` matches `<field>[<zero-based-index>].<subfield>` and is therefore syntactically valid under D3. D3 does not thereby authorize that marker for BR-006 or any runtime use.

Any consumer that requires a restricted set of indexed markers must apply its own rule-specific authorization after D3 syntax validation. That semantic gate must fail closed when authorization is absent. No such authorization registry or runtime gate is introduced by this contract or pilot.

Bare markers such as `fee`, `venue`, `eligibility`, or any other identifier without indexed syntax are not judged valid or invalid by D3. They pass through D3 without field-name recognition and remain subject to whatever separate canonical schema or rule validation already governs them outside D3.

## Output

When validation is invoked against a list of `uncertain_fields` entries, the validator returns findings under Finding Contract v1 only for attempted indexed markers that violate the approved indexed syntax.

### Finding Contract v1 Fields

Each finding uses these fields:

- `index`: always `0` for standalone uncertain_fields validation.
- `activity_id`: always `"<unknown>"` for standalone validation.
- `rule_id`: `"D3"`.
- `field`: `"uncertain_fields"`.
- `path`: the original invalid marker string.
- `severity`: `"medium"`.
- `message`: description of the syntax violation.
- `recommendation`: `"Use the approved ADR-006 indexed path shape: <field>[<zero-based-index>].<subfield>."`

### Pass

A syntactically valid attempted indexed marker produces no D3 finding. Bare top-level markers also produce no D3 finding because they are outside D3 adjudication authority, not because D3 recognizes or authorizes them. An empty D3 finding list is not evidence of field-name, rule-specific, schema-level, runtime, or activation authorization.

### Fail

When one or more attempted indexed `uncertain_fields` entries contain syntax not approved by ADR-006, the validator returns one finding per invalid attempted indexed entry.

## Implementation Status

Draft contract only. Implementation is limited to fictional/test inputs. The validator module exists outside the active business-rule registry and is not runtime active.

## Governance

This contract does not alter production authority or security boundaries. It does not authorize BR-006 activation, real-data processing, schema changes, destructive operations, or downstream activation.
