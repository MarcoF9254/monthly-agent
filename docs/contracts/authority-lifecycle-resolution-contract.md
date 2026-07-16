# Authority Lifecycle Resolution Contract Draft

Status: inactive Draft 0.1 contract; no runtime resolver exists

Resolution order is: admit one external trust anchor and one bundle; verify the anchor pins the effective complete snapshot; verify publication bootstrap without membership in that snapshot; verify lineage, closed-world completeness, and ordinary membership; resolve authorized revocations; remove revoked authorities; resolve authority supersession; independently resolve business-subject supersession; then derive run-metadata, eligibility, and selection outcomes.

Revocation precedes authority supersession. Broken, cyclic, cross-purpose, cross-scope, or multiple active authority tips fail closed. There is no intrinsic Phase 1 expiry; trust-anchor freshness defines revocation-knowledge freshness. Closed artifacts follow supersede-not-conceal. Published-output recall is out of scope.
