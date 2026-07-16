# Calendar-Only Vertical Slice Contract Package

Decision authority: `OD-CAL-ARCH-001`, `OD-CAL-ARCH-002`, and `OD-CAL-ARCH-003`

Status: architecture direction approved for contract drafting; executable contracts remain draft `0.x`, unimplemented, and runtime-inactive

## Artifact and Authority Model

The approved direction is one canonical projection per selected eligible activity plus one canonical monthly manifest. Five concerns remain separate:

1. immutable accepted owner authority and revocation artifacts;
2. an external authority registry that indexes and binds those artifacts without authenticating them;
3. consumer eligibility decisions that grant permission to use exact fields;
4. monthly selection decisions that identify permitted activities intended for publication;
5. generated projections and manifests that bind validated inputs without creating authority.

Eligibility means permission to use the exact calendar fields. Monthly selection means an externally authorized publication-intent decision. Selection grants no fields and cannot override missing, denied, revoked, or invalid eligibility.

Authority is purpose-typed and non-transferable: `calendar-eligibility`, `calendar-monthly-selection`, and `calendar-authority-revocation`. Each verification requires exact equality between the consuming contract's expected purpose, registry entry purpose, and externally verified artifact purpose. The registry is only an index and content-binding layer and cannot grant, broaden, self-authenticate, transfer, or revoke authority.

Each externally authorized decision defines a separate authorization-subject object containing exact owner-approved business content and excluding authority-reference metadata. Its `subject_sha256` is lowercase hexadecimal SHA-256 over RFC 8785 canonical UTF-8 bytes. Eligibility subjects bind the decision content and exact run, activity, and consumer; selection subjects bind the selection content and exact run, consumer, and month. Revocation subjects bind the original authority identifier, artifact digest, purpose, and exact scope.

## Eligibility Resolution

Eligibility decisions are immutable and append-only. Each decision has a stable `decision_id`, exact scope, positive version, and explicit predecessor or `null`. A root uses version 1; each successor uses its direct predecessor's version plus one.

- `eligible` grants only its exact `allowed_fields`;
- `denied` grants no fields;
- revocation is a new `denied` decision that supersedes the active decision;
- duplicate active tips, duplicate identity/version, missing predecessors, broken chains, cycles, or cross-run, cross-activity, or cross-consumer supersession fail closed;
- absent, malformed, unverifiable, denied, revoked, or unmatched authority fails closed;
- filename, timestamp, mtime, directory order, generation order, and file presence establish no precedence.

For `calendar-renderer`, the effective eligible decision must grant exactly this source-field set, with no subset or additional field:

1. `activity_id`
2. `activity_title`
3. `dates`
4. `time`

## Monthly Selection Resolution

Monthly selection decisions are immutable and append-only. Their exact scope is `run_id` + `consumer_id` + `programme_month`. A root uses `selection_version: 1` and `supersedes_selection_id: null`; each successor increments its direct predecessor's version by one and names that predecessor.

The effective selection is the unique active tip of one complete, externally verified, same-scope chain. Missing selection, duplicate active tips, duplicate identity/version, missing predecessors, broken chains, cycles, cross-scope supersession, or unverifiable authority fails closed.

`selected_activity_ids` is the complete intended publication set. It is unique and sorted lexicographically by Unicode code-point order. An empty set is permitted only through a valid, explicit selection containing `selected_activity_ids: []`.

Selection grants no fields, cannot create eligibility, cannot override denial or revocation, and cannot mutate evidence or `qa_status`. Filename, timestamp, mtime, directory order, generation order, file presence, and projection presence establish no selection or precedence.

## Projection Validation and Identity

For each selected activity, the projection must validate against the draft projection schema and satisfy all semantic bindings:

- projection `consumer_id` equals selection and manifest `consumer_id`;
- projection evidence `run_id` equals selection and manifest `run_id`;
- projection evidence `activity_id`, projection payload `activity_id`, and manifest entry `activity_id` are identical;
- provenance binds that same evidence record;
- eligibility resolves uniquely for the same run, activity, and consumer;
- eligibility grants exactly the calendar field set;
- `activity_title` is copied exactly to payload `title`;
- `dates` is copied completely and in source order without normalization, inference, reordering, flattening, truncation, or partial copying;
- `time` is copied exactly without normalization or inference;
- renderer payload excludes `source_reference`.

`payload_sha256` is SHA-256 over exact UTF-8 bytes produced by RFC 8785 JCS canonicalization of the renderer `payload` object only.

The projection identity-input object contains exactly:

