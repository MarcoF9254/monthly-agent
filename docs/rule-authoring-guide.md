# Business Rule Authoring Guide

Status: Draft guidance derived from BR-001 through BR-005 as committed. Use this guide to keep BR-006 and later rules consistent with the repository's existing rule structure.

## Purpose

This guide documents the section structure used by `rules/BR-001-*.md` through `rules/BR-005-*.md`, so BR-006 and later rules can follow existing repository conventions rather than a structure invented independently.

This guide separates:

- **Core sections**: present in every existing rule spec, in the same order.
- **Conditional sections**: present only in some rule specs, added when a rule's design requires them.

No new mandatory heading is introduced here that does not already appear in at least one committed rule spec.

## Core Sections

Every rule spec from BR-001 through BR-005 contains all of the following, in this order:

1. **`# BR-XXX Rule Title`**: top-level heading combining rule ID and a short name.
2. **`## Rule ID`**: the bare rule ID, such as `BR-005`.
3. **`## Rule Name`**: one-line statement of what the rule enforces.
4. **`## Purpose`**: why the rule exists, in terms of what harm it prevents.
5. **`## Pass Condition`**: the exact condition or conditions under which a record passes. This must be phrased so it can be evaluated without semantic judgement.
6. **`## Fail Condition`**: the exact condition or conditions under which a record fails. This should be the logical complement of Pass Condition, not a vague restatement.
7. **`## Severity`**: severity level or levels the rule assigns. If more than one fail scenario exists, map each scenario to its severity explicitly. BR-004 is the pattern to follow.
8. **`## Example Pass`**: at least one concrete example. This may be a single inline example, or multiple labeled sub-examples when the rule has several distinct pass paths.
9. **`## Example Fail`**: at least one concrete failing example.
10. **`## Human Review Guidance`**: what a human reviewer should do when the rule fires. This should give an actionable next step, not just restate the fail condition.

## Field Declaration Section

Every rule so far declares which record fields it touches, but two forms exist.

The field declaration section should appear after Purpose and before Pass Condition.

### Form A: `## Applies to Fields`

Used by BR-001, BR-002, BR-004, and BR-005.

This is a flat bullet list of field names the rule reads or reports against.

### Form B: `## Scope`

Used by BR-003.

Use this variant when a rule needs to explicitly state what it does not consider, in addition to what it does. It contains:

- An `Applies to:` bullet list.
- An `Out of scope:` bullet list.
- A sentence stating what the validator must not infer from out-of-scope fields.

BR-003 uses this pattern because registration timing must not be inferred from `registration_method`, activity dates, centre practice, or assumptions not stated in the source.

Guidance for BR-006 and later: use Form A by default. Use Form B only when the rule's correctness depends on explicitly excluding related fields the validator must not use for inference. Do not invent a third form.

## Conditional Sections

These sections appear in some rule specs and should be added only when the same underlying need exists. Do not add them by default or for symmetry with another rule.

| Section | Used by | When to add it |
| --- | --- | --- |
| `## Validation Scope` | BR-004, BR-005 | The rule only applies at a specific pipeline stage, or explicitly defers a related condition to another rule. State which rule owns the deferred condition. |
| `## Overlapping Findings` | BR-002, BR-003 | The rule may legitimately fire on the same field or item as another rule for a different reason. State this explicitly so it is not mistaken for a duplicate-finding bug. |
| `## Recognized <X> Indicators` | BR-002, BR-003 | The rule depends on a closed list of exact-match strings. Include the literal list plus explicit matching rules. |
| `## Deterministic <X> Inputs` | BR-005 | The rule accepts more than one kind of deterministic evidence and needs to enumerate them before Pass/Fail Condition can reference them concisely. |
| `## Exact Anchor Matching` / `## Matching Rules` | BR-003, BR-005 | The rule's matching logic is non-trivial enough that Pass/Fail Condition would be ambiguous without spelling it out separately. If the rule tokenizes an input field, list the fixed delimiter set explicitly. |
| `## Finding Field Guidance` | BR-004, BR-005 | The rule has more than one possible fail scenario with different `field`/`path` assignments, or the rule reads fields that must never appear in findings. |
| `## Boundary Examples` | BR-005 | Pass/Fail Condition alone leaves genuine edge cases ambiguous. Boundary Examples should resolve those edges explicitly. |
| `## Valid <X> Timing Examples` | BR-003 | The pass space is large and varied enough that a single Example Pass section would not give enough implementation guidance. |
| `## Pending Decision` | BR-006 | The rule specification is blocked by an unresolved architecture, schema, output-contract, or business-authority decision. Do not use it for ordinary TODOs, implementation notes, discussion notes, or speculative ideas. |

### Pending Decision Sections

Use `## Pending Decision` only when a rule specification is blocked by an unresolved architecture, schema, output-contract, or business-authority decision.

Do not use it for ordinary TODOs, implementation notes, discussion notes, or speculative ideas.

The section must include:

- the exact canonical label from `docs/governance.md`:

```text
DECISION PENDING — Requires Human Approval
```

- a clear statement of the unresolved decision
- why the rule cannot be implemented until the decision is approved
- what existing contract or boundary would be affected
- confirmation that implementation is held until approval

A pending decision inside a rule spec does not make the decision approved.

It must not be treated as an accepted ADR.

If the decision is later approved, the accepted architecture decision should be recorded in `docs/decisions.md` where appropriate.

## Closed-List Matching Rules

Any rule that checks a field value against a fixed set of recognized strings must include these constraints, following BR-002 and BR-003:

- Trim surrounding whitespace before comparison.
- English matching is case-insensitive.
- Chinese matching is exact after trimming.
- Do not use broad substring, regex, fuzzy, or NLP matching unless the specification is later explicitly updated to allow it.
- State explicitly whether a recognized value embedded inside a longer sentence should be treated as a match. BR-003's precedent is that it should not, unless the spec is later updated to allow contains matching.

## Determinism Requirement

This is not a section to add to every rule. It is a constraint every Pass/Fail Condition must satisfy.

A validator must be able to evaluate Pass/Fail using only:

- The record's own fields.
- A fixed closed list.
- A fixed deterministic pattern, such as regex or delimiter-based tokenization.

A validator must not require access to the original source document, semantic or similarity judgement, fuzzy matching, translation, synonym matching, or NLP.

If a rule's Pass/Fail wording uses terms such as "specific enough", "too vague", "similar to", or "likely to be", that wording is not implementable yet. Replace it with an explicit closed list, exact-match anchor, or structural pattern before accepting the spec.

If a rule's correctness requires comparing across multiple records in the same batch, this must be stated explicitly in `Validation Scope`, because the existing rule engine calls every rule as `check(record, index) -> list` with no access to sibling records. Per BR-005's precedent, prefer simplifying the rule to stay per-record over changing the engine interface.

## Finding Output

This is not a rule-spec section. It applies to implementations and is included here for completeness.

Every rule implementation must emit findings using exactly these eight keys, per `docs/output-contracts.md`:

- `index`
- `activity_id`
- `rule_id`
- `field`
- `path`
- `severity`
- `message`
- `recommendation`

A rule spec does not need its own section restating this contract. It should reference `docs/output-contracts.md` if anything rule-specific about `field` or `path` assignment needs clarification. Use `Finding Field Guidance` for that case.

## Open Question

BR-005 introduced an inline version label (`BR-005 v1`) without a dedicated section or repo-wide convention. This guide does not resolve whether versioning should be a section, a filename convention, or deferred to a future `docs/spec-versioning.md`. BR-006 authors should not independently invent a versioning convention without review.
