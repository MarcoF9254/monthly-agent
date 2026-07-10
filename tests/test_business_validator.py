import json
import subprocess
import sys
from pathlib import Path

from validators.business_rules.br001_required_fields import check as check_br001
from validators.business_rules.br002_fee_uncertainty import check as check_br002
from validators.business_rules.br003_registration_period import check as check_br003
from validators.business_rules.br004_qa_status import check as check_br004
from validators.business_rules.br005_source_reference import check as check_br005
from validators.business_rules.br006_per_session_date_completeness import check as check_br006


ROOT_DIR = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT_DIR / "tools" / "validate_business_rules.py"
SAMPLE_OUTPUT = ROOT_DIR / "examples" / "sample-output.json"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def sample_record() -> dict:
    with SAMPLE_OUTPUT.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)[0]


def write_records(tmp_path: Path, records: list[dict]) -> Path:
    path = tmp_path / "records.json"
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return path


def findings_for(record: dict) -> list[dict]:
    return check_br001(record, index=3)


def br002_findings_for(record: dict) -> list[dict]:
    return check_br002(record, index=4)


def br003_findings_for(record: dict) -> list[dict]:
    return check_br003(record, index=5)


def br004_findings_for(record: dict) -> list[dict]:
    return check_br004(record, index=6)


def br005_findings_for(record: dict) -> list[dict]:
    return check_br005(record, index=7)


def br006_findings_for(record: dict) -> list[dict]:
    return check_br006(record, index=8)


def fields(findings: list[dict]) -> set[str]:
    return {finding["field"] for finding in findings}


def test_sample_output_passes():
    result = run_validator(SAMPLE_OUTPUT)

    assert result.returncode == 0
    assert result.stdout.strip() == "PASS"
    assert result.stderr == ""


def test_missing_venue_with_empty_uncertain_fields_fails_br001():
    record = sample_record()
    record.pop("venue")
    record["uncertain_fields"] = []

    findings = findings_for(record)

    assert len(findings) == 1
    assert findings[0]["index"] == 3
    assert findings[0]["activity_id"] == record["activity_id"]
    assert findings[0]["rule_id"] == "BR-001"
    assert findings[0]["field"] == "venue"
    assert findings[0]["path"] == "venue"
    assert findings[0]["severity"] == "high"
    assert findings[0]["message"] == "Required field 'venue' is missing, empty, or not meaningful."
    assert findings[0]["recommendation"] == (
        "Check the source document. Add the missing value if present, or list this field "
        "in uncertain_fields if the source is unclear."
    )


def test_missing_venue_with_uncertain_field_passes():
    record = sample_record()
    record.pop("venue")
    record["uncertain_fields"] = ["venue"]

    assert findings_for(record) == []


def test_uncertain_field_with_surrounding_whitespace_suppresses_finding():
    record = sample_record()
    record["venue"] = ""
    record["uncertain_fields"] = [" venue "]

    assert findings_for(record) == []


def test_empty_fee_array_fails_unless_fee_is_uncertain():
    record = sample_record()
    record["fee"] = []

    findings = findings_for(record)

    assert fields(findings) == {"fee"}
    assert findings[0]["path"] == "fee"

    record["uncertain_fields"] = ["fee"]
    assert findings_for(record) == []


def test_fee_item_with_empty_amount_text_fails_unless_fee_is_uncertain():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount_text": "  "}]

    findings = findings_for(record)

    assert fields(findings) == {"fee"}
    assert findings[0]["path"] == "fee[].amount_text"

    record["uncertain_fields"] = ["fee"]
    assert findings_for(record) == []


def test_dates_empty_fails_unless_dates_is_uncertain():
    record = sample_record()
    record["dates"] = []

    findings = findings_for(record)

    assert fields(findings) == {"dates"}
    assert findings[0]["path"] == "dates"

    record["uncertain_fields"] = ["dates"]
    assert findings_for(record) == []


def test_date_item_with_empty_date_text_is_not_br001_per_entry_finding():
    record = sample_record()
    record["dates"] = [{"date_text": ""}]
    record["uncertain_fields"] = []

    assert findings_for(record) == []


def test_br006_all_date_text_meaningful_passes():
    record = sample_record()
    record["dates"] = [
        {"date_text": "2026-04-08"},
        {"date_text": "next Wednesday"},
    ]
    record["uncertain_fields"] = []

    assert br006_findings_for(record) == []


def test_br006_exact_indexed_uncertain_marker_passes():
    record = sample_record()
    record["dates"] = [
        {"date_text": "2026-04-08"},
        {"date_text": ""},
    ]
    record["uncertain_fields"] = ["dates[1].date_text"]

    assert br006_findings_for(record) == []


