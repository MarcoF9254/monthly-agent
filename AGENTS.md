# AGENTS.md

## Project Purpose

This repository supports an agent workflow for elderly centre monthly programme documents. The primary goal is to extract activity information accurately, validate it, and prepare structured data for downstream monthly newsletter generation.

## Agent Guidelines

- Preserve source meaning. Do not invent activity names, dates, times, fees, venues, quotas, or eligibility details.
- Treat missing or unclear source information as unknown and flag it for QA.
- Keep extraction output structured, consistent, and easy to compare with the original document.
- Prefer small, auditable changes to prompts and documentation.
- Store raw inputs under `data/input/` and generated outputs under `data/output/`.

## Expected Data Fields

- Activity title
- Date or date range
- Time
- Venue
- Target participants or eligibility
- Fee
- Quota
- Registration method or deadline
- Organizer or responsible team
- Notes and special requirements
- Source reference
- QA status

## Verification

When changing prompts or extraction logic, test with at least one representative monthly programme document and check that uncertain fields are explicitly flagged.
