# BR-005 Source Reference

## Rule ID

BR-005

## Rule Name

Source reference must be structurally traceable.

## Purpose

Ensure QA and Human Review can trace each extracted record back to the original monthly programme source using deterministic source-reference structure.

BR-005 is a structural and deterministic traceability validation rule. It checks whether a non-empty `source_reference` contains record-specific traceability evidence that can be evaluated without interpreting source-document meaning.

BR-005 must not use semantic, NLP, fuzzy, or judgement-based checks for whether a reference is "specific enough", "too vague", similar to the activity, or likely to identify the correct activity.

## Applies to Fields

- `source_reference`
- `activity_title`
- `category`

## Validation Scope

BR-005 applies only when `source_reference` is non-empty.

Empty, missing, placeholder, or non-meaningful `source_reference` values are covered by BR-001 and must not be re-checked by BR-005.

BR-005 does not confirm that the referenced source text truly matches the extracted activity. That comparison belongs to QA or Human Review.

## Deterministic Traceability Inputs

BR-005 v1 keeps anchors limited to values that can be validated from a single record without source-document context:

- A deterministic locator with enough structure, such as page + row, table + row, item number, or activity number.
- The exact `activity_title` value from the record.
- The exact `category` value from the record.

`activity_title` and `category` are used only as exact structural anchors. BR-005 may check whether the exact non-empty `activity_title` or exact non-empty `category` appears in `source_reference`.

BR-005 must not infer that a paraphrase, translation, abbreviation, synonym, nearby topic, or partial fuzzy match is equivalent to `activity_title` or `category`.

## Pass Condition

A record passes when non-empty `source_reference` contains at least one BR-005 v1 deterministic traceability anchor listed above.

Bare page-only or section-only references do not pass unless combined with another deterministic anchor such as row, item number, activity number, exact `activity_title`, or exact `category`.

## Fail Condition

A record fails when non-empty `source_reference` contains no deterministic traceability anchor and is only a generic document-level reference.

Examples of generic document-level references include values such as `"monthly programme"`, `"programme leaflet"`, `"source document"`, or `"newsletter"` when no deterministic locator, exact title, or exact category is included.

## Severity

Medium by default.

High only if the non-empty but structurally untraceable `source_reference` prevents verification of participant-facing details and no other deterministic source locator is available.

## Finding Field Guidance

Findings always report `field: "source_reference"` and `path: "source_reference"`.

Do not report BR-005 findings against `activity_title` or `category`. Those fields are used only as optional exact-match anchors for evaluating `source_reference`.

## Example Pass

`source_reference` is `"Page 3, table row 5"`.

`source_reference` is `"Activity title: Tai Chi Class"` and `activity_title` is `"Tai Chi Class"`.

`source_reference` is `"Category: Health Talks"` and `category` is `"Health Talks"`.

## Example Fail

`source_reference` is `"monthly programme"`.

`source_reference` is `"programme leaflet"`.

`source_reference` is `"source document"`.

`source_reference` is `"newsletter"`.

These fail only when the value is non-empty and contains no BR-005 v1 deterministic locator, exact `activity_title`, or exact `category`.

## Boundary Examples

`source_reference: "monthly programme, page 2, row 5"` passes because it includes page and row locators.

`source_reference: "monthly programme, page 2"` fails because a bare page-only reference is not enough structure for BR-005 v1. The validator must not decide whether page 2 contains one or multiple activities.

`source_reference: "monthly programme"` fails because it is only a generic document-level reference.

`source_reference: "Tai Chi"` does not pass as an `activity_title` anchor for `activity_title: "Tai Chi Class"` because partial or fuzzy title matching is outside BR-005 scope.

`source_reference: "Tai Chi Class"` passes as an exact `activity_title` anchor for `activity_title: "Tai Chi Class"`.

An empty `source_reference` is not a BR-005 failure. It is handled by BR-001.

## Human Review Guidance

If BR-005 fires, update `source_reference` with deterministic traceability information such as page + row, table + row, item number, activity number, exact activity title, or exact category.

If the record cannot be traced to the source, treat it as unsupported during QA or Human Review.
