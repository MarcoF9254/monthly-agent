import re

from validators.business_rules.helpers import is_meaningful_string, is_uncertain


RULE_ID = "BR-005"
RECOMMENDATION = (
    "Update source_reference with deterministic traceability information such as "
    "page + row, table + row, item number, activity number, exact activity title, "
    "or exact category."
)

PAGE_PATTERN = re.compile(r"(?:\bpage\s*\d+\b|\bpg\.?\s*\d+\b|第\s*\d+\s*頁)", re.IGNORECASE)
TABLE_PATTERN = re.compile(r"(?:\btable\s*[A-Za-z0-9-]*\b|表\s*[A-Za-z0-9-]*)", re.IGNORECASE)
ROW_PATTERN = re.compile(r"(?:\brow\s*\d+\b|第\s*\d+\s*行)", re.IGNORECASE)
ITEM_NUMBER_PATTERN = re.compile(
    r"(?:\bitem\s*(?:no\.?|number)?\s*\d+\b|\bitem\s*#\s*\d+\b|項目\s*(?:編號)?\s*\d+)",
    re.IGNORECASE,
)
ACTIVITY_NUMBER_PATTERN = re.compile(
    r"(?:\bactivity\s*(?:no\.?|number)?\s*\d+\b|\bactivity\s*#\s*\d+\b|活動\s*(?:編號)?\s*\d+)",
    re.IGNORECASE,
)


def _activity_id(record) -> str:
    if isinstance(record, dict):
        return record.get("activity_id", "<missing>")
    return "<missing>"


def _finding(record, index: int) -> dict:
    return {
        "index": index,
        "activity_id": _activity_id(record),
        "rule_id": RULE_ID,
        "field": "source_reference",
        "path": "source_reference",
        "severity": "medium",
        "message": "Source reference has no BR-005 v1 deterministic traceability anchor.",
        "recommendation": RECOMMENDATION,
    }


def _source_reference_segments(source_reference: str) -> list[str]:
    return [
        segment.strip()
        for segment in re.split(r"[,，;；|\n]", source_reference)
        if segment.strip()
    ]


def _contains_exact_anchor(source_reference: str, anchor) -> bool:
    if not is_meaningful_string(anchor):
        return False

    normalized_anchor = anchor.strip()
    if source_reference == normalized_anchor:
        return True

    return normalized_anchor in _source_reference_segments(source_reference)


def _contains_labeled_exact_anchor(
    source_reference: str, label_pattern: str, anchor
) -> bool:
    if not is_meaningful_string(anchor):
        return False

    match = re.search(label_pattern, source_reference, re.IGNORECASE)
    if match is None:
        return False

    return match.group(1).strip() == anchor.strip()


def _has_structured_locator(source_reference: str) -> bool:
    has_page_row = bool(PAGE_PATTERN.search(source_reference)) and bool(
        ROW_PATTERN.search(source_reference)
    )
    has_table_row = bool(TABLE_PATTERN.search(source_reference)) and bool(
        ROW_PATTERN.search(source_reference)
    )
    return (
        has_page_row
        or has_table_row
        or bool(ITEM_NUMBER_PATTERN.search(source_reference))
        or bool(ACTIVITY_NUMBER_PATTERN.search(source_reference))
    )


def check(record, index: int = 0) -> list:
    if not isinstance(record, dict):
        return []

    uncertain_fields = record.get("uncertain_fields")
    if is_uncertain("source_reference", uncertain_fields):
        return []

    source_reference = record.get("source_reference")
    if not is_meaningful_string(source_reference):
        return []

    source_reference = source_reference.strip()
    if _contains_exact_anchor(source_reference, record.get("activity_title")):
        return []
    if _contains_exact_anchor(source_reference, record.get("category")):
        return []
    if _contains_labeled_exact_anchor(
        source_reference, r"\bactivity\s+title\s*:\s*(.+)\s*$", record.get("activity_title")
    ):
        return []
    if _contains_labeled_exact_anchor(
        source_reference, r"\bcategory\s*:\s*(.+)\s*$", record.get("category")
    ):
        return []
    if _has_structured_locator(source_reference):
        return []

    return [_finding(record, index)]
