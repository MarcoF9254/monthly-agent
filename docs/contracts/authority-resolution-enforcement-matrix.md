# Authority Resolution Enforcement Matrix

Status: inactive contract design under `OD-BAI-CONTRACT-001`; no runtime enforcement implemented

Each blocking rule has exactly one primary enforcing component.

| Rule ID | Failure condition or threat | Primary enforcing component | Secondary verifier | Input boundary | Rejection result | Prohibited authoritative outcome | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BAI-TA-001 | Missing external trust anchor | Operational caller | Bundle verifier | Production admission | Reject request | Any authoritative resolution | BAI-N01 |
| BAI-TA-002 | Expected snapshot digest mismatch | Bundle verifier | Lifecycle resolver | Anchor + bundle | Reject bundle | Eligibility/selection resolution | BAI-N02 |
| BAI-TA-003 | Anchor tip and digest disagree | Bundle verifier | Lifecycle resolver | Anchor + snapshot | Reject bundle | Tip acceptance | BAI-N03 |
| BAI-LC-001 | Internally valid snapshot is stale | Lifecycle resolver | Bundle verifier | Anchored snapshot lifecycle | Reject snapshot | Stale-tip resolution | BAI-N04 |
| BAI-LC-002 | Rollback behind anchored tip | Lifecycle resolver | Bundle verifier | Anchored snapshot lifecycle | Reject snapshot | Rolled-back resolution | BAI-N05 |
| BAI-LC-003 | Multiple active snapshot tips | Lifecycle resolver | Registry snapshot validator | Snapshot lineage | Reject lineage | Ambiguous active tip | BAI-N06 |
| BAI-BV-001 | Declared artifact is missing | Bundle verifier | Bundle builder | Bundle boundary | Reject bundle | Partial resolution | BAI-N07 |
| BAI-BV-002 | Physical artifact is undeclared | Bundle verifier | Bundle builder | Bundle boundary | Reject bundle | Hidden-input resolution | BAI-N08 |
| BAI-BV-003 | One logical ID has conflicting content | Bundle verifier | Registry snapshot validator | Bundle inventory | Reject bundle | Ambiguous artifact identity | BAI-N09 |
| BAI-PA-001 | Snapshot publication is unauthorized | Registry publication authority verifier | Registry snapshot validator | Complete snapshot | Reject snapshot | Published registry tip | BAI-N10 |
| BAI-PA-002 | Publication authority purpose is wrong | Registry publication authority verifier | Artifact authority verifier | Publication authority | Reject authority | Cross-purpose publication | BAI-N11 |
| BAI-LC-004 | Snapshot supersession crosses scope | Lifecycle resolver | Registry snapshot validator | Snapshot lineage | Reject lineage | Cross-scope tip | BAI-N12 |
| BAI-AS-001 | Required revocation omitted from closed world | Artifact authority verifier | Registry snapshot validator | Snapshot entries | Reject resolution | Revoked grant treated active | BAI-N13 |
| BAI-RM-001 | Run/month binding differs | Run-metadata validator | Manifest validator | Metadata + scoped artifacts | Reject scope | Projection/manifest readiness | BAI-N14 |
| BAI-PA-003 | Subject changed with reused authority | Registry publication authority verifier | Registry snapshot validator | Subject + authority | Reject snapshot | Tampered publication | BAI-N15 |
| BAI-IN-001 | Loose files submitted to production | Operational caller | Bundle verifier | Production admission | Reject input | Any authoritative or publishable status | BAI-N16 |
| BAI-RS-001 | Empty snapshot lacks exact empty-subject authority | Registry snapshot validator | Registry publication authority verifier | Snapshot subject | Reject snapshot | Unauthorized empty closed world | BAI-N17 |
| BAI-BV-004 | Inventory ordering is non-canonical | Bundle verifier | Bundle builder | Bundle root | Reject bundle | Non-deterministic resolution | BAI-N18 |
| BAI-RS-002 | Unknown registry entry type | Registry snapshot validator | Bundle verifier | Snapshot entries | Reject snapshot | Unknown authority interpretation | BAI-N19 |
| BAI-LC-005 | Snapshot lineage is broken or cyclic | Lifecycle resolver | Registry snapshot validator | Snapshot lineage | Reject lineage | Unproven active tip | BAI-N20 |
| BAI-BV-005 | Declared artifact hash mismatches bytes | Bundle verifier | Bundle builder | Bundle inventory | Reject bundle | Tampered artifact use | matrix-only |
| BAI-RS-003 | Duplicate snapshot identity | Registry snapshot validator | Lifecycle resolver | Snapshot set | Reject snapshots | Ambiguous immutable version | matrix-only |
| BAI-RS-004 | Registry entry ordering malformed | Registry snapshot validator | Bundle verifier | Snapshot entries | Reject snapshot | Non-deterministic closed world | matrix-only |
| BAI-PA-004 | Publication authority revoked | Registry publication authority verifier | Artifact authority verifier | Publication authority | Reject snapshot | Revoked publication | matrix-only |
| BAI-RM-002 | `run_id` parsed to infer month | Run-metadata validator | Manifest validator | Run metadata | Reject inferred binding | Manifest readiness | matrix-only |
| BAI-PB-001 | Projection requested before authoritative resolution | Projection builder | Bundle verifier | Projection admission | Reject build | Publishable projection | matrix-only |
| BAI-MV-001 | Manifest scope differs from run metadata or selection | Manifest validator | Run-metadata validator | Manifest validation | Reject manifest | Manifest-ready status | matrix-only |

