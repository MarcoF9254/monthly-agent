from validators.business_rules.helpers import (
    finding,
    is_meaningful_string,
    is_uncertain,
    matches_closed_list,
)


RULE_ID = "BR-003"
RECOMMENDATION = (
    "Check the source document. Confirm the registration timing, or list "
    "registration_period in uncertain_fields if the source is unclear."
)

CHINESE_NO_REGISTRATION_INDICATORS = {
    "毋須報名",
    "無須報名",
    "不用報名",
    "免報名",
    "無需登記",
}

ENGLISH_NO_REGISTRATION_INDICATORS = {
    "no registration required",
    "registration not required",
}

CHINESE_NON_ACTIONABLE_INDICATORS = {
    "電話報名",
    "親臨中心報名",
    "請向中心職員查詢",
    "詳情請致電中心",
    "報名日期待定",
    "稍後公布",
    "通訊未列明報名日期",
}

ENGLISH_NON_ACTIONABLE_INDICATORS: set[str] = set()


def _is_no_registration_indicator(value) -> bool:
    return matches_closed_list(
        value,
        CHINESE_NO_REGISTRATION_INDICATORS,
        ENGLISH_NO_REGISTRATION_INDICATORS,
    )


def _is_non_actionable_indicator(value) -> bool:
    return matches_closed_list(
        value,
        CHINESE_NON_ACTIONABLE_INDICATORS,
        ENGLISH_NON_ACTIONABLE_INDICATORS,
    )


def _finding(record, index: int) -> dict:
    return finding(
        record,
        index,
        RULE_ID,
        "registration_period",
        "registration_period",
        "high",
        "Registration period does not provide actionable registration timing.",
        RECOMMENDATION,
    )


def check(record, index: int = 0) -> list:
    if not isinstance(record, dict):
        return []

    uncertain_fields = record.get("uncertain_fields")
    if is_uncertain("registration_period", uncertain_fields):
        return []

    registration_period = record.get("registration_period")
    if _is_no_registration_indicator(registration_period):
        return []

    if (
        is_meaningful_string(registration_period)
        and not _is_non_actionable_indicator(registration_period)
    ):
        return []

    return [_finding(record, index)]