def test_br006_blank_date_text_without_exact_marker_fails():
    record = sample_record()
    record["dates"] = [
        {"date_text": "2026-04-08"},
        {"date_text": ""},
    ]
    record["uncertain_fields"] = []

    findings = br006_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["index"] == 8
    assert findings[0]["activity_id"] == record["activity_id"]
    assert findings[0]["rule_id"] == "BR-006"
    assert findings[0]["field"] == "dates"
    assert findings[0]["path"] == "dates[1].date_text"
    assert findings[0]["severity"] == "high"
    assert findings[0]["message"] == "Session date is missing for dates[1].date_text."
    assert findings[0]["recommendation"] == (
        "Fill in the session date from source evidence or mark the exact per-session "
        "date field as uncertain for QA / Human Review."
    )
    assert set(findings[0]) == {
        "index",
        "activity_id",
        "rule_id",
        "field",
        "path",
        "severity",
        "message",
        "recommendation",
    }


def test_br006_top_level_dates_uncertainty_does_not_suppress_per_entry_finding():
    record = sample_record()
    record["dates"] = [
        {"date_text": "2026-04-08"},
        {"date_text": ""},
    ]
    record["uncertain_fields"] = ["dates"]

    findings = br006_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["path"] == "dates[1].date_text"


def test_br006_placeholder_date_text_values_fail():
    for placeholder in ["待定", "未定", "TBC", "unknown"]:
        record = sample_record()
        record["dates"] = [{"date_text": placeholder}]
        record["uncertain_fields"] = []

        findings = br006_findings_for(record)

        assert len(findings) == 1
        assert findings[0]["rule_id"] == "BR-006"
        assert findings[0]["field"] == "dates"
        assert findings[0]["path"] == "dates[0].date_text"
        assert findings[0]["severity"] == "high"


def test_br006_emits_one_finding_per_failing_date_entry():
    record = sample_record()
    record["dates"] = [
        {"date_text": ""},
        {"date_text": "2026-04-08"},
        {"date_text": "TBC"},
        {},
    ]
    record["uncertain_fields"] = []

    findings = br006_findings_for(record)

    assert [finding["path"] for finding in findings] == [
        "dates[0].date_text",
        "dates[2].date_text",
        "dates[3].date_text",
    ]


def test_br006_missing_or_empty_dates_is_left_to_br001_or_schema():
    missing_record = sample_record()
    missing_record.pop("dates")
    assert br006_findings_for(missing_record) == []

    empty_record = sample_record()
    empty_record["dates"] = []
    assert br006_findings_for(empty_record) == []


def test_br006_unparseable_but_meaningful_date_text_passes():
    record = sample_record()
    record["dates"] = [{"date_text": "next Wednesday"}]
    record["uncertain_fields"] = []

    assert br006_findings_for(record) == []


def test_source_reference_missing_or_empty_fails_medium_unless_uncertain():
    missing_record = sample_record()
    missing_record.pop("source_reference")

    missing_findings = findings_for(missing_record)

    assert fields(missing_findings) == {"source_reference"}
    assert missing_findings[0]["severity"] == "medium"

    empty_record = sample_record()
    empty_record["source_reference"] = ""

    empty_findings = findings_for(empty_record)

    assert fields(empty_findings) == {"source_reference"}
    assert empty_findings[0]["severity"] == "medium"

    empty_record["uncertain_fields"] = ["source_reference"]
    assert findings_for(empty_record) == []


def test_whitespace_only_string_field_fails():
    record = sample_record()
    record["venue"] = "   "

    assert fields(findings_for(record)) == {"venue"}


def test_placeholder_values_fail_unless_uncertain():
    placeholder_cases = [
        ("activity_title", "TBC"),
        ("time", "待定"),
        ("venue", "-"),
        ("source_reference", "N/A"),
        ("activity_title", " tbc "),
        ("venue", "UNKNOWN"),
        ("source_reference", " n/a "),
    ]

    for field, placeholder in placeholder_cases:
        record = sample_record()
        record[field] = placeholder

        assert fields(findings_for(record)) == {field}

        record["uncertain_fields"] = [field]
        assert findings_for(record) == []


def test_uncertain_fields_ignore_non_string_values_without_crashing():
    record = sample_record()
    record["fee"] = []
    record["venue"] = ""
    record["uncertain_fields"] = ["fee", 123, None]

    assert fields(findings_for(record)) == {"venue"}


def test_br002_amount_null_with_free_indicator_passes():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": None, "amount_text": "免費"}]
    record["uncertain_fields"] = []

    assert br002_findings_for(record) == []


