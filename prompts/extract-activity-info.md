# Extract Activity Information

You are extracting activity information from an elderly centre monthly programme document.

## Task

Read the provided source text and extract every programme activity as structured data. Preserve the source meaning exactly. Do not infer missing details unless the source clearly supports the inference.

## Output Format

Return a JSON array. Every item must validate against `schemas/activity.schema.json`.

```json
{
  "activity_id": "",
  "activity_title": "",
  "category": "",
  "description": "",
  "dates": [
    {
      "date_text": "",
      "start_date": "",
      "end_date": "",
      "recurrence": ""
    }
  ],
  "time": "",
  "venue": "",
  "target_participants": "",
  "fee": [
    {
      "fee_type": "",
      "amount_text": "",
      "currency": "",
      "amount": null,
      "notes": ""
    }
  ],
  "quota": "",
  "registration_method": "",
  "registration_period": "",
  "staff_in_charge": "",
  "notes": "",
  "source_reference": "",
  "uncertain_fields": [],
  "qa_status": "pending"
}
```

## Rules

- Extract all activities, including one-off events, recurring classes, talks, workshops, outings, services, and enrolment notices.
- Keep original wording for names, dates, times, fees, and venues when possible.
- If a field is not present, use an empty string and add the field name to `uncertain_fields`.
- Use `dates` as an array, even when there is only one date. Keep multiple dates or date ranges as separate array items when the source lists them separately.
- Use `fee` as an array, even when there is only one fee. Create separate fee entries for member fees, non-member fees, material fees, deposits, concessions, or other distinct fee types.
- Set `qa_status` to `pending` for newly extracted records.
- If multiple dates or sessions belong to one activity, keep them together only when the source clearly presents them as one activity.
- Include a source reference such as page number, section heading, table row, or nearby text when available.
- Do not include commentary outside the JSON output.

