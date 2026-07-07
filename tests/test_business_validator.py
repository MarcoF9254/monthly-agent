import json
import subprocess
import sys
from pathlib import Path

from validators.business_rules.br001_required_fields import check as check_br001
from validators.business_rules.br002_fee_uncertainty import check as check_br002
from validators.business_rules.br003_registration_period import check as check_br003


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


def test_date_item_with_empty_date_text_fails_unless_dates_is_uncertain():
    record = sample_record()
    record["dates"] = [{"date_text": ""}]

    findings = findings_for(record)

    assert fields(findings) == {"dates"}
    assert findings[0]["path"] == "dates[].date_text"

    record["uncertain_fields"] = ["dates"]
    assert findings_for(record) == []


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


def test_cli_returns_1_on_br001_failure(tmp_path):
    record = sample_record()
    record["venue"] = ""
    path = write_records(tmp_path, [record])

    result = run_validator(path)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "BR-001" in result.stdout
    assert "venue" in result.stdout


def test_cli_returns_2_on_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("{invalid json", encoding="utf-8")

    result = run_validator(path)

    assert result.returncode == 2
    assert result.stdout == ""
    assert "Invalid JSON" in result.stderr

