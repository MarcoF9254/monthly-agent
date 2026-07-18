# D3 — Indexed Marker Syntax Validation Contract

## Purpose

This contract defines the validation rules for indexed marker syntax used in `uncertain_fields` entries.

Indexed markers extend the existing `uncertain_fields` vocabulary so that per-element uncertainty can be expressed for individual array entries without generalizing to the entire field.

This contract does not activate any business rule or change runtime validator behavior. It is a definition contract only.

## Relationship to ADR-006

ADR-006 approves a narrow deterministic indexed path shape for rules that explicitly require per-element uncertainty marking. This contract defines the validation logic that checks whether a given `uncertain_fields` entry conforms to that approved shape.

## Approved Path Shape

An indexed marker must match this pattern:

```text
<field>[<zero-based-index>].<subfield>
```

Where:

- `<field>` is the array field name (e.g. `dates`, `fee`).
- `<zero-based-index>` is a non-negative integer (e.g. `0`, `1`, `17`).
- `<subfield>` is a field within the array element (e.g. `date_text`, `amount_text`).

### Examples

Valid indexed markers:

- `dates[0].date_text`
- `dates[1].date_text`
- `fee[0].amount_text`

### Explicitly Invalid Forms

The following must be rejected:

- Wildcards: `dates[*].date_text`
- Empty index: `dates[].date_text`
- Ranges: `dates[0:2].date_text`
- JSONPath syntax: `$..dates[*].date_text`
- Unknown-index placeholders: `dates[?].date_text`
- Regex paths: `dates/\\d+/.date_text`
- Fuzzy paths: `dates[approx].date_text`
- Semantic paths: `dates[first].date_text`
- Bare indexed fields without subfield: `dates[0]`
- Indexed paths on non-indexable fields: `date_text[0].value`
- Leading dots or slashes: `.dates[0].date_text`, `/dates[0].date_text`
- Trailing dots or slashes: `dates[0].date_text.`

## Validation Scope

### In Scope

- Syntax validation of `uncertain_fields` string entries against the approved ADR-006 shape.
- Rejection of wildcard, range, JSONPath, regex, fuzzy, semantic, and other unapproved forms.
- Rejection of indexes that are not zero-based non-negative integers.
- Rejection of missing subfield after indexed array path.
- Preservation of valid top-level field markers (e.g. `fee`, `dates`).
- Fictional/test-only validation logic.

### Out of Scope

- BR-006 activation.
- Real-data processing or validation.
- Runtime or production activation.
- Schema changes to `schemas/activity.schema.json`.
- Projection, manifest, or downstream activation.
- Trust-anchor delivery.
- Phase 2 secure filesystem admission.
- Any business rule registration or activation.

## Output

When validation is invoked against a list of `uncertain_fields` entries, the validator returns findings under Finding Contract v1.

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

When every `uncertain_fields` entry conforms to the approved syntax (either a recognized top-level field name or a valid indexed marker), the validator returns no findings.

### Fail

When one or more `uncertain_fields` entries contain syntax not approved by ADR-006, the validator returns one finding per invalid entry.

## Implementation Status

Draft contract only. Implementation is limited to fictional/test inputs. The validator module exists outside the active business-rule registry and is not runtime active.

## Governance

This contract does not alter production authority or security boundaries. It does not authorize BR-006 activation, real-data processing, schema changes, destructive operations, or downstream activation.
