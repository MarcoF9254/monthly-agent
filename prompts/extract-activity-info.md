# Extract Activity Information

You are extracting activity information from an elderly centre monthly programme document.

## Task

Read the provided source text and extract every programme activity as structured data. Preserve the source meaning exactly. Do not infer missing details unless the source clearly supports the inference.

## Output Format

Return a JSON array. Each item should use these fields:

```json
{
  "activity_title": "",
  "date": "",
  "time": "",
  "venue": "",
  "target_participants": "",
  "fee": "",
  "quota": "",
  "registration": "",
  "organizer": "",
  "notes": "",
  "source_reference": "",
  "uncertain_fields": []
}
```

## Rules

- Extract all activities, including one-off events, recurring classes, talks, workshops, outings, services, and enrolment notices.
- Keep original wording for names, dates, times, fees, and venues when possible.
- If a field is not present, use an empty string and add the field name to `uncertain_fields`.
- If multiple dates or sessions belong to one activity, keep them together only when the source clearly presents them as one activity.
- Include a source reference such as page number, section heading, table row, or nearby text when available.
- Do not include commentary outside the JSON output.
