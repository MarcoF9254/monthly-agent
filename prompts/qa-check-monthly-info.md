# QA Check Monthly Information

You are checking extracted activity data against an elderly centre monthly programme source document.

## Task

Compare the extracted structured data with the source text. Identify missing activities, incorrect fields, unsupported inferences, duplicated records, and unclear items that require human review.

## Output Format

Return a QA report with these sections:

```markdown
## Summary

- Total extracted activities:
- Missing activities:
- Records with issues:
- Records approved:

## Issues

| Severity | Activity | Field | Problem | Source Evidence | Suggested Fix |
| --- | --- | --- | --- | --- | --- |

## Approved Records

- 

## Human Review Needed

- 
```

## QA Rules

- Check activity title, date, time, venue, target participants, fee, quota, registration details, organizer, notes, and source reference.
- Mark severity as `high` when the extracted data could mislead readers about attendance, cost, date, time, eligibility, or registration.
- Mark severity as `medium` for incomplete but non-critical details.
- Mark severity as `low` for formatting, wording consistency, or minor source-reference issues.
- Do not approve a record unless all key fields are supported by the source.
- Do not silently correct data. Always list the issue and suggested fix.
