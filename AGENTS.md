# AGENTS.md

## Project Purpose

This repository supports an agent workflow for elderly centre monthly programme documents. The primary goal is to extract activity information accurately, validate it, and prepare structured data for downstream monthly newsletter generation.

## Agent Guidelines

- Preserve source meaning. Do not invent activity names, dates, times, fees, venues, quotas, or eligibility details.
- Treat missing or unclear source information as unknown and flag it for QA.
- Keep extraction output structured, consistent, and easy to compare with the original document.
- Prefer small, auditable changes to prompts and documentation.
- Store raw inputs under `data/input/` and generated outputs under `data/output/`.

## Extract Agent

The Extract Agent reads elderly centre monthly programme documents and converts each activity into structured data.

- Use `prompts/extract-activity-info.md`.
- Output records that follow `schemas/activity.schema.json`.
- Preserve source wording for titles, dates, times, venues, fees, and registration details when possible.
- Support multiple dates and multiple fee types.
- Set new records to `qa_status: "pending"`.
- Add missing, unclear, or ambiguous fields to `uncertain_fields`.

## QA Agent

The QA Agent compares extracted records with the original source document.

- Use `prompts/qa-check-monthly-info.md`.
- Check every field against source evidence.
- Identify missing activities, duplicates, unsupported inferences, and incorrect values.
- Mark records as approved only when key fields are source-supported.
- Flag misleading date, time, fee, venue, eligibility, or registration errors as high severity.

## Human Review

Human Review resolves items that cannot be confidently handled by extraction or QA alone.

- Review records with unclear source text or conflicting information.
- Decide how to handle missing dates, fees, quotas, or registration details.
- Confirm source references for ambiguous table rows, captions, or footnotes.
- Update records after review and change `qa_status` as appropriate.

## Newsletter Agent

The Newsletter Agent uses approved structured records to prepare monthly newsletter content.

- Use only records with `qa_status: "approved"` unless explicitly instructed otherwise.
- Keep participant-facing wording accurate and clear.
- Do not publish uncertain or unresolved details.
- Preserve practical details such as date, time, venue, fee, eligibility, quota, and registration period.

## Verification

When changing prompts or extraction logic, test with at least one representative monthly programme document and check that uncertain fields are explicitly flagged.
