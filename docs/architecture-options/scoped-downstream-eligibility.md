# Scoped Downstream Eligibility — Architecture Options

Status: Draft for independent review. Option D is owner-authorized for drafting only, not finally accepted or activated.

## Owner-reviewed Options

### Option A — Eligibility in the activity schema

Store consumer eligibility in each activity record. This is direct, but couples mutable, consumer-specific authority to source evidence and invites schema expansion for every consumer.

### Option B — Eligibility in an approval or authority artifact alone

Keep owner decisions outside the activity schema. This separates evidence from authority, but is insufficient by itself: a decision artifact does not define a least-data renderer payload, deterministic field transformation, or projection provenance.

### Option C — Projection alone

Generate a consumer-shaped payload from evidence. This minimizes renderer inputs, but is insufficient by itself: a projection cannot self-authorize, prove owner approval, or distinguish permission from technical producibility.

### Option D — Policy plus scoped approval plus generated projection

Use a consumer policy contract, an immutable owner decision scoped to one evidence record and consumer, and a deterministic allowlisted projection with separately bound provenance. This adds lifecycle, validation, and reproducibility requirements, but cleanly separates evidence, authority, policy, and delivery.

## Rejected Variants and Anti-patterns

- Treating `qa_status: approved` as consumer permission conflates record review with authority.
- Writing eligibility or projections into closed run trees mutates or mixes later authority with immutable historical evidence.
- Inferring precedence from filenames, modification times, directory order, or timestamps alone is non-deterministic and unauthorized.

## Recommendation

Option D. Missing, unmatched, unverifiable, duplicated, cyclic, cross-scope, or otherwise broken authority fails closed. Final architecture acceptance and all implementation or activation require later explicit Architecture Owner approval.
