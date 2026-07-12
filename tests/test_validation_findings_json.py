import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools import validate_business_rules, validate_schema
from tools.validation_findings_json import (
    build_validation_artifact,
    validate_finding_contract,
    validate_validation_artifact,
    valid_run_id,
)


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "sample-output.json"
RUN_ID = "2026-07-r01"


def invoke(tool: str, input_path: Path, output: Path | None = None, run_id=RUN_ID):
    command = [sys.executable, str(ROOT / "tools" / tool), str(input_path)]
    if run_id is not None:
        command += ["--run-id", run_id]
    if output is not None:
        command += ["--json-output", str(output)]
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def finding(**overrides):
    value = {
        "index": 0, "activity_id": "a-1", "rule_id": "BR-001",
        "field": "venue", "path": "venue", "severity": "high",
        "message": "Missing venue.", "recommendation": "Check source.",
    }
    value.update(overrides)
    return value


@pytest.mark.parametrize("run_id", ["2026-07-r01", "2026-12-r99"])
def test_run_id_accepts_d1_format(run_id):
    assert valid_run_id(run_id)


@pytest.mark.parametrize("run_id", ["2026-07-r00", "2026-13-r01", "26-07-r01", "2026-07-r1"])
def test_run_id_rejects_invalid_values(run_id):
    assert not valid_run_id(run_id)


@pytest.mark.parametrize("tool", ["schema_validator", "business_validator"])
@pytest.mark.parametrize("status", ["pass", "fail", "error"])
def test_artifact_contract_top_level_fields_and_conditionals(tool, status):
    kwargs = {"findings": []}
    if status == "fail":
        kwargs["message"] = "Input is not an array."
    if status == "error":
        kwargs["error"] = {"type": "execution_error", "target": "runtime", "message": "boom"}
    artifact = build_validation_artifact(
        tool=tool, run_id=RUN_ID, status=status, source_artifact="input.json", **kwargs
    )
    assert set(artifact) >= {"contract_version", "tool", "run_id", "status", "generated_at", "source_artifact", "findings"}
    assert artifact["contract_version"] == "validation-findings-v1"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", artifact["generated_at"])


def test_contract_rejects_fail_without_findings_or_message():
    with pytest.raises(ValueError, match="message"):
        build_validation_artifact(tool="schema_validator", run_id=RUN_ID, status="fail", source_artifact="x", findings=[])


def test_finding_contract_rejects_masking_defaults_and_finding_id():
    malformed = finding(rule_id="<missing>", severity="high", message="", recommendation="")
    malformed["finding_id"] = "not-v1"
    problems = validate_finding_contract(malformed)
    assert any("rule_id" in item for item in problems)
    assert any("message" in item for item in problems)
    assert any("recommendation" in item for item in problems)
    assert any("finding_id" in item for item in problems)


def test_schema_pass_and_fail_artifacts(tmp_path):
    passed = tmp_path / "schema-pass.json"
    result = invoke("validate_schema.py", SAMPLE, passed)
    assert result.returncode == 0 and result.stdout.strip() == "PASS"
    assert read(passed)["status"] == "pass" and read(passed)["findings"] == []

    records = json.loads(SAMPLE.read_text(encoding="utf-8-sig"))
    records[0]["quota"] = 30
    source = tmp_path / "records.json"
    source.write_text(json.dumps(records), encoding="utf-8")
    failed = tmp_path / "schema-fail.json"
    result = invoke("validate_schema.py", source, failed)
    artifact = read(failed)
    assert result.returncode == 1 and "FAIL" in result.stdout
    assert artifact["status"] == "fail"
    assert artifact["findings"][0]["rule_id"] == "SCHEMA"
    assert artifact["findings"][0]["severity"] == "critical"
    assert "finding_id" not in artifact["findings"][0]


@pytest.mark.parametrize("tool", ["validate_schema.py", "validate_business_rules.py"])
def test_non_array_is_run_level_fail(tool, tmp_path):
    source = tmp_path / "object.json"
    source.write_text("{}", encoding="utf-8")
    output = tmp_path / "finding.json"
    result = invoke(tool, source, output)
    artifact = read(output)
    assert result.returncode == 1 and "FAIL" in result.stdout
    assert artifact["status"] == "fail" and artifact["findings"] == []
    assert artifact["message"]
    assert "error" not in artifact


@pytest.mark.parametrize("tool", ["validate_schema.py", "validate_business_rules.py"])
@pytest.mark.parametrize("kind", ["missing", "invalid_json"])
def test_input_errors_write_artifacts(tool, kind, tmp_path):
    source = tmp_path / "input.json"
    if kind == "invalid_json":
        source.write_text("{no", encoding="utf-8")
    output = tmp_path / "error.json"
    result = invoke(tool, source, output)
    artifact = read(output)
    expected = "file_not_found" if kind == "missing" else "invalid_json"
    assert result.returncode == 2 and "ERROR:" in result.stderr
    assert artifact["status"] == "error" and artifact["findings"] == []
    assert artifact["error"]["type"] == expected
    assert artifact["error"]["target"] == "input"