def test_br002_amount_null_with_uncertain_fee_passes():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": None, "amount_text": "請向中心查詢"}]
    record["uncertain_fields"] = ["fee"]

    assert br002_findings_for(record) == []


def test_br002_amount_null_with_pending_fee_fails():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": None, "amount_text": "費用待定"}]
    record["uncertain_fields"] = []

    findings = br002_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["index"] == 4
    assert findings[0]["activity_id"] == record["activity_id"]
    assert findings[0]["rule_id"] == "BR-002"
    assert findings[0]["field"] == "fee[].amount"
    assert findings[0]["path"] == "fee[0].amount"
    assert findings[0]["severity"] == "high"


def test_br002_partial_free_indicator_match_does_not_pass():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": None, "amount_text": "本月活動費用全免喎"}]
    record["uncertain_fields"] = []

    findings = br002_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["rule_id"] == "BR-002"
    assert findings[0]["field"] == "fee[].amount"
    assert findings[0]["path"] == "fee[0].amount"

def test_br002_amount_present_with_meaningful_amount_text_passes():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": 15, "amount_text": "$15"}]
    record["uncertain_fields"] = []

    assert br002_findings_for(record) == []


def test_br002_amount_present_with_free_text_passes_as_meaningful_source_text():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": 15, "amount_text": " 免費 "}]
    record["uncertain_fields"] = []

    assert br002_findings_for(record) == []

def test_br002_amount_present_with_empty_amount_text_fails():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": 15, "amount_text": ""}]
    record["uncertain_fields"] = []

    findings = br002_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["field"] == "fee[].amount_text"
    assert findings[0]["path"] == "fee[0].amount_text"


def test_br002_amount_present_with_placeholder_amount_text_fails():
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": 15, "amount_text": "TBC"}]
    record["uncertain_fields"] = []

    findings = br002_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["path"] == "fee[0].amount_text"


def test_br002_multiple_fee_items_validate_independently():
    record = sample_record()
    record["fee"] = [
        {"fee_type": "會員", "amount": 20, "amount_text": "$20"},
        {"fee_type": "非會員", "amount": None, "amount_text": ""},
    ]
    record["uncertain_fields"] = []

    findings = br002_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["path"] == "fee[1].amount"


def test_br002_whitespace_handling_for_free_and_meaningful_text():
    record = sample_record()
    record["fee"] = [
        {"fee_type": "一般", "amount": None, "amount_text": " 免費 "},
        {"fee_type": "材料", "amount": 15, "amount_text": " $15 "},
    ]
    record["uncertain_fields"] = []

    assert br002_findings_for(record) == []


def test_br002_english_free_indicators_are_case_insensitive():
    for amount_text in ["free", "Free of charge", " NO CHARGE "]:
        record = sample_record()
        record["fee"] = [{"fee_type": "一般", "amount": None, "amount_text": amount_text}]
        record["uncertain_fields"] = []

        assert br002_findings_for(record) == []


def test_br003_actionable_registration_timing_passes():
    for registration_period in [
        "6月3日上午9時開始報名",
        "6月3日至6月10日",
        "截止報名日期：6月10日",
        "即日起接受報名",
        "即日起至額滿",
        "額滿即止",
        "長期接受報名",
        "全年接受報名",
        "每月首個工作天開始報名",
        "活動前一星期截止",
        "電話報名，6月3日起接受報名",
    ]:
        record = sample_record()
        record["registration_period"] = registration_period
        record["uncertain_fields"] = []

        assert br003_findings_for(record) == []


def test_br003_no_registration_indicators_pass_with_exact_matching():
    for registration_period in [
        "毋須報名",
        "無須報名",
        "不用報名",
        "免報名",
        "無需登記",
        "no registration required",
        " Registration Not Required ",
    ]:
        record = sample_record()
        record["registration_period"] = registration_period
        record["uncertain_fields"] = []

        assert br003_findings_for(record) == []


def test_br003_non_actionable_registration_period_fails_unless_uncertain():
    for registration_period in [
        "電話報名",
        "親臨中心報名",
        "請向中心職員查詢",
        "詳情請致電中心",
        "報名日期待定",
        "稍後公布",
        "通訊未列明報名日期",
    ]:
        record = sample_record()
        record["registration_period"] = registration_period
        record["uncertain_fields"] = []

        findings = br003_findings_for(record)

        assert len(findings) == 1
        assert findings[0]["index"] == 5
        assert findings[0]["activity_id"] == record["activity_id"]
        assert findings[0]["rule_id"] == "BR-003"
        assert findings[0]["field"] == "registration_period"
        assert findings[0]["path"] == "registration_period"
        assert findings[0]["severity"] == "high"

        record["uncertain_fields"] = ["registration_period"]
        assert br003_findings_for(record) == []


