# Pipeline Run Contract

## Purpose

This document defines D1, the repository contract for recording one auditable monthly programme pipeline run. It standardizes run identifiers, artifact locations, stage boundaries, status ownership, and closure outcomes.

D1 is a contract, not a runner. It does not prescribe orchestration commands, implement stage execution, or change validator behavior.

## Run Identifier

Each run uses a `run_id` in this format:

```text
YYYY-MM-rNN
```

- `YYYY-MM` identifies the programme month.
- `rNN` is a zero-padded run sequence for that month, starting with `r01`.
- A `run_id` must uniquely identify one run directory. Existing run directories must not be overwritten to reuse an identifier.

Example: `2026-07-r01`.

## Required Run Layout

Each run lives under `data/runs/<run_id>/` and uses this layout:

```text
data/runs/<run_id>/
├── source/
│   ├── source_manifest.json
│   └── originals/
├── extraction/
│   └── extracted_activity_records.json
├── validation/
│   ├── schema_validation.txt
│   └── business_validation.txt
├── qa/
│   └── qa_review_notes.md
├── human-review/
│   └── human_review_decisions.md
├── approval/
│   ├── approved_records.json
│   ├── blocked_records.md
│   └── blocked_run_summary.md
└── run_summary.md
```

The layout shows every recognized path, but approval artifacts are conditional. The following artifacts are required for every run:

- `source/source_manifest.json`
- `extraction/extracted_activity_records.json`
- `validation/schema_validation.txt`
- `validation/business_validation.txt`
- `qa/qa_review_notes.md`
- `human-review/human_review_decisions.md`
- `run_summary.md`

Approval artifacts are required only when applicable:

- `approval/approved_records.json` for `approved` or `partially_approved` runs
- `approval/blocked_records.md` for `partially_approved` or `blocked` runs
- `approval/blocked_run_summary.md` for `blocked` runs or runs with unresolved run-level issues

Do not create empty approval artifacts merely to fill the directory layout. `run_summary.md` must state which approval artifacts apply to the run and which are present.

## Artifact Commit Policy

Run artifacts under `data/runs/<run_id>/` are commit-eligible so a completed run can be reviewed and audited in repository history. Whether a particular run is committed remains an explicit review decision; D1 does not require automatic commits.

The only path-level non-commit exception is `data/runs/*/source/originals/*`. Original source documents may contain sensitive or unsuitable binary material and must not be committed. A `.gitkeep` file may be committed at `data/runs/<run_id>/source/originals/.gitkeep` to retain the directory.

`source/source_manifest.json` must identify the selected source material and preserve traceability without requiring original source files to be committed.

## Pipeline Stages

### 1. Source Selection

Select the authoritative monthly programme source set and record it in `source/source_manifest.json`. Missing, conflicting, or unreadable sources are run-level issues when they prevent a trustworthy extraction scope.

### 2. Extraction

Extract activity records according to `prompts/extract-activity-info.md` and `schemas/activity.schema.json`. Write the complete run batch to `extraction/extracted_activity_records.json`. Preserve source meaning and flag missing or unclear information rather than inventing it.

### 3. Schema Validation

Validate the extracted batch against `schemas/activity.schema.json`. Record the human-readable result in `validation/schema_validation.txt`. Schema validation reports structural problems and does not mutate records.

### 4. Business Rule Validation

Run the active business-rule registry and record the human-readable result in `validation/business_validation.txt`. Business validation is deterministic, reports findings, and does not mutate records. BR-006 remains outside the active registry.

### 5. GPT QA

Compare every extracted record with source evidence using `prompts/qa-check-monthly-info.md`. Record review evidence, missing activities, duplicates, unsupported inferences, and severity in `qa/qa_review_notes.md`. Route unresolved source-dependent questions to Human Review.

### 6. Human Review

Resolve or explicitly retain issues that cannot be decided confidently by extraction, validation, or GPT QA. Record decisions and supporting evidence in `human-review/human_review_decisions.md`. Unresolved decisions remain visible and prevent affected records from being treated as approved.

### 7. Approval / Run Closure

Determine the run outcome, write only the applicable approval artifacts, and summarize the run in `run_summary.md`. Closure must account for every extracted record and every unresolved run-level issue.

