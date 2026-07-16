# Registry Publication Bootstrap Contract Draft

Status: inactive Draft 0.1 contract; non-self-authorizing bootstrap exception

The registry-publication subject binds the snapshot core: contract version, registry and snapshot identities, predecessor identity/digest, exact scope, and complete ordered ordinary entry inventory. It excludes its digest, publication envelope/evidence, publication metadata, and complete snapshot digest.

Construction is: snapshot core → canonical publication subject → subject digest → generic envelope with purpose/type `calendar-registry-publication` → envelope artifact digest → complete snapshot attaching subject/envelope references → complete snapshot artifact digest → externally delivered trust anchor.

The publication envelope is not an ordinary entry in the snapshot it authorizes and derives no authority from that snapshot. The bootstrap verifier accepts it only as evidence bound into the exact complete snapshot pinned by the trusted delivery channel. Using this exception for another purpose fails closed.

Schema validation and hashing provide integrity, not authentication. Phase 1 trust ultimately reduces to the owner-controlled external trust-anchor delivery channel. A later anchor transition, not same-snapshot revocation metadata, ends future publication authority.
