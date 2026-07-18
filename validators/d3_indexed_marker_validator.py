"""
D3 — Indexed Marker Syntax Validator

Validates only the syntax of uncertain_fields entries against the ADR-006 indexed
path shape. A passing result grants no rule-specific, schema-level, runtime, or
activation authority. Limited to fictional/test inputs and not registered in the
active business-rule registry.
"""

import re
from typing import Any

from validators.business_rules.helpers import finding

RULE_ID = "D3"
FIELD = "uncertain_fields"
SEVERITY = "medium"
RECOMMENDATION = (
    "Use the approved ADR-006 indexed path shape: "
    "<field>[<zero-based-index>].<subfield>."
)

INDEXED_MARKER_RE = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]\.([a-zA-Z_][a-zA-Z0-9_]*)$")

# Recognized top-level field names that may appear directly in uncertain_fields
TOP_LEVEL_FIELDS = frozenset({
    "activity_title",
    "time",
    "venue",
    "fee",
    "dates",
    "category",
    "registration_period",
    "quota",
    "eligibility",
    "source_reference",
})


def _is_top_level_marker(marker: str) -> bool:
    return marker.strip() in TOP_LEVEL_FIELDS


def _validate_indexed_marker(marker: str) -> tuple[bool, str]:
    """Validate only whether an indexed marker matches the ADR-006 shape.

    Field and subfield identifiers are not semantically authorized here.

    Returns (is_valid, message).
    """
    if not isinstance(marker, str):
        return False, f"Invalid marker type: {type(marker).__name__}."

    stripped = marker.strip()

    # Must contain brackets — all indexed markers do
    if "[" not in stripped or "]" not in stripped:
        return False, f"Marker '{stripped}' is not a recognized top-level field or valid indexed path."

    # Check for leading dots/slashes
    if stripped.startswith(".") or stripped.startswith("/"):
        return False, (
            f"Marker '{stripped}' uses a leading dot or slash. "
            "Indexed paths must start with a field name."
        )

    # Check for trailing dots/slashes
    if stripped.endswith(".") or stripped.endswith("/"):
        return False, (
            f"Marker '{stripped}' has a trailing dot or slash. "
            "Indexed paths must end with a subfield name."
        )

    # Check for wildcards in index position
    if re.search(r"\[\s*\*\s*\]", stripped):
        return False, (
            f"Marker '{stripped}' uses a wildcard index '*'. "
            "Wildcards are not approved by ADR-006."
        )

    # Check for empty index
    if re.search(r"\[\s*\]", stripped):
        return False, (
            f"Marker '{stripped}' has an empty index. "
            "Index must be a zero-based non-negative integer."
        )

    # Check for range syntax
    if re.search(r"\[\d+\s*:\s*\d+\]", stripped):
        return False, (
            f"Marker '{stripped}' uses a range syntax. "
            "Ranges are not approved by ADR-006."
        )

    # Check for JSONPath syntax
    if stripped.startswith("$") or stripped.startswith("@"):
        return False, (
            f"Marker '{stripped}' uses JSONPath syntax ($ or @). "
            "JSONPath syntax is not approved by ADR-006."
        )

    # Check for regex-like patterns in marker
    if re.search(r"/.*/", stripped) and "[]" not in stripped and "[*]" not in stripped:
        return False, (
            f"Marker '{stripped}' appears to contain regex syntax. "
            "Regex paths are not approved by ADR-006."
        )

    # Check for unknown-index placeholders
    if re.search(r"\[\s*\?\s*\]", stripped):
        return False, (
            f"Marker '{stripped}' uses an unknown-index placeholder '?'. "
            "Unknown-index placeholders are not approved by ADR-006."
        )

    # Check for fuzzy/semantic paths (non-numeric index)
    bracket_content = re.findall(r"\[([^\]]+)\]", stripped)
    for content in bracket_content:
        if not content.strip().isdigit():
            return False, (
                f"Marker '{stripped}' has non-numeric index '{content}'. "
                "Index must be a zero-based non-negative integer."
            )

    # Validate against the approved pattern
    match = INDEXED_MARKER_RE.match(stripped)
    if not match:
        # It looks like an indexed path but doesn't match — likely missing subfield
        if "[" in stripped and "]" in stripped:
            return False, (
                f"Marker '{stripped}' has an indexed field but is missing "
                "a valid subfield after the index. "
                "Use <field>[<index>].<subfield>."
            )
        return False, (
            f"Marker '{stripped}' does not match the approved ADR-006 "
            "indexed path shape: <field>[<zero-based-index>].<subfield>."
        )

    return True, ""


def check(
    uncertain_fields: Any,
    *,
    index: int = 0,
    activity_id_override: str = "<unknown>",
) -> list[dict]:
    """Validate uncertain_fields entries against ADR-006 indexed path shape.

    Args:
        uncertain_fields: The uncertain_fields list to validate.
        index: Record index for Finding Contract v1 (default 0).
        activity_id_override: Activity ID override (default "<unknown>").

    Returns:
        List of Finding Contract v1 findings.
    """
    if not isinstance(uncertain_fields, list):
        return []

    findings: list[dict] = []

    for item in uncertain_fields:
        if not isinstance(item, str):
            # Non-string entries are structurally invalid but out of D3 scope
            continue

        stripped = item.strip()

        # Accept recognized top-level markers
        if stripped in TOP_LEVEL_FIELDS or _is_top_level_marker(stripped):
            continue

        # Validate indexed marker
        is_valid, message = _validate_indexed_marker(stripped)
        if not is_valid:
            findings.append(finding(
                {"activity_id": activity_id_override},
                index,
                RULE_ID,
                FIELD,
                stripped,
                SEVERITY,
                message,
                RECOMMENDATION,
            ))

    return findings
