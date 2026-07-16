# Authoritative Run Metadata Binding Contract Draft

Status: `authoritative-run-metadata/0.1.0-draft`; inactive, fictional-only, unimplemented, and not accepted as executable

Schema: `schemas/drafts/bounded-authority-input/authoritative-run-metadata.schema.json`

The contract binds opaque `run_id` to exact `programme_month` for one consumer. A resolver must never parse, infer, normalize, or reconstruct programme month from `run_id`.

Exact equality is required among authoritative run metadata, registry snapshot, monthly selection, and future monthly manifest. Missing metadata, conflicting metadata, consumer mismatch, or month mismatch fails closed before projection or manifest readiness.

The committed fixture is explicitly fictional. Real run-metadata authority, issuance, trust, lifecycle, and publication remain unresolved owner decisions and blockers before real registry publication or implementation authorization.
