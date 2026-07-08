from validators.business_rules.helpers import (
    finding,
    is_free_indicator,
    is_meaningful_string,
    is_uncertain,
)


RULE_ID = "BR-002"
RECOMMENDATION = (
    "Check the source document. Confirm the fee text, or list fee in "
    "uncertain_fields if the source is unclear."
)


def _finding(record, index: int, field: str, path: str, message: str) -> dict:
    return finding(
        record,
        index,
        RULE_ID,
        field,
        path,
        "high",
        message,
        RECOMMENDATION,
    )


def _amount_for(item):
    if isinstance(item, dict):
        return item.get("amount")
    return None


def _amount_text_for(item):
    if isinstance(item, dict):
        return item.get("amount_text")
    return None


def _check_fee_item(record: dict, index: int, item, item_index: int) -> dict | None:
    amount = _amount_for(item)
    amount_text = _amount_text_for(item)
    uncertain_fields = record.get("uncertain_fields")
    fee_uncertain = is_uncertain("fee", uncertain_fields)

    if amount is None:
        if is_free_indicator(amount_text) or fee_uncertain:
            return None
        return _finding(
            record,
            index,
            "fee[].amount",
            f"fee[{item_index}].amount",
            "Fee is unclear and is neither marked as uncertain nor identified as free.",
        )

    if is_meaningful_string(amount_text) or fee_uncertain:
        return None

    return _finding(
        record,
        index,
        "fee[].amount_text",
        f"fee[{item_index}].amount_text",
        "Fee has a normalized amount but no meaningful source text.",
    )


def check(record, index: int = 0) -> list:
    if not isinstance(record, dict):
        return []

    fee = record.get("fee")
    if not isinstance(fee, list):
        return []

    findings = []
    for item_index, item in enumerate(fee):
        finding = _check_fee_item(record, index, item, item_index)
        if finding is not None:
            findings.append(finding)
    return findings
