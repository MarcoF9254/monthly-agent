# Bounded Authority Fictional-Fixture Test Matrix

Status: test design and fictional data only; no runtime harness or production artifacts

Base: `examples/contract-fixtures/bounded-authority-input/positive/valid-resolution-chain/`

All data uses year 2099 and `example-` identifiers. It grants no real authority.

`valid-resolution-chain` means a valid Gate 2 bounded-input envelope chain only. The positive chain demonstrates trusted-tip anchoring, registry publication, closed-world snapshot identity, bounded bundle completeness, ordering, and run-metadata binding.

It does not constitute executable end-to-end verification of the separate owner-authority artifacts referenced by the fictional calendar eligibility and monthly-selection decisions. Their authority-artifact schemas, fixtures, and verifiers remain a separate blocker requiring separate owner authorization.

## Positive Chain

| ID | Case | Expected |
| --- | --- | --- |
| BAI-P01 | External anchor names the one authorized snapshot and exact complete digest | pass |
| BAI-P02 | Publication authority binds the canonical snapshot subject with `calendar-registry-publication` | pass |
| BAI-P03 | Run metadata, snapshot, selection, and bundle scope agree | pass |
| BAI-P04 | Two structurally valid fictional eligibility decisions exist; selection includes only activity 001 | deterministic one-selected/one-unselected envelope input |
| BAI-P05 | Root inventory is complete, unique, hashed, and canonically ordered | pass |
| BAI-P06 | Repeated canonical construction produces identical subject, snapshot, and bundle identities | pass |

## Machine-Applicable Negative Corpus

File: `examples/contract-fixtures/bounded-authority-input/negative/negative-cases.json`

| Fixture | Expected rule | Primary owner | Intended rejection |
| --- | --- | --- | --- |
| BAI-N01 | BAI-TA-001 | Operational caller | missing anchor |
| BAI-N02 | BAI-TA-002 | Bundle verifier | wrong expected digest |
| BAI-N03 | BAI-TA-003 | Bundle verifier | tip/digest disagreement |
| BAI-N04 | BAI-LC-001 | Lifecycle resolver | stale valid snapshot |
| BAI-N05 | BAI-LC-002 | Lifecycle resolver | rollback |
| BAI-N06 | BAI-LC-003 | Lifecycle resolver | two active tips |
| BAI-N07 | BAI-BV-001 | Bundle verifier | missing declared artifact |
| BAI-N08 | BAI-BV-002 | Bundle verifier | undeclared artifact |
| BAI-N09 | BAI-BV-003 | Bundle verifier | conflicting logical identity |
| BAI-N10 | BAI-PA-001 | Registry publication authority verifier | unauthorized publication |
| BAI-N11 | BAI-PA-002 | Registry publication authority verifier | wrong typed purpose |
| BAI-N12 | BAI-LC-004 | Lifecycle resolver | cross-scope supersession |
| BAI-N13 | BAI-AS-001 | Artifact authority verifier | omitted revocation |
| BAI-N14 | BAI-RM-001 | Run-metadata validator | run/month mismatch |
| BAI-N15 | BAI-PA-003 | Registry publication authority verifier | tampered subject/reused authority |
| BAI-N16 | BAI-IN-001 | Operational caller | production loose files |
| BAI-N17 | BAI-RS-001 | Registry snapshot validator | unauthorized empty snapshot |
| BAI-N18 | BAI-BV-004 | Bundle verifier | malformed ordering |
| BAI-N19 | BAI-RS-002 | Registry snapshot validator | unknown entry type |
| BAI-N20 | BAI-LC-005 | Lifecycle resolver | broken/cyclic lineage |

Each mutation starts from the valid base chain and supplies an operation, deterministic artifact path, optional JSON Pointer, expected layer, rule, primary owner, and semantic reason. Validation must first prove the unmodified base is schema-valid, then apply the mutation and assert the named semantic rule is the first failure.
