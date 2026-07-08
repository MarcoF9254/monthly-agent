from validators.business_rules.helpers import finding

RULE_ID = "BR-004"
RECOMMENDATION = (
    "Reset premature status to pending during pre-QA validation. Do not approve "
    "records until QA or Human Review has completed."
)


def _has_uncertainty(record: dict) -> bool:
    uncertain_fields = record.get("uncertain_fields")
    return isinstance(uncertain_fields, list) and bool(uncertain_fields)


def _finding(
    record,
    index: int,
    field: str,
    path: str,
    severity: str,
    message: str,
) -> dict:
    return finding(
        record,
        index,
        RULE_ID,
        field,
        path,
        severity,
        message,
        RECOMMENDATION,
    )


def check(record, index: int = 0) -> list:
    if not isinstance(record, dict):
        return []

    qa_status = record.get("qa_status")
    if qa_status == "pending":
        return []

    if qa_status == "approved" and _has_uncertainty(record):
        return [
            _finding(
                record,
                index,
                "uncertain_fields",
                "uncertain_fields",
                "high",
                "Record is approved while uncertain_fields is non-empty at the pre-QA stage.",
            )
        ]

    if qa_status == "approved":
        return [
            _finding(
                record,
                index,
                "qa_status",
                "qa_status",
                "high",
                "Record is approved at the pre-QA stage.",
            )
        ]

    if qa_status in {"needs_review", "rejected"}:
        return [
            _finding(
                record,
                index,
                "qa_status",
                "qa_status",
                "medium",
                f"Record has qa_status '{qa_status}' at the pre-QA stage.",
            )
        ]

    return []