@pytest.mark.parametrize("tool", ["validate_schema.py", "validate_business_rules.py"])
@pytest.mark.parametrize("run_id", [None, "2026-07-r00"])
def test_invalid_arguments_are_pre_artifact(tool, run_id, tmp_path):
    output = tmp_path / "must-not-exist.json"
    result = invoke(tool, SAMPLE, output, run_id=run_id)
    assert result.returncode == 2 and result.stderr
    assert not output.exists()


def test_business_pass_and_finding_artifacts(tmp_path):
    passed = tmp_path / "business-pass.json"
    result = invoke("validate_business_rules.py", SAMPLE, passed)
    assert result.returncode == 0 and result.stdout.strip() == "PASS"
    assert read(passed)["findings"] == []

    records = json.loads(SAMPLE.read_text(encoding="utf-8-sig"))
    records[0]["venue"] = ""
    source = tmp_path / "records.json"
    source.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    failed = tmp_path / "business-fail.json"
    result = invoke("validate_business_rules.py", source, failed)
    item = read(failed)["findings"][0]
    assert result.returncode == 1 and "FAIL" in result.stdout
    assert set(item) == {"index", "activity_id", "rule_id", "field", "path", "severity", "message", "recommendation"}


@pytest.mark.parametrize("tool", ["validate_schema.py", "validate_business_rules.py"])
def test_unavailable_activity_id_uses_missing_marker(tool, tmp_path):
    records = json.loads(SAMPLE.read_text(encoding="utf-8-sig"))
    records[0]["activity_id"] = None
    records[0]["venue"] = ""
    source = tmp_path / "records.json"
    source.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "findings.json"
    result = invoke(tool, source, output)
    assert result.returncode == 1
    assert read(output)["findings"][0]["activity_id"] == "<missing>"


def test_schema_file_error_mappings(monkeypatch, tmp_path):
    output = tmp_path / "schema-error.json"
    missing = tmp_path / "missing-schema.json"
    monkeypatch.setattr(validate_schema, "SCHEMA_PATH", missing)
    assert validate_schema.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    assert read(output)["error"] == {"type": "file_not_found", "target": "schema", "message": f"Schema file not found: {missing}"}

    invalid = tmp_path / "invalid-schema.json"
    invalid.write_text("{bad", encoding="utf-8")
    monkeypatch.setattr(validate_schema, "SCHEMA_PATH", invalid)
    assert validate_schema.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    assert read(output)["error"]["type"] == "invalid_json"


def test_invalid_schema_mapping(monkeypatch, tmp_path):
    schema = tmp_path / "schema.json"
    schema.write_text(json.dumps({"type": 7}), encoding="utf-8")
    output = tmp_path / "error.json"
    monkeypatch.setattr(validate_schema, "SCHEMA_PATH", schema)
    assert validate_schema.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    assert read(output)["error"]["type"] == "invalid_schema"
    assert read(output)["error"]["target"] == "schema"


def test_schema_read_error_mappings(monkeypatch, tmp_path):
    output = tmp_path / "error.json"
    original = validate_schema.load_json

    def fail_schema(path):
        if path == validate_schema.SCHEMA_PATH:
            raise PermissionError("denied")
        return original(path)

    monkeypatch.setattr(validate_schema, "load_json", fail_schema)
    assert validate_schema.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    assert read(output)["error"]["type"] == "unreadable_file"
    assert read(output)["error"]["target"] == "schema"


@pytest.mark.parametrize("module", [validate_schema, validate_business_rules])
def test_input_read_error_mapping(monkeypatch, module, tmp_path):
    output = tmp_path / "error.json"
    original = module.load_json

    def fail_input(path):
        if Path(path) == SAMPLE:
            raise OSError("read failed")
        return original(path)

    monkeypatch.setattr(module, "load_json", fail_input)
    assert module.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    assert read(output)["error"]["type"] == "unreadable_file"
    assert read(output)["error"]["target"] == "input"


@pytest.mark.parametrize("module", [validate_schema, validate_business_rules])
def test_unexpected_runtime_error_writes_execution_error(monkeypatch, module, tmp_path):
    output = tmp_path / "runtime.json"
    monkeypatch.setattr(module, "load_json", lambda path: (_ for _ in ()).throw(RuntimeError("boom")))
    assert module.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    assert read(output)["error"]["type"] == "execution_error"
    assert read(output)["error"]["target"] == "runtime"


def test_business_helper_bypass_fails_closed(monkeypatch, tmp_path):
    class BadRule:
        RULE_ID = "BR-X"
        @staticmethod
        def check(record, index=0):
            return [{"index": index, "rule_id": "BR-X"}]

    output = tmp_path / "invariant.json"
    monkeypatch.setattr(validate_business_rules, "RULES", [BadRule])
    assert validate_business_rules.main([str(SAMPLE), "--run-id", RUN_ID, "--json-output", str(output)]) == 2
    artifact = read(output)
    assert artifact["findings"] == []
    assert "record index 0" in artifact["error"]["message"]
    assert "rule_id BR-X" in artifact["error"]["message"]
    assert "missing fields" in artifact["error"]["message"]


def test_active_rules_use_shared_finding_helper_and_br006_is_inactive():
    import inspect
    from validators.business_rules import RULES
    assert [rule.RULE_ID for rule in RULES] == ["BR-001", "BR-002", "BR-003", "BR-004", "BR-005"]
    for rule in RULES:
        source = inspect.getsource(rule)
        assert "from validators.business_rules.helpers import" in source
        assert "finding(" in source
