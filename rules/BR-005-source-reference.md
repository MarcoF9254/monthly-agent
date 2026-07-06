# BR-005 Source Reference

## Rule ID

BR-005

## Rule Name

Extracted records must include traceable source references.

## Purpose

Ensure QA and Human Review can trace each extracted record back to the original monthly programme source.

## Applies to Fields

- `source_reference`
- `activity_title`
- `category`

## Pass Condition

`source_reference` is present and specific enough to locate the activity in the source, such as a page number, section heading, table row, activity title, or nearby source text.

## Fail Condition

`source_reference` is empty, generic, or too vague to support QA tracing.

## Severity

Medium by default. High if the missing source reference prevents verification of participant-facing details.

## Example Pass

`source_reference` is `"手作活動，母親節花藝工作坊"`.

## Example Fail

`source_reference` is `"monthly programme"` or an empty string.

## Human Review Guidance

Locate the activity in the original source and update `source_reference` with enough detail for another reviewer to find it quickly. If the record cannot be traced to the source, treat it as unsupported.
