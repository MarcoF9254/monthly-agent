# Decision Brief — Per-array-element Uncertainty Semantics

## Status

```text
DECISION PENDING — Requires Human Approval
```

## Question

Should `uncertain_fields` support exact nested array-element paths such as `dates[1].date_text`, or remain limited to top-level field names only?

## Current Contract

`uncertain_fields` is currently defined as an array of strings whose description refers to field names that are missing, unclear, or require human review.

Existing active rules use top-level uncertainty marking.

BR-002 is the most relevant precedent. It validates individual `fee[]` items independently, but it treats `"fee"` in `uncertain_fields` as the uncertainty marker for unclear fee items rather than using indexed paths such as `fee[1].amount_text`.

This means BR-006 would introduce finer-grained uncertainty marking than BR-002.

## Why This Matters

BR-006 checks per-session completeness inside `dates[]`.

Without exact per-entry uncertainty marking, the system cannot distinguish between:

- the whole `dates` field being uncertain
- one specific session date being uncertain
- one specific session date being missing and therefore failing BR-006

A top-level marker such as `"dates"` is too coarse for BR-006 because it can hide which individual `dates[]` entry is incomplete.

The indexed path syntax itself is not new to the repository. Finding Contract v1 already uses detailed paths such as `fee[0].amount` in validator findings. This decision would extend an existing path vocabulary from finding output into uncertainty marking.

## Options

### Option A — Keep `uncertain_fields` top-level only

Example:

```json
{
  "uncertain_fields": ["dates"]
}
```

Benefits:

- simplest convention
- matches BR-002's current top-level pattern
- avoids introducing a finer-grained uncertainty convention

Costs:

- cannot support BR-006 precisely
- makes it unclear which `dates[]` entry is incomplete
- may cause over-broad uncertainty marking
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

Not approved:

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
- reuses the repository's existing finding-path vocabulary
- avoids introducing a new uncertainty object structure
- keeps implementation deterministic

Costs:

- introduces a finer-grained uncertainty convention than BR-002
- requires documentation so extractors, validators, QA, and downstream consumers interpret it consistently
- future rules must explicitly state whether they accept top-level uncertainty, indexed uncertainty, or both

### Option C — Introduce a separate structured uncertainty object

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
- premature for the current need
- increases extractor and downstream implementation cost

## Recommendation

Approve Option B narrowly.

`uncertain_fields` may support exact deterministic indexed paths for rules that explicitly require per-element uncertainty marking, starting with BR-006.

This approval should be prospective.

It does not retroactively require BR-002 or any existing active rule to migrate from top-level uncertainty markers to indexed uncertainty markers.

BR-002's top-level `"fee"` convention remains valid within its own rule scope.

Future rules must state explicitly whether they use:

- top-level uncertainty markers only
- indexed uncertainty markers
- both, with precedence rules

## Contract Impact

This decision affects documentation semantics, not the current JSON Schema structure.

`schemas/activity.schema.json` already defines `uncertain_fields.items` as strings without a path-format constraint, so no structural schema change is required for Option B.

Affected documents:

- `docs/output-contracts.md`
- `docs/rule-authoring-guide.md`
- `rules/BR-006-per-session-date-completeness.md` if wording needs alignment after approval
- future extractor / validator guidance

Not affected:

- runtime pipeline
- source authority
- activity classification
- existing BR-001 to BR-005 behavior
- BR-002's existing top-level `"fee"` convention

## Implementation Gate

BR-006 remains held until this decision is approved and reflected in the relevant contract documentation.

Approval of this decision is necessary but not sufficient for implementation.

After approval:

1. Record the accepted decision in `docs/decisions.md`.
2. Update `docs/output-contracts.md` to define allowed `uncertain_fields` path semantics.
3. Update `docs/rule-authoring-guide.md` to require rules to declare top-level vs indexed uncertainty behavior.
4. Re-check BR-006 spec determinism.
5. Implement BR-006 validator.
6. Add focused tests.
7. Run regression.