def test_br003_missing_empty_or_placeholder_registration_period_fails_unless_uncertain():
    missing_record = sample_record()
    missing_record.pop("registration_period")
    missing_record["uncertain_fields"] = []

    assert fields(br003_findings_for(missing_record)) == {"registration_period"}

    for registration_period in ["", "   ", "待定", "TBC"]:
        record = sample_record()
        record["registration_period"] = registration_period
        record["uncertain_fields"] = []

        assert fields(br003_findings_for(record)) == {"registration_period"}

        record["uncertain_fields"] = [" registration_period "]
        assert br003_findings_for(record) == []


def test_br003_partial_no_registration_indicator_is_not_special_case():
    record = sample_record()
    record["registration_period"] = "本活動毋須報名，敬請留意"
    record["uncertain_fields"] = []

    assert br003_findings_for(record) == []


def test_br004_pending_with_empty_uncertain_fields_passes():
    record = sample_record()
    record["qa_status"] = "pending"
    record["uncertain_fields"] = []

    assert br004_findings_for(record) == []


def test_br004_pending_with_non_empty_uncertain_fields_passes():
    record = sample_record()
    record["qa_status"] = "pending"
    record["uncertain_fields"] = ["fee"]

    assert br004_findings_for(record) == []


def test_br004_approved_with_empty_uncertain_fields_fails_on_qa_status():
    record = sample_record()
    record["qa_status"] = "approved"
    record["uncertain_fields"] = []

    findings = br004_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["index"] == 6
    assert findings[0]["activity_id"] == record["activity_id"]
    assert findings[0]["rule_id"] == "BR-004"
    assert findings[0]["field"] == "qa_status"
    assert findings[0]["path"] == "qa_status"
    assert findings[0]["severity"] == "high"
    assert set(findings[0]) == {
        "index",
        "activity_id",
        "rule_id",
        "field",
        "path",
        "severity",
        "message",
        "recommendation",
    }


def test_br004_approved_with_non_empty_uncertain_fields_fails_on_uncertainty():
    record = sample_record()
    record["qa_status"] = "approved"
    record["uncertain_fields"] = ["registration_period"]

    findings = br004_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["rule_id"] == "BR-004"
    assert findings[0]["field"] == "uncertain_fields"
    assert findings[0]["path"] == "uncertain_fields"
    assert findings[0]["severity"] == "high"


def test_br004_needs_review_fails_on_qa_status():
    record = sample_record()
    record["qa_status"] = "needs_review"

    findings = br004_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["field"] == "qa_status"
    assert findings[0]["path"] == "qa_status"
    assert findings[0]["severity"] == "medium"


def test_br004_rejected_fails_on_qa_status():
    record = sample_record()
    record["qa_status"] = "rejected"

    findings = br004_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["field"] == "qa_status"
    assert findings[0]["path"] == "qa_status"
    assert findings[0]["severity"] == "medium"


def test_br004_does_not_emit_duplicate_findings():
    record = sample_record()
    record["qa_status"] = "approved"
    record["uncertain_fields"] = ["fee"]

    findings = br004_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["field"] == "uncertain_fields"


def test_br005_exact_activity_title_anchor_passes():
    record = sample_record()
    record["activity_title"] = "Tai Chi Class"
    record["category"] = "Exercise"
    record["source_reference"] = "Activity title: Tai Chi Class"
    record["uncertain_fields"] = []

    assert br005_findings_for(record) == []


def test_br005_exact_category_anchor_passes():
    record = sample_record()
    record["activity_title"] = "Tai Chi Class"
    record["category"] = "Health Talks"
    record["source_reference"] = "Category: Health Talks"
    record["uncertain_fields"] = []

    assert br005_findings_for(record) == []


def test_br005_structured_locator_anchors_pass():
    passing_references = [
        "monthly programme, page 2, row 5",
        "table A row 3",
        "item number 7",
        "activity number 12",
    ]

    for source_reference in passing_references:
        record = sample_record()
        record["activity_title"] = "Tai Chi Class"
        record["category"] = "Exercise"
        record["source_reference"] = source_reference
        record["uncertain_fields"] = []

        assert br005_findings_for(record) == []


def test_br005_fullwidth_pipe_delimited_exact_anchor_passes():
    record = sample_record()
    record["category"] = "健康講座"
    record["activity_title"] = "護心有法健康講座"
    record["source_reference"] = "健康講座｜護心有法健康講座"
    record["uncertain_fields"] = []

    assert br005_findings_for(record) == []