## OAR rules

| Rule ID | Failure condition | Primary enforcing component | Boundary | Result |
| --- | --- | --- | --- | --- |
| OAR-BS-001 | Publication envelope derives authority from the snapshot it authorizes | Registry publication bootstrap verifier | Snapshot bootstrap | Reject snapshot |
| OAR-BS-002 | Bootstrap exception used for a non-publication purpose | Registry publication bootstrap verifier | Bootstrap admission | Reject envelope |
| OAR-BS-003 | Publication subject or envelope evidence missing | Bundle verifier | Bundle inventory | Reject bundle |
| OAR-BS-004 | Publication subject/envelope digest binding mismatch | Registry publication bootstrap verifier | Complete snapshot | Reject snapshot |
| OAR-BS-005 | Publication envelope appears as ordinary membership | Registry snapshot validator | Snapshot entries | Reject snapshot |
| OAR-BS-006 | Anchor does not pin the complete effective snapshot | Bundle verifier | Anchor and bundle | Reject resolution |
| OAR-RV-001 | Revocation envelope is unauthorized | Revocation resolver | Ordinary membership | Ignore no revocation; reject claimed result |
| OAR-RV-002 | Revocation target is missing | Revocation resolver | Closed-world snapshot | Reject lifecycle |
| OAR-RV-003 | Target authority ID or artifact digest differs | Revocation resolver | Revocation target | Reject lifecycle |
| OAR-RV-004 | Target purpose, subject, or scope differs | Revocation resolver | Revocation target | Reject lifecycle |
| OAR-RV-005 | Revocation is resolved after supersession | Revocation resolver | Lifecycle pipeline | Reject lifecycle |
| OAR-RV-006 | Revocation reason identifier is structurally invalid | Subject schema validator | Subject admission | Reject revocation subject |
| OAR-SB-001 | Envelope subject type, ID, digest, purpose, or scope differs | Authority subject-binding verifier | Subject plus envelope | Reject authority |
| OAR-SB-002 | Envelope reuses a binding after subject mutation | Authority subject-binding verifier | Subject plus envelope | Reject authority |
| OAR-SB-003 | Ordinary envelope lacks exact anchored membership | Artifact authority verifier | Effective snapshot | Reject authority |
| OAR-AL-001 | Multiple active authority tips exist | Authority lifecycle resolver | Authority lineage | Reject lifecycle |
| OAR-AL-002 | Authority supersession is broken or cyclic | Authority lifecycle resolver | Authority lineage | Reject lifecycle |
| OAR-AL-003 | Authority and business-subject supersession are conflated | Authority lifecycle resolver | Outcome resolution | Reject outcome |
| OAR-AL-004 | Intrinsic expiry is inferred in Phase 1 | Authority lifecycle resolver | Lifecycle evaluation | Reject inferred expiry |

Every row has exactly one named primary component. Secondary review does not transfer primary ownership.
