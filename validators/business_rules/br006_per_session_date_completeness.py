from validators.business_rules.helpers import finding, is_meaningful_string, is_uncertain


RULE_ID = "BR-006"
FIELD = "dates"
SEVERITY = "high"
MESSAGE_TEMPLATE = "Session date is missing for {path}."
RECOMMENDATION = (
    "Fill in the session date from source evidence or mark the exact per-session "
    "date field as uncertain for QA / Human Review."
)


def _date_text_for(item):
    if isinstance(item, dict):
        return item.get("date_text")
    return None


def _finding(record: dict, index: int, path: str) -> dict:
    return finding(
        record,
        index,
        RULE_ID,
        FIELD,
        path,
        SEVERITY,
        MESSAGE_TEMPLATE.format(path=path),
        RECOMMENDATION,
    )


def check(record, index: int = 0) -> list:
    if not isinstance(record, dict):
        return []

    dates = record.get("dates")
    if not isinstance(dates, list) or not dates:
        return []

    uncertain_fields = record.get("uncertain_fields")
    findings = []
    for item_index, item in enumerate(dates):
        path = f"dates[{item_index}].date_text"
        if is_meaningful_string(_date_text_for(item)) or is_uncertain(path, uncertain_fields):
            continue
        findings.append(_finding(record, index, path))
    return findings
