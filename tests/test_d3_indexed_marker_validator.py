"""Tests for the D3 Indexed Marker Syntax Validator."""

import pytest

from validators.d3_indexed_marker_validator import (
    RULE_ID,
    SEVERITY,
    FIELD,
    RECOMMENDATION,
    check,
    _validate_indexed_marker,
    INDEXED_MARKER_RE,
)


class TestValidateIndexedMarker:
    """Tests for the _validate_indexed_marker helper."""

    def test_valid_indexed_marker(self):
        """Approved ADR-006 indexed paths pass."""
        markers = [
            "dates[0].date_text",
            "dates[1].date_text",
            "fee[0].amount_text",
            "fee[17].amount",
            "dates[42].date_text",
        ]
        for marker in markers:
            is_valid, message = _validate_indexed_marker(marker)
            assert is_valid, f"Expected '{marker}' to be valid: {message}"

    def test_wildcard_index_rejected(self):
        """Wildcard index * is not approved."""
        is_valid, message = _validate_indexed_marker("dates[*].date_text")
        assert not is_valid
        assert "wildcard" in message.lower()

    def test_empty_index_rejected(self):
        """Empty brackets [] are not approved."""
        is_valid, message = _validate_indexed_marker("dates[].date_text")
        assert not is_valid
        assert "empty index" in message.lower()

    def test_range_syntax_rejected(self):
        """Range syntax [0:2] is not approved."""
        is_valid, message = _validate_indexed_marker("dates[0:2].date_text")
        assert not is_valid
        assert "range" in message.lower()

    def test_jsonpath_syntax_rejected(self):
        """JSONPath syntax $..dates[...] is not approved."""
        markers = [
            "$..dates[*].date_text",
            "@.dates[0].date_text",
        ]
        for marker in markers:
            is_valid, message = _validate_indexed_marker(marker)
            assert not is_valid
            assert "jsonpath" in message.lower() or "$" in message or "@" in message

    def test_unknown_index_placeholder_rejected(self):
        """Unknown-index placeholder ? is not approved."""
        is_valid, message = _validate_indexed_marker("dates[?].date_text")
        assert not is_valid
        assert "placeholder" in message.lower()

    def test_non_numeric_index_rejected(self):
        """Fuzzy/semantic non-numeric indexes are not approved."""
        markers = [
            "dates[approx].date_text",
            "dates[first].date_text",
            "dates[last].date_text",
        ]
        for marker in markers:
            is_valid, message = _validate_indexed_marker(marker)
            assert not is_valid
            assert "non-numeric" in message.lower() or "index" in message.lower()

    def test_missing_subfield_rejected(self):
        """Bare indexed field without subfield is not approved."""
        is_valid, message = _validate_indexed_marker("dates[0]")
        assert not is_valid
        assert "subfield" in message.lower()

    def test_leading_dot_or_slash_rejected(self):
        """Leading dot or slash is not approved."""
        markers = [".dates[0].date_text", "/dates[0].date_text"]
        for marker in markers:
            is_valid, message = _validate_indexed_marker(marker)
            assert not is_valid
            assert "leading" in message.lower()

    def test_trailing_dot_rejected(self):
        """Trailing dot is not approved."""
        is_valid, message = _validate_indexed_marker("dates[0].date_text.")
        assert not is_valid
        assert "trailing" in message.lower()

    def test_identifier_shaped_field_and_subfield_are_syntactically_valid(self):
        """Shape validation does not infer field types or grant rule authority."""
        is_valid, message = _validate_indexed_marker("date_text[0].value")
        assert is_valid
        assert message == ""

        # Acceptance establishes syntax only. BR-006 and runtime authorization
        # remain separate fail-closed semantic gates outside this validator.
        assert check(["date_text[0].value"]) == []


class TestCheckFunction:
    """Tests for the check() function."""

    def test_empty_list_passes(self):
        """Empty uncertain_fields passes with no findings."""
        assert check([]) == []

    def test_none_or_non_list_passes(self):
        """None or non-list input returns empty findings."""
        assert check(None) == []
        assert check("not a list") == []
        assert check(42) == []

    def test_bare_markers_are_outside_d3_adjudication(self):
        """D3 does not maintain or consult a vocabulary of bare field names."""
        fields = [
            "fee",
            "venue",
            "source_reference",
            "eligibility",
            "bogus_nonexistent_field",
        ]
        assert check(fields) == []

    def test_single_invalid_marker_produces_finding(self):
        """A single invalid marker produces one Finding Contract v1 finding."""
        findings = check(["dates[*].date_text"])
        assert len(findings) == 1

        finding = findings[0]
        assert finding["rule_id"] == RULE_ID
        assert finding["field"] == FIELD
        assert finding["severity"] == SEVERITY
        assert finding["recommendation"] == RECOMMENDATION
        assert finding["index"] == 0
        assert finding["activity_id"] == "<unknown>"
        assert finding["path"] == "dates[*].date_text"
        assert finding["message"]

    def test_multiple_invalid_produces_multiple_findings(self):
        """Each invalid marker produces its own finding."""
        fields = [
            "fee",
            "dates[*].date_text",
            "dates[0].date_text",
            "dates[?].date_text",
        ]
        findings = check(fields)
        assert len(findings) == 2
        assert findings[0]["path"] == "dates[*].date_text"
        assert findings[1]["path"] == "dates[?].date_text"

    def test_invalid_between_valid_produces_only_invalid_findings(self):
        """Bare markers pass through; only invalid attempted indexed markers produce findings."""
        fields = [
            "fee",
            "dates[0:2].date_text",
            "dates[0].date_text",
            "$..dates[*].date_text",
            "venue",
        ]
        findings = check(fields)
        assert len(findings) == 2
        assert findings[0]["path"] == "dates[0:2].date_text"
        assert findings[1]["path"] == "$..dates[*].date_text"

    def test_non_string_items_ignored(self):
        """Non-string items in uncertain_fields are ignored."""
        fields = ["fee", 123, None, 45.6, "dates[0].date_text"]
        assert check(fields) == []

    def test_finding_contract_v1_structure(self):
        """Each finding has all required Finding Contract v1 fields."""
        findings = check(["dates[].date_text"])
        assert len(findings) == 1

        finding = findings[0]
        required_fields = {
            "index", "activity_id", "rule_id",
            "field", "path", "severity",
            "message", "recommendation",
        }
        assert set(finding.keys()) == required_fields

    def test_custom_index_and_activity_id(self):
        """Custom index and activity_id_override are propagated."""
        findings = check(
            ["dates[*].date_text"],
            index=5,
            activity_id_override="CUSTOM-001",
        )
        assert len(findings) == 1
        assert findings[0]["index"] == 5
        assert findings[0]["activity_id"] == "CUSTOM-001"

    def test_range_syntax_finding_content(self):
        """Range syntax produces an informative message."""
        findings = check(["dates[0:2].date_text"])
        assert len(findings) == 1
        message = findings[0]["message"]
        assert "range" in message.lower()

    def test_all_explicitly_invalid_forms(self):
        """All explicitly unapproved forms from ADR-006 are rejected."""
        invalid_forms = [
            "dates[*].date_text",     # wildcard
            "dates[].date_text",      # empty index
            "dates[0:2].date_text",   # range
            "$..dates[*].date_text",  # JSONPath
            "dates[?].date_text",     # unknown-index placeholder
            "dates[approx].date_text",  # fuzzy/semantic
        ]
        for form in invalid_forms:
            findings = check([form])
            assert len(findings) == 1, f"Expected '{form}' to produce a finding"
