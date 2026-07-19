# D4A — BR-006 Shadow Evidence Contract

## Purpose and status

Status: **Proposed under an Owner-authorized bounded contract-drafting pilot.** This is a Draft PR work product. It is not independently reviewed, accepted, or repository-effective.

This contract defines evidence and fail-closed boundaries for a possible future, separately authorized BR-006 real-data shadow vertical slice. It is contract-only, pre-activation, non-authoritative, and has no runtime effect. It does not execute or authorize a shadow run.

The provisional classification is Tier 2 because this documentation-only PR introduces a new evidence contract and semantic boundaries governing future real-data shadow evaluation. Future review requires two separately qualified independent perspectives on the same exact head, subject to Owner qualification under repository-effective governance. This classification does not qualify reviewers or authorize review, Ready, merge, or activation.

## Frozen input identity

A separately authorized shadow run must bind its evidence to one exact immutable input. Before execution, record:

- the exact run or dataset ID and governed locator;
- digest algorithm and full cryptographic digest of the complete input;
- artifact size and, for a set, a deterministic member manifest and member digests;
- repository, base commit, execution commit, and clean-code identity; and
- the authorization selecting that exact input.

Freeze the input before the first invocation. Apply the same digest procedure immediately before and after every baseline, BR-006 shadow, D3, and comparison step. Pre-run and post-run digests must be equal. Any mismatch invalidates the complete shadow run; no partial result survives as activation evidence.

Closed R03 artifacts are immutable. A future process may access only an exact frozen input under separate authorization and must not create, overwrite, relabel, repair, copy into, or otherwise modify a closed R03 run or its artifacts. This contract records no R03 data identity and authorizes no R03 access or processing.

## Shadow isolation

BR-006 remains outside the active business-rule registry. A future shadow invocation must be explicit, separately authorized, and mechanically separate from the active registry invocation. Existing BR-001 through BR-005 results remain the authoritative baseline.

BR-006 shadow output is a separate, non-authoritative evidence stream. It must not overwrite, merge into, suppress, relabel, or rewrite baseline artifacts or findings. It cannot change `qa_status`, approve a record, grant consumer eligibility, or create projection, manifest, publication, production, or downstream authority.

## D3 boundary and semantic gate

D3 validates attempted indexed-marker syntax only. A D3 no-finding result is not authorization. Bare top-level markers remain outside D3 adjudication authority; passage without a finding conveys no field-name, schema, rule-specific, runtime, or activation authority.

After D3, a separate BR-006-specific semantic gate must decide whether the exact marker is authorized for BR-006. It must fail closed when authorization is absent, ambiguous, or contradictory. D3 syntax validity never authorizes BR-006 semantics, registry membership, runtime use, or activation.

## Required shadow evidence

A complete evidence package records all of the following without altering authoritative artifacts:

1. Exact frozen input identity and locator, digest algorithm, pre-run digest, post-run digest, and equality result.
2. Repository identity, exact base and execution SHAs, complete commit chain, clean-state result, and code/package identity.
3. Exact BR-006 implementation, rule, configuration, invocation, and output-contract identities, with digests when external to the execution commit.
4. Complete authoritative baseline BR-001 through BR-005 findings, artifact identity, and digest.
5. Complete separate non-authoritative shadow BR-006 findings, artifact identity, and digest.
6. Complete D3 findings for attempted indexed markers, artifact identity, and digest.
7. Deterministic record-by-record and finding-by-finding comparison of baseline, shadow, and D3 results.
8. Overlap and duplicate-finding analysis that identifies every related finding and assigns ownership without deleting or rewriting evidence.
9. Expected-versus-observed analysis, the source of every expectation, and every unexplained deviation.
10. Human Review or separately governed adjudication handoff for source-dependent questions.
11. Complete unresolved-disagreement list, including D3/BR-006 contradictions and ownership disputes.
12. One activation-readiness conclusion from the vocabulary below, with reasons and confirmation that it does not activate BR-006.

Missing evidence cannot be inferred, reconstructed from altered artifacts, or waived because results appear favorable.

## Finding overlap and ownership

Schema validation and BR-001 own a missing `dates` field, invalid top-level `dates` shape, or empty `dates[]`. BR-006 owns per-entry `dates[i].date_text` completeness when `dates[]` exists with at least one entry.

The comparison must detect exact duplicates and semantic overlaps; report rule IDs, record identity, paths, messages, and ownership rationale; and preserve original findings. It must not silently suppress, deduplicate, rewrite, or prefer a shadow finding. Missing or incomplete ownership analysis fails closed. A material ownership disagreement that remains after complete analysis and is explicitly recorded receives `blocked_by_disagreement` under the outcome precedence.

## Source-evidence boundary

Deterministic validators must not open or interpret the original PDF or other original source material. Only an authorized human or separately governed review process may use original source material for adjudication. That conclusion remains distinct from deterministic findings and must cite its authorization and evidence.

