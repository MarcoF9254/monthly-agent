from validators.business_rules.helpers import finding, is_meaningful_string, is_uncertain


RULE_ID = "BR-001"
RECOMMENDATION = (
    "Check the source document. Add the missing value if present, or list this field "
    "in uncertain_fields if the source is unclear."
)

HIGH_SEVERITY_FIELDS = {
    "activity_title",
    "dates",
    "time",
    "venue",
    "target_participants",
    "fee",
    "quota",
    "registration_method",
    "registration_period",
}

REQUIRED_FIELDS = [
    "activity_title",
    "dates",
    "time",
    "venue",
    "target_participants",
    "fee",
    "quota",
    "registration_method",
    "registration_period",
    "source_reference",
]


def _severity(field: str) -> str:
    if field in HIGH_SEVERITY_FIELDS:
        return "high"
    return "medium"


def _finding(record, index: int, field: str, path: str) -> dict:
    return finding(
        record,
        index,
        RULE_ID,
        field,
        path,
        _severity(field),
        f"Required field '{field}' is missing, empty, or not meaningful.",
        RECOMMENDATION,
    )


def _dates_path(value) -> str:
    if not isinstance(value, list) or not value:
        return "dates"
    return "dates[].date_text"


def _fee_path(value) -> str:
    if not isinstance(value, list) or not value:
        return "fee"
    return "fee[].amount_text"


def _has_meaningful_date(value) -> bool:
    if not isinstance(value, list) or not value:
        return False
    return any(
        isinstance(item, dict) and is_meaningful_string(item.get("date_text"))
        for item in value
    )


def _has_meaningful_fee(value) -> bool:
    if not isinstance(value, list) or not value:
        return False
    return any(
        isinstance(item, dict) and is_meaningful_string(item.get("amount_text"))
        for item in value
    )


def _field_is_meaningful(record: dict, field: str) -> bool:
    value = record.get(field)
    if field == "dates":
        return _has_meaningful_date(value)
    if field == "fee":
        return _has_meaningful_fee(value)
    return is_meaningful_string(value)


def _path_for(record: dict, field: str) -> str:
    value = record.get(field)
    if field == "dates":
        return _dates_path(value)
    if field == "fee":
        return _fee_path(value)
    return field


def check(record, index: int = 0) -> list:
    if not isinstance(record, dict):
        return [_finding({}, index, field, field) for field in REQUIRED_FIELDS]

    uncertain_fields = record.get("uncertain_fields")
    findings = []
    for field in REQUIRED_FIELDS:
        if is_uncertain(field, uncertain_fields):
            continue
        if not _field_is_meaningful(record, field):
            findings.append(_finding(record, index, field, _path_for(record, field)))
    return findings
