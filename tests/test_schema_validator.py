import json
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT_DIR / "tools" / "validate_schema.py"
SAMPLE_OUTPUT = ROOT_DIR / "examples" / "sample-output.json"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_sample_output_passes_schema_validation():
    result = run_validator(SAMPLE_OUTPUT)

    assert result.returncode == 0
    assert result.stdout.strip() == "PASS"
    assert result.stderr == ""


def test_invalid_schema_sample_fails_validation(tmp_path):
    records = json.loads(SAMPLE_OUTPUT.read_text(encoding="utf-8").lstrip("\ufeff"))
    records[0]["quota"] = 30
    broken_sample = tmp_path / "broken-sample-output.json"
    broken_sample.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")

    result = run_validator(broken_sample)

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "rule_id: SCHEMA" in result.stdout
    assert "field: quota" in result.stdout
    assert result.stderr == ""


def test_missing_file_returns_tool_execution_error(tmp_path):
    missing_file = tmp_path / "missing-file.json"

    result = run_validator(missing_file)

    assert result.returncode == 2
    assert result.stdout == ""
    assert "ERROR:" in result.stderr