def test_br005_missing_empty_or_placeholder_source_reference_is_left_to_br001():
    missing_record = sample_record()
    missing_record.pop("source_reference")

    assert br005_findings_for(missing_record) == []

    for source_reference in ["", "   ", "TBC", "N/A", "-"]:
        record = sample_record()
        record["source_reference"] = source_reference
        record["uncertain_fields"] = []

        assert br005_findings_for(record) == []


def test_br005_uncertain_source_reference_suppresses_finding():
    record = sample_record()
    record["source_reference"] = "monthly programme"
    record["uncertain_fields"] = [" source_reference "]

    assert br005_findings_for(record) == []


def test_br005_generic_source_reference_fails():
    record = sample_record()
    record["activity_title"] = "Tai Chi Class"
    record["category"] = "Exercise"
    record["source_reference"] = "monthly programme"
    record["uncertain_fields"] = []

    findings = br005_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["index"] == 7
    assert findings[0]["activity_id"] == record["activity_id"]
    assert findings[0]["rule_id"] == "BR-005"
    assert findings[0]["field"] == "source_reference"
    assert findings[0]["path"] == "source_reference"
    assert findings[0]["severity"] == "medium"
    assert set(findings[0]) == {
        "index",
        "activity_id",
        "rule_id",
        "field",
        "path",
        "severity",
        "message",
        "recommendation",
    }


def test_br005_bare_page_or_section_only_references_fail():
    for source_reference in ["monthly programme, page 2", "Health section"]:
        record = sample_record()
        record["activity_title"] = "Tai Chi Class"
        record["category"] = "Exercise"
        record["source_reference"] = source_reference
        record["uncertain_fields"] = []

        findings = br005_findings_for(record)

        assert len(findings) == 1
        assert findings[0]["field"] == "source_reference"
        assert findings[0]["path"] == "source_reference"


def test_br005_partial_activity_title_does_not_pass():
    record = sample_record()
    record["activity_title"] = "Tai Chi Class"
    record["category"] = "Exercise"
    record["source_reference"] = "Tai Chi"
    record["uncertain_fields"] = []

    findings = br005_findings_for(record)

    assert len(findings) == 1
    assert findings[0]["rule_id"] == "BR-005"


def test_cli_returns_0_on_pass(tmp_path):
    path = write_records(tmp_path, [sample_record()])

    result = run_validator(path)

    assert result.returncode == 0
    assert result.stdout.strip() == "PASS"


def test_cli_returns_0_on_br002_free_fee_pass(tmp_path):
    record = sample_record()
    record["fee"] = [{"fee_type": "一般", "amount": None, "amount_text": "Free of charge"}]
    record["uncertain_fields"] = []
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 0
    assert result.stdout.strip() == "PASS"


def test_cli_returns_1_on_br003_registration_period_failure(tmp_path):
    record = sample_record()
    record["registration_period"] = "通訊未列明報名日期"
    record["uncertain_fields"] = []
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "BR-003" in result.stdout
    assert "registration_period" in result.stdout
    assert "Registration period does not provide actionable registration timing." in result.stdout


def test_cli_returns_1_on_br004_qa_status_failure(tmp_path):
    record = sample_record()
    record["qa_status"] = "approved"
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "BR-004" in result.stdout
    assert "qa_status" in result.stdout


def test_cli_returns_1_on_br005_source_reference_failure(tmp_path):
    record = sample_record()
    record["activity_title"] = "Tai Chi Class"
    record["category"] = "Exercise"
    record["source_reference"] = "monthly programme"
    record["uncertain_fields"] = []
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "BR-005" in result.stdout
    assert "source_reference" in result.stdout


def test_cli_returns_1_on_br001_failure(tmp_path):
    record = sample_record()
    record["venue"] = ""
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "BR-001" in result.stdout
    assert "venue" in result.stdout


def test_cli_returns_1_on_br006_date_text_failure(tmp_path):
    record = sample_record()
    record["dates"] = [
        {"date_text": "2026-04-08"},
        {"date_text": ""},
    ]
    record["uncertain_fields"] = []
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "BR-006" in result.stdout
    assert "dates[1].date_text" in result.stdout
    assert "Session date is missing for dates[1].date_text." in result.stdout


def test_cli_returns_2_on_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("{invalid json", encoding="utf-8")

    result = run_validator(path)

    assert result.returncode == 2
    assert result.stdout == ""
    assert "Invalid JSON" in result.stderr

