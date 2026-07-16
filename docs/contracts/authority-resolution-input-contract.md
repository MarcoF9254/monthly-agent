# Authority Resolution Input Boundary Contract Draft

Status: contract drafting authorized by `OD-BAI-CONTRACT-001`; inactive, unimplemented, and not accepted as executable

## Production Boundary

Production authority resolution consumes exactly one externally supplied trust anchor plus one self-contained verified resolution bundle. Both must describe the same exact `registry_id`, `snapshot_id`, snapshot artifact digest, and scope.

## Fictional Proof Boundary

The positive fictional chain is complete for the Gate 2 bounded-input envelope only. It demonstrates trusted-tip anchoring, registry publication, closed-world snapshot identity, bounded bundle completeness, ordering, and run-metadata binding.

It does not constitute executable end-to-end verification of the separate owner-authority artifacts referenced by calendar eligibility or monthly-selection decisions. Those authority-artifact schemas, fixtures, and verifiers remain a separate blocker and require separate owner authorization.

The fixture directory named `valid-resolution-chain` therefore means a valid Gate 2 resolution-input chain, not a complete production authority-resolution chain or a fully verified eligibility/selection authority chain.

`registry_id` is the logical registry identity. `snapshot_id` is one immutable published version identity. They are not synonyms.

The existing external authority registry is not the authorized closed-world registry publication snapshot. The Gate 2 snapshot may enclose registry information, but does not activate, replace, or upgrade the existing inactive calendar-only registry schema.

Loose files may be used only for linting or fictional fixture authoring. Production loose-file input fails at admission and cannot yield authoritative eligibility, authoritative monthly selection, publishable projection, or manifest-ready status.

## Exact Scope

The exact scope is `run_id` + `consumer_id` + `programme_month` + `registry_purpose: calendar-authority-resolution`. Every boundary comparison uses exact equality.

## Fail Closed

Missing or conflicting anchors, missing bundles, scope disagreement, unverified bundle completeness, unknown artifact type, or any failed downstream authority/lifecycle check rejects the whole resolution request. No partial authoritative result exists.

Storage location, filename, timestamp, version number, highest or only visible tip, directory order, and generation order confer no authority.

## OAR Resolution

OAR uses separately hashed subjects and generic authority envelopes. Ordinary authority must be exact membership in the anchored snapshot. Registry publication is the single non-self-authorizing bootstrap exception. This remains inactive.

## OAR Resolution

OAR uses separately hashed subjects and generic authority envelopes. Ordinary authority must be exact membership in the anchored snapshot. Registry publication is the single non-self-authorizing bootstrap exception. This remains an inactive contract package.

## OAR Resolution

The OAR fixtures replace the former Gate 2 prototype with separately hashed subjects and generic authority envelopes. Ordinary authority must be exact membership in the anchored snapshot. Registry publication is the single non-self-authorizing exception described by the bootstrap contract. This remains an inactive contract package, not implementation authorization.
