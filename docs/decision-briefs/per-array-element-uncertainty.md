# Per-array-element Uncertainty Semantics

## Status

```text
DECISION PENDING — Requires Human Approval
```

This brief is a pending decision brief only. It is not an accepted ADR and does not approve implementation.

## Question

Should `uncertain_fields` support exact nested array-element paths such as `dates[1].date_text`, or remain limited to top-level field names only?

## Current Contract

`uncertain_fields` is currently an array of strings.

`schemas/activity.schema.json` currently defines `uncertain_fields.items` as `type: string`.

This means Option B does not require a structural JSON Schema change, because indexed paths such as `dates[1].date_text` are still strings.

Existing active rules use top-level uncertainty marking.

BR-002 is the most relevant precedent:

- BR-002 validates individual `fee[]` items independently.
- BR-002 still uses top-level `"fee"` in `uncertain_fields`.
- This means BR-006 would introduce finer-grained uncertainty marking than BR-002.

## Why This Matters

BR-006 checks per-session completeness inside `dates[]`.

Top-level `"dates"` is too coarse to distinguish:

- the whole `dates` field is uncertain
- one specific session date is uncertain
- one specific session date is missing and should fail

Indexed path syntax is not new to the repository because `docs/output-contracts.md` Finding Contract v1 already uses detailed finding paths such as `fee[0].amount`.

The proposal extends existing path vocabulary from finding output to uncertainty marking.

## Options

### Option A — Keep uncertain_fields top-level only

Example:

```json
{
  "uncertain_fields": ["dates"]
}
```

Benefits:

- simplest convention
- matches BR-002 current top-level pattern
- avoids finer-grained uncertainty semantics

Costs:

- cannot support BR-006 precisely
- hides which `dates[]` entry is incomplete
- weakens QA and Human Review traceability

### Option B — Allow narrowed deterministic indexed paths

Example:

```json
{
  "uncertain_fields": ["dates[1].date_text"]
}
```

Approved path shape:

```text
<field>[<zero-based-index>].<subfield>
```

Initial approved examples:

```text
dates[0].date_text
dates[1].date_text
```

Explicitly not approved:

```text
dates[*].date_text
dates[].date_text
dates[1:3].date_text
$.dates[1].date_text
dates[?].date_text
regex paths
fuzzy paths
semantic paths
```

Benefits:

- directly supports BR-006
- preserves exact per-session uncertainty
- reuses existing finding-path vocabulary
- avoids new uncertainty object structure
- deterministic

Costs:

- introduces finer-grained convention than BR-002
- requires documentation so extractor, validators, QA, and downstream consumers interpret it consistently
- future rules must explicitly state top-level vs indexed uncertainty behavior

### Option C — Introduce separate structured uncertainty object

Example:

```json
{
  "uncertainties": [
    {
      "path": "dates[1].date_text",
      "reason": "source unclear"
    }
  ]
}
```

Benefits:

- most expressive
- can support reasons, evidence, confidence, and review status later

Costs:

- larger output-shape change
- likely requires schema and contract changes
- premature for current need
- higher extractor and downstream implementation cost

## Recommendation

Recommend Option B narrowly.

`uncertain_fields` may support exact deterministic indexed paths only for rules that explicitly require per-element uncertainty marking, starting with BR-006.

Approval is prospective.

This does not retroactively require BR-002 or other existing rules to migrate.

BR-002's top-level `"fee"` convention remains valid within its rule scope.

Future rules must explicitly declare whether they use:

- top-level uncertainty markers only
- indexed uncertainty markers
- both, with precedence rules

## Contract Impact

This affects documentation semantics, not current JSON Schema structure.

No `schemas/activity.schema.json` structural change is required.

Affected documents after approval:

- `docs/output-contracts.md`
- `docs/rule-authoring-guide.md`
- `rules/BR-006-per-session-date-completeness.md` if wording needs alignment
- future extractor / validator guidance

Not affected:

- runtime pipeline
- source authority
- activity classification
- existing BR-001 to BR-005 behavior
- BR-002's existing top-level `"fee"` convention

## Implementation Gate

BR-006 remains held until this decision is approved and reflected in relevant contract documentation.

Approval of this brief is necessary but not sufficient for implementation.

After approval, the correct path is:

1. Record the accepted decision in `docs/decisions.md`.
2. Update `docs/output-contracts.md` to define allowed `uncertain_fields` path semantics.
3. Update `docs/rule-authoring-guide.md` to require rules to declare top-level vs indexed uncertainty behavior.
4. Re-check BR-006 spec determinism.
5. Implement BR-006 validator.
6. Add focused tests.
7. Run regression.