Validators and comparison tooling must not infer, repair, normalize, translate, copy, propagate, or auto-fill dates. Shadow evaluation observes the frozen input; it does not correct it.

## Outcome vocabulary

Record exactly one non-authorizing outcome:

- `evidence_sufficient_for_activation_consideration`: use only when the shadow run and evidence chain are valid; all mandatory evidence is present and internally consistent; no material disagreement remains; and evidence coverage and probative strength are sufficient for later independent review and Owner consideration.
- `evidence_insufficient`: use only when the shadow run and evidence chain are valid; all mandatory identity, integrity, completeness, procedure, and authority gates passed; all mandatory evidence artifacts were validly produced; no material unresolved disagreement remains; but coverage, representativeness, variation, or probative strength is insufficient to support activation consideration. Examples include a valid real-data slice containing no relevant BR-006 negative case, lacking sufficient positive and negative variation, or being complete and internally valid but too narrow to support an activation decision. Missing or incomplete mandatory artifacts or evidence, stale identity, an unauthenticated baseline, incomplete required comparison, integrity failure, unauthorized mutation, or an authority-boundary violation must not receive this outcome; each invalidates the shadow run.
- `blocked_by_disagreement`: use only when the shadow run and evidence chain are valid and mandatory evidence is complete, but a material semantic, finding-ownership, expected-versus-observed, Human Review, or adjudication disagreement remains unresolved. The disagreement must be explicitly recorded.
- `invalid_shadow_run`: use when any mandatory identity, integrity, completeness, procedural, isolation, authorization, or evidence-chain gate fails. This includes missing, incomplete, altered, stale, unauthenticated, or mismatched mandatory evidence; incomplete comparison; mutation; unauthorized artifact action; closed-run write; or any other fail-closed condition. The run is unusable as activation evidence.

Apply this deterministic precedence and stop at the first matching condition:

1. If any fail-closed condition is triggered, record `invalid_shadow_run` as the final outcome.
2. Otherwise, if a material unresolved disagreement remains, record `blocked_by_disagreement` as the final outcome.
3. Otherwise, if the valid, complete, internally consistent evidence lacks sufficient coverage or probative strength, record `evidence_insufficient` as the final outcome.
4. Otherwise, record `evidence_sufficient_for_activation_consideration`.

No fact pattern may map to more than one outcome.

No outcome activates BR-006, changes registry membership, approves records, grants eligibility, or authorizes downstream use. Even `evidence_sufficient_for_activation_consideration` is only input to a later decision.

## Fail-closed conditions

The result must be `invalid_shadow_run` and unusable as activation evidence upon:

- input digest mismatch or unequal pre-run and post-run digests;
- post-run mutation or mutation of input, code, evidence, or a closed run;
- missing, incomplete, altered, or unauthenticated baseline evidence;
- a D3/BR-006 contradiction that establishes absent, ambiguous, or contradictory semantic authorization;
- any changed artifact outside the future authorization's exact allowlist;
- incomplete comparison, expected-versus-observed analysis, or disagreement list;
- missing or incomplete duplicate or overlap analysis, ownership assignment, or recording of an unresolved ownership disagreement;
- stale, ambiguous, dirty, or mismatched repository, commit, code, rule, or configuration identity;
- an attempt to write into, overwrite, relabel, or repair a closed run;
- an attempt to treat shadow findings as authoritative runtime findings;
- baseline overwrite, suppression, mutation, or silent deduplication;
- missing adjudication handoff where source interpretation is required; or
- an attempt to derive approval, eligibility, projection, manifest, publication, production, downstream, or activation authority.

An invalid attempt may be preserved only as governed failure evidence in a separately authorized destination. It must not be repaired or rerun merely to obtain a favorable outcome without new authorization and a new unique evidence-attempt identity.

## Human authority

Only the Owner may authorize BR-006 activation. Shadow evidence supports a later decision but cannot make it. Independent review remains required under governance effective for the exact future work product and head. Reviewer identity and qualification remain pending Owner decision under that governance; this contract and provisional classification supply neither.

Human Review may resolve source-dependent questions but cannot retroactively validate a broken deterministic evidence chain. Record approval, consumer eligibility, and activation remain separate authority decisions.

## Explicit exclusions and held authorities

This D4A Draft PR provides no authority for:

- D4B execution or any shadow run;
- real-data access or processing;
- BR-006 registry change or activation;
- validator, test, rule, schema, workflow, configuration, pipeline-runner, or comparison-tool implementation;
- R03 artifact creation, reading, copying, transformation, or modification;
- `qa_status` change, record approval, or consumer eligibility;
- projection, manifest, publication, recall, downstream use, or production authority;
- trust-anchor delivery; or
- Phase 2.

Drafting does not complete D4A. Acceptance and repository effect require the separately authorized governance path, exact-head independent review, Owner decisions, and merge. No review request, Ready, merge, D4B, or activation authority is granted.
