# Calendar-Only Fictional-Fixture Test Matrix

Status: test design only; no fixtures or runtime tests implemented

All future identifiers use `example-` or year `2099`. No R03 identifier or record may appear.

| ID | Fictional case | Expected result |
| --- | --- | --- |
| P01 | One externally verified eligible root with exact calendar fields | eligible |
| P02 | Authorized subset selection; all selected activities valid | manifest contains exactly selected subset |
| P03 | Eligible but unselected projection exists | projection excluded from manifest |
| P04 | Explicit authorized empty selection | canonical empty manifest passes |
| P05 | Eligible decision superseded by verified denial | revoked; fail closed |
| P06 | Revoked authority with valid external revocation artifact | authority rejected |
| P07 | Same validated inputs regenerated | identical hashes and IDs |
| P08 | Valid non-circular selection subject, authority artifact, complete selection artifact, and manifest chain | passes |
| N01 | Missing monthly selection | whole manifest fails closed |
| N02 | Duplicate active selections | fail closed |
| N03 | Broken selection predecessor | fail closed |
| N04 | Cyclic selection chain | fail closed |
| N05 | Cross-run, consumer, or month selection supersession | fail closed |
| N06 | Unsorted or duplicate selected activity IDs | fail closed |
| N07 | Selection contains ineligible activity | whole manifest fails closed |
| N08 | Selection contains invalid projection | whole manifest fails closed |
| N09 | Builder silently drops selected activity | fail closed |
| N10 | Eligible but unselected activity added | fail closed |
| N11 | Partial calendar `allowed_fields` | fail closed |
| N12 | Additional calendar `allowed_fields` | fail closed |
| N13 | Denied or revoked effective eligibility | fail closed |
| N14 | Duplicate active eligibility tips | fail closed |
| N15 | Broken, cyclic, or cross-scope eligibility chain | fail closed |
| N16 | Evidence and payload activity IDs differ | fail closed |
| N17 | Projection and manifest runs differ | fail closed |
| N18 | Projection and manifest consumers differ | fail closed |
| N19 | Selection and manifest programme months differ | fail closed |
| N20 | Authoritative run metadata and programme month differ | fail closed |
| N21 | Referenced projection is schema-invalid | fail closed |
| N22 | Projection ID recomputation differs | fail closed |
| N23 | Payload hash recomputation differs | fail closed |
| N24 | Manifest entry projection ID or hash differs | fail closed |
| N25 | Manifest entries unsorted or duplicated | fail closed |
| N26 | Manifest identity includes itself or recomputation differs | fail closed |
| N27 | Registry grant artifact missing or hash mismatched | fail closed |
| N28 | Revocation declared without verified external revocation evidence | fail closed |
| N29 | Revocation artifact scope differs from original authority | fail closed |
| N30 | Empty manifest without explicit effective empty selection | fail closed |
| N31 | Selection resolution fails and directory is empty | fail closed, not empty publication |
| N32 | Renderer payload contains `source_reference` | fail closed |
| N33 | Dates/time normalized, inferred, reordered, truncated, or partial | fail closed |
| N34 | Artifact placed under `data/runs/` | fail closed |
| N35 | Eligibility authority used for monthly selection | fail closed |
| N36 | Monthly-selection authority used for eligibility | fail closed |
| N37 | Revocation authority used as a grant | fail closed |
| N38 | Modified `selected_activity_ids` with unchanged subject hash | fail closed |
| N39 | Recomputed selection subject hash with unchanged authority binding | fail closed |
| N40 | Wrong selection run, consumer, or month with otherwise valid authority | fail closed |
| N41 | Authority artifact binds wrong subject type | fail closed |
| N42 | Authority artifact binds wrong subject digest | fail closed |
| N43 | Manifest binds a complete selection artifact different from the owner-authorized subject | fail closed |
| N44 | Incomplete resolver input happens to contain one apparent active tip | fail closed |
| N45 | Registry entry has wrong authority purpose | fail closed |

Future fixture review must prove examples are fictional, schema-valid where intended, and incapable of granting real authority.
