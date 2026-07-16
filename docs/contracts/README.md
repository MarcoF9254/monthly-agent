# Contract Index

## OAR closure status

The Bounded Calendar Authority Chain v0 architecture is frozen. PR #18 accepted and merged the OAR contracts, inactive Draft 0.x schemas, and fictional authority/revocation fixtures. PR #19 accepted and merged the fictional year-2099 offline authority verifier prototype.

The prototype verifies RFC 8785/SHA-256 bindings, a separately supplied fictional trust anchor, the non-self-authorizing registry-publication bootstrap, ordinary closed-world membership, exact subject/envelope binding, authorized revocation before authority supersession, independent business-subject supersession, deterministic fictional outcomes, two positive scenarios, and twenty negative first-failure cases. Its merge validation baseline was 147 passed with one pre-existing unrelated skip.

The verifier is executable fictional evidence only. It is not production-ready, does not activate any Draft 0.x schema, and does not implement operational trust-anchor delivery, real registry publication, or real authority issuance.

## Active contracts

- `docs/pipeline-run-contract.md` — D1 auditable run contract.
- `docs/output-contracts.md` — validator output contracts.

## Accepted architecture and inactive draft contracts

Calendar-only architecture and retained contracts:

- `docs/contracts/calendar-only-vertical-slice-contract.md`
- `docs/contracts/calendar-projection-contract.md`
- `docs/contracts/external-authority-registry-contract.md`
- `docs/contracts/calendar-only-fictional-fixture-test-matrix.md`

The external-authority-registry draft remains inactive and is not the anchored closed-world OAR snapshot.

OAR and bounded-input contracts:

- `docs/contracts/authority-resolution-input-contract.md`
- `docs/contracts/authority-subject-boundary-contract.md`
- `docs/contracts/owner-authority-envelope-contract.md`
- `docs/contracts/calendar-eligibility-subject-contract.md`
- `docs/contracts/calendar-monthly-selection-subject-contract.md`
- `docs/contracts/run-metadata-binding-subject-contract.md`
- `docs/contracts/authority-revocation-subject-contract.md`
- `docs/contracts/registry-publication-bootstrap-contract.md`
- `docs/contracts/registry-snapshot-contract.md`
- `docs/contracts/resolution-bundle-contract.md`
- `docs/contracts/trust-anchor-contract.md`
- `docs/contracts/authority-lifecycle-resolution-contract.md`
- `docs/contracts/authority-resolution-enforcement-matrix.md`
- `docs/contracts/bounded-authority-fictional-fixture-test-matrix.md`
- `docs/contracts/oar-draft-migration-plan.md`

Inactive Draft 0.x schemas:

- `schemas/drafts/calendar-only/external-authority-registry.schema.json`
- `schemas/drafts/calendar-only/calendar-activity-projection.schema.json`
- `schemas/drafts/calendar-only/calendar-monthly-manifest.schema.json`
- `schemas/drafts/bounded-authority-input/trust-anchor.schema.json`
- `schemas/drafts/bounded-authority-input/authority-registry-snapshot.schema.json`
- `schemas/drafts/bounded-authority-input/resolution-bundle-root.schema.json`
- `schemas/drafts/owner-authority-resolution/authority-envelope.schema.json`
- `schemas/drafts/owner-authority-resolution/authority-revocation-subject.schema.json`
- `schemas/drafts/owner-authority-resolution/calendar-eligibility-subject.schema.json`
- `schemas/drafts/owner-authority-resolution/calendar-monthly-selection-subject.schema.json`
- `schemas/drafts/owner-authority-resolution/registry-publication-subject.schema.json`
- `schemas/drafts/owner-authority-resolution/run-metadata-binding-subject.schema.json`

These schemas are not runtime inputs and remain inactive despite successful fictional prototype verification.

## Fictional fixtures and verifier navigation

Accepted fictional scenarios:

- `examples/contract-fixtures/owner-authority-resolution/positive/pre-revocation/`
- `examples/contract-fixtures/owner-authority-resolution/positive/post-revocation/`
- `examples/contract-fixtures/bounded-authority-input/negative/negative-cases.json`

Fictional-only offline verifier:

- `tools/oar_verifier/`
- `tools/verify_fictional_authority.py`

Verifier tests:

- `tests/test_oar_canonical.py`
- `tests/test_oar_positive_scenarios.py`
- `tests/test_oar_negative_cases.py`
- `tests/test_oar_fail_closed.py`

## Historical Gate 2 context

At Gate 2, the bounded-input fixtures proved only the trusted-tip, closed-world snapshot, bundle-completeness, ordering, and run-metadata envelope. Executable owner-authority verification was then a separate blocker. PR #18 supplied the accepted OAR contract and fixture package, and PR #19 resolved the fictional-verifier blocker.

The production boundary remains unresolved and unauthorized: fictional verification does not provide real trust-anchor delivery, real registry publication, real authority/revocation issuance, R03 eligibility or selection, projection or manifest activation, calendar downstream activation, BR-006 activation, D3 resolution, or published-output recall.
