# monthly-agent

`monthly-agent` is a structured extraction and validation workflow for elderly centre monthly programme documents. It helps convert source programme material into reliable activity records for QA review and downstream newsletter generation.

The repository is organized around clear responsibilities: prompts guide agent behavior, schemas define data contracts, validators check objective issues, workflows document handoffs, and examples support regression testing.

## Project Overview

Monthly programme documents often contain dense tables, repeated dates, footnotes, registration rules, fee variations, and ambiguous source wording. This repository provides a repeatable workflow for turning those documents into structured JSON while preserving uncertainty instead of guessing.

Core outputs are activity records that can be compared with the original source, validated automatically, reviewed by humans where needed, and reused safely in participant-facing newsletter content.

## Problem This Project Solves

Manual newsletter preparation from monthly programme documents is error-prone. A small mistake in date, time, venue, fee, quota, eligibility, or registration period can mislead participants.

This project reduces that risk by:

- Separating extraction, validation, QA, and human review.
- Keeping every activity record traceable to source evidence.
- Treating unclear source information as uncertainty, not a gap to fill by inference.
- Providing regression tests and examples for prompt, schema, and validator changes.

## Architecture

```text
Monthly Programme Document
        |
        v
Extract Agent
        |
        v
Structured JSON
        |
        v
Schema Validator
        |
        v
Business Rule Validator
        |
        v
QA Review
        |
        v
Human Review
        |
        v
Newsletter Generation
```

The architecture has three layers:

- **Agent layer**: extraction and QA prompts guide source-faithful AI work.
- **Contract layer**: JSON schema and output contracts define expected structure and validator behavior.
- **Validation layer**: automated checks catch malformed records and objective workflow issues before QA or publication.

Human review remains part of the architecture because source documents can be incomplete, visually ambiguous, or internally inconsistent.

## Current Status

| Milestone | Status |
|-----------|--------|
| Foundation | Complete |
| Validation Engine | Complete |
| Business Rule Engine | In progress |
| QA Engine | Planned |
| Newsletter Generation | Planned |

## Quick Start

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run tests:

```powershell
python -m pytest
```

Validate a sample extraction:

```powershell
python tools/validate_schema.py examples/sample-output.json
```

Source files should be stored under `data/input/`. Generated extraction and QA outputs should be stored under `data/output/`.

## Repository Structure

```text
.
|-- data/          # Source inputs and generated outputs
|-- docs/          # Project planning, decisions, and contracts
|-- examples/      # Representative source, output, and QA examples
|-- prompts/       # Extract and QA agent prompts
|-- rules/         # Business rule specifications
|-- schemas/       # JSON schemas
|-- tests/         # Regression tests
|-- tools/         # Validation command-line tools
|-- validators/    # Validator implementation modules
`-- workflows/     # Extraction and QA workflow documentation
```

## Development Workflow

Development uses a multi-AI pipeline with automated regression testing:

```text
Architecture and integration review
        |
        v
ChatGPT
        |
        v
Implementation
        |
        v
Codex
        |
        v
Code review and edge-case review
        |
        v
Claude
        |
        v
Regression testing
        |
        v
pytest
        |
        v
Commit
        |
        v
Git
```

Typical change flow:

1. Update the smallest relevant prompt, schema, validator, test, or document.
2. Validate at least one representative extracted output.
3. Run `python -m pytest`.
4. Review failures for both technical regressions and source-meaning risks.
5. Check `git status --short` before committing.

Changes should preserve source meaning. Missing or unclear programme details should be flagged for QA or Human Review rather than invented.

## Design Principles

- Source-first extraction and review.
- Validation before publication.
- Explicit uncertainty instead of guessing.
- Small, independently testable components.
- Regression tests before commit.

## Roadmap

- Complete the Business Rule Engine and align it with `rules/`.
- Add broader regression coverage for realistic monthly programme formats.
- Expand representative sample inputs and expected outputs.
- Add newsletter generation prompts and templates.
- Improve end-to-end handoff documentation from extraction through publication.

## Key Project Documents

- `AGENTS.md`: operating instructions for human developers and AI assistants.
- `docs/project-plan.md`: project goals, scope, and planned enhancements.
- `docs/output-contracts.md`: validator output and exit-code contracts.
- `workflows/extract-workflow.md`: end-to-end extraction workflow.
- `workflows/qa-workflow.md`: QA workflow and review severity model.
- `prompts/extract-activity-info.md`: Extract Agent prompt.
- `prompts/qa-check-monthly-info.md`: QA Agent prompt.
- `schemas/activity.schema.json`: structured activity record contract.
- `rules/README.md`: business rule index.