## Failure Boundaries

A per-record failure affects one identifiable activity record. Examples include a schema violation, a business-rule finding, unsupported activity details, or unresolved uncertainty for that record. Other records may continue through QA and approval when their evidence and validation are complete.

A per-run failure affects the integrity or execution of the run as a whole. Examples include an unreadable required source, an incomplete source manifest, invalid batch JSON that prevents record enumeration, a validation tool execution error, or uncertainty about whether the activity set is complete. A run-level failure blocks closure as `approved` until resolved.

Record-level findings must not be promoted to run-level failures merely because they exist. Run-level failures must not be hidden by approving unaffected records; they remain explicit in `run_summary.md` and, when unresolved, `approval/blocked_run_summary.md`.

## Mutation Ownership

- Extraction owns the initial record creation. New records use `qa_status: "pending"`, and extraction adds `uncertain_fields` markers for source information that is missing, unclear, or ambiguous.
- Schema Validation and Business Rule Validation are read-only. They report findings and never mutate `qa_status`, `uncertain_fields`, or participant-facing fields.
- GPT QA may update `qa_status` and `uncertain_fields` when the update is supported by recorded source evidence. It must not clear uncertainty or approve a record without support.
- Human Review owns decisions for escalated ambiguity or conflict and may update `qa_status`, `uncertain_fields`, and corrected record fields when its decision cites source evidence.
- Approval / Run Closure selects and summarizes records; it does not silently repair or reclassify them.

Every mutation after extraction must remain traceable through `qa/qa_review_notes.md` or `human-review/human_review_decisions.md`.

## `qa_status` Mapping

`qa_status` remains anchored to the enum in `schemas/activity.schema.json`:

- `pending`: the record is newly extracted or has not completed the required QA review.
- `approved`: key fields are source-supported and no unresolved issue prevents downstream use.
- `needs_review`: source ambiguity, conflict, missing evidence, or another unresolved issue requires Human Review.
- `rejected`: the record must not proceed because review determined it is unsupported, out of scope, duplicated without a valid retained instance, or otherwise unsuitable for approval.

These values describe record workflow state. They are not run outcomes.

Human Review decision concepts are separate from the schema enum. Decisions such as correcting a value, accepting source evidence, retaining an uncertainty, treating entries as duplicates, or declining an activity are recorded as review decisions first; the reviewer then maps the resulting record state to one of the four allowed `qa_status` values. Decision labels must not be written into `qa_status`.

## Run Outcomes

- `approved`: all records included for downstream use have `qa_status: "approved"`, no records remain blocked, and no unresolved run-level issue remains.
- `partially_approved`: at least one record is approved and at least one record is withheld because it is `needs_review`, `rejected`, or otherwise unresolved.
- `blocked`: no reliable approval set can be released, or an unresolved run-level issue prevents approval closure.

Run outcomes do not extend the `qa_status` enum and must be recorded in `run_summary.md`.

## Approval Artifact Coexistence

For an `approved` run, `approval/approved_records.json` is present and blocked artifacts are absent. A run with an unresolved run-level issue cannot use the `approved` outcome.

For a `partially_approved` run, `approval/approved_records.json` and `approval/blocked_records.md` coexist. Add `approval/blocked_run_summary.md` only when an unresolved run-level issue also exists.

For a `blocked` run, `approval/blocked_records.md` and `approval/blocked_run_summary.md` are present. `approval/approved_records.json` is absent because a blocked run releases no approval set.

## Forward Compatibility

D1 reserves stable stage directories and artifact boundaries so D2 can later define a machine-readable Findings Contract without reorganizing existing runs. D1 does not define the D2 JSON filename, schema, fields, or serialization rules. Existing `.txt` validation artifacts remain required until a later accepted contract explicitly changes them.

## Scope Guardrails

- Do not implement a pipeline runner as part of D1.
- Do not define D2 machine-readable findings JSON as part of D1.
- Do not activate BR-006. Its implementation and direct tests remain retained while runtime activation is held.
- Do not change validators, the active business-rule registry, schemas, or runtime output contracts to satisfy this document.
