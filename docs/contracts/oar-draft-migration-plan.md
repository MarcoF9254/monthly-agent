# OAR Inactive Draft Migration Plan

Status: authorized drafting only; no executable acceptance or activation

| Old draft | New draft | Breaking migration |
| --- | --- | --- |
| `scoped-eligibility-decision/0.2.0-draft` | `calendar-eligibility-subject/0.3.0-draft` | Explicit subject path; remove embedded authority metadata |
| `calendar-monthly-selection/0.2.0-draft` | `calendar-monthly-selection-subject/0.3.0-draft` | Explicit subject path; remove authority and artifact bindings |
| `authoritative-run-metadata/0.1.0-draft` | `run-metadata-binding-subject/0.2.0-draft` | Explicit subject path; generic envelope |
| `registry-publication-authority/0.1.0-draft` | publication subject plus generic envelope | Split subject from bootstrap authority |
| snapshot `0.1.0-draft` | snapshot `0.2.0-draft` | Ordinary envelope membership; separate bootstrap references |
| bundle `0.1.0-draft` | bundle `0.2.0-draft` | Explicit subject/envelope inventory |

Breaking inactive-draft migration needs no runtime backward compatibility. Semantic intent and provenance remain explicit.

The inactive external-authority-registry contract and schema remain unchanged and are not the Gate 2 anchored closed-world source.

Projection and manifest contracts, schemas, and fixtures remain unchanged. A future separately authorized provenance migration may replace their legacy references; this note is non-normative.