- projection contract version;
- `consumer_id`;
- evidence `run_id` and `activity_id`;
- effective eligibility decision IDs in root-to-active-tip order;
- `payload_sha256`.

`projection_id` is `calproj_sha256_<lowercase-hex SHA-256>` over the RFC 8785 canonical bytes of that identity input. It excludes `projection_id`; no circular dependency exists. Missing, extra, reordered, or non-effective decision references, schema failure, hash mismatch, or identity mismatch fails closed.

## Manifest Assembly, Validation, and Identity

Manifest membership equals the effective monthly selection exactly. The builder must neither drop a selected activity nor add an unselected activity.

Every selected activity must have one valid projection and effective exact-field calendar eligibility. The whole manifest fails closed if any selected activity lacks eligibility or a projection; is denied or revoked; has mismatched scope, evidence, consumer, or identity; or fails schema, hash, provenance, or projection-ID validation.

Every referenced projection is revalidated. For each entry:

- manifest `projection_id` equals the recomputed projection ID;
- manifest `payload_sha256` equals the recomputed renderer-payload hash;
- projection consumer and run equal manifest consumer and run;
- evidence activity, payload activity, and entry activity are equal;
- the activity occurs in the effective selection;
- selection scope equals manifest scope.

Entries are sorted lexicographically by `activity_id` using Unicode code-point order. Duplicate entries fail closed.

The manifest binds:

- manifest contract version;
- effective `selection_id`;
- `selection_artifact_sha256`, computed over the RFC 8785 canonical UTF-8 bytes of the complete effective selection artifact;
- `builder_version`;
- `consumer_id`;
- `run_id`;
- `programme_month`;
- ordered manifest entries containing `activity_id`, `projection_id`, and `payload_sha256`.

`manifest_id` is `calmanifest_sha256_<lowercase-hex SHA-256>` over the RFC 8785 canonical bytes of exactly those identity inputs. It excludes `manifest_id`; no circular dependency exists.

The selection subject digest proves which selection content the owner authorized. The selection artifact digest proves which complete selection artifact the manifest consumed. Validation must reconstruct and verify both bindings.

## Non-Circular Construction Order

1. Construct the canonical authorization subject.
2. Compute its subject digest.
3. Produce and externally accept an authority artifact binding that digest.
4. Record or reference the authority artifact in the complete decision.
5. Compute the complete decision artifact digest where required.
6. Bind the complete selection artifact digest into the manifest.

No subject digest contains itself. No authority artifact digest is part of the subject it authorizes. No selection artifact digest contains itself. `manifest_id` excludes itself, and `projection_id` excludes itself.

`programme_month` is not derived by parsing `run_id`. A future implementation must verify the run/month relationship against authoritative run metadata. D1 does not currently expose a normative machine-readable programme-month field, so that dependency is blocking before implementation authorization.

### Explicit Empty Manifest

An empty manifest is valid only when the uniquely resolved, externally authorized selection has `selected_activity_ids: []`. It represents an authorized empty publication set.

An empty manifest must not result from missing or failed selection resolution, invalid projections, an empty directory, directory enumeration, or silently dropped activities.

## Storage Layout

```text
data/
├── authority/
│   ├── artifacts/<authority_id>.json
│   ├── revocations/<revocation_id>.json
│   └── registry/<registry_id>.json
├── consumer-eligibility/
│   └── calendar-renderer/decisions/<decision_id>.json
├── calendar-selections/
│   └── calendar-renderer/<run_id>/<programme_month>/<selection_id>.json
└── projections/
    └── calendar-renderer/<run_id>/
        ├── activities/<projection_id>.json
        └── manifests/<manifest_id>.json

examples/
└── contract-fixtures/calendar-only/{positive,negative}/
```

No runtime directory above is created by contract drafting. Authority, revocation, registry, eligibility, selection, projection, and manifest artifacts must remain outside `data/runs/`. Fictional fixtures must use obviously fictional identifiers and cannot grant authority.

## Lifecycle and Migration Gate

The architecture direction is accepted. Executable schemas remain draft `0.x` contracts and cannot become runtime-active before implementation validation, independent review, and explicit owner acceptance.

Existing approved-only newsletter behavior remains unchanged. It is newsletter-specific and is not universal consumer authorization.

## Remaining Blockers Before Implementation Authorization

- executable owner-authority artifact schema and verifier;
- executable revocation-artifact schema and verifier;
- bounded authoritative resolver-input mechanism;
- deterministic registry identity and publication mechanics;
- authoritative machine-readable run metadata binding `run_id` to `programme_month`;
- implementation validation;
- independent review;
- explicit owner schema and implementation acceptance.

No bounded-input or registry-publication model is selected by this draft.
