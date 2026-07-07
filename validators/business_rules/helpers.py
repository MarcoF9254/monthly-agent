CHINESE_PLACEHOLDER_VALUES = {
    "待定",
    "未定",
    "待確認",
    "未列明",
    "不詳",
}

ENGLISH_PLACEHOLDER_VALUES = {
    "",
    "-",
    "—",
    "n/a",
    "na",
    "tbc",
    "unknown",
}

CHINESE_FREE_INDICATOR_VALUES = {
    "免費",
    "全免",
    "不設收費",
    "免收費",
    "免收費用",
    "費用全免",
}

ENGLISH_FREE_INDICATOR_VALUES = {
    "free",
    "free of charge",
    "no charge",
}

FREE_INDICATOR_VALUES = CHINESE_FREE_INDICATOR_VALUES | ENGLISH_FREE_INDICATOR_VALUES


def is_placeholder(value) -> bool:
    if not isinstance(value, str):
        return False

    normalized = value.strip()
    return (
        normalized in CHINESE_PLACEHOLDER_VALUES
        or normalized.lower() in ENGLISH_PLACEHOLDER_VALUES
    )


def is_meaningful_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not is_placeholder(value)


def is_uncertain(field_name: str, uncertain_fields) -> bool:
    if not isinstance(uncertain_fields, list):
        return False

    return any(
        isinstance(item, str) and item.strip() == field_name
        for item in uncertain_fields
    )


def is_free_indicator(value) -> bool:
    if not isinstance(value, str):
        return False

    normalized = value.strip()
    return (
        normalized in CHINESE_FREE_INDICATOR_VALUES
        or normalized.lower() in ENGLISH_FREE_INDICATOR_VALUES
    )
