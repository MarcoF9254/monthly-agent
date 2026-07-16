# Authority Revocation Subject Contract Draft

Status: inactive Draft 0.1 contract; no revocation is issued

A revocation subject binds exactly the target authority ID and digest, target purpose, target subject type, ID and digest, target exact scope, and a governed non-empty reason-code identifier. The schema enforces stable identifier syntax only; owner-approved governance defines actual codes.

A file has no revocation authority because of its name or contents. Its subject must be bound by a generic envelope with purpose and subject type `calendar-authority-revocation`, with effective ordinary membership in the anchored snapshot.

Resolution fails closed for an absent target or any target identifier, digest, purpose, subject, or scope mismatch. Authorized revocation resolves before authority supersession. Revoked authorities remain historical provenance.

A publication envelope cannot learn authoritative revocation from the snapshot it authorized. A later externally anchored snapshot may retain revocation evidence, but the trust-anchor transition is the decisive future-authorization change.
