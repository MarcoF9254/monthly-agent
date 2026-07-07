import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from validators.business_rules import RULES


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.loads(handle.read().lstrip("\ufeff"))


def print_error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def activity_id_for(record) -> str:
    if isinstance(record, dict):
        return record.get("activity_id", "<missing>")
    return "<missing>"


def normalize_finding(finding: dict, index: int, record) -> dict:
    return {
        "index": finding.get("index", index),
        "activity_id": finding.get("activity_id", activity_id_for(record)),
        "rule_id": finding.get("rule_id", "<missing>"),
        "field": finding.get("field", "<record>"),
        "path": finding.get("path", "<record>"),
        "severity": finding.get("severity", "high"),
        "message": finding.get("message", ""),
        "recommendation": finding.get("recommendation", ""),
    }


def main() -> int:
    configure_stdout()

    parser = argparse.ArgumentParser(
        description="Validate extracted activity records against monthly-agent business rules."
    )
    parser.add_argument("input_json", help="Path to a JSON file containing an array of activity records.")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    try:
        data = load_json(input_path)
    except FileNotFoundError:
        print_error(f"Input file not found: {input_path}")
        return 2
    except PermissionError:
        print_error(f"Input file is not readable: {input_path}")
        return 2
    except json.JSONDecodeError as error:
        print_error(
            f"Invalid JSON in input file {input_path}: "
            f"{error.msg} at line {error.lineno}, column {error.colno}"
        )
        return 2
    except OSError as error:
        print_error(f"Could not read input file {input_path}: {error}")
        return 2

    if not isinstance(data, list):
        print("FAIL")
        print(f"{input_path}: expected a JSON array of activity records.")
        return 1

    findings = []
    for index, record in enumerate(data):
        for rule in RULES:
            for finding in rule.check(record, index=index):
                findings.append(normalize_finding(finding, index, record))

    if not findings:
        print("PASS")
        return 0

    print("FAIL")
    for finding in findings:
        print(
            f"Record {finding['index']} "
            f"(activity_id: {finding['activity_id']}), "
            f"rule_id: {finding['rule_id']}, "
            f"field: {finding['field']}, "
            f"path: {finding['path']}, "
            f"severity: {finding['severity']}"
        )
        print(f"Message: {finding['message']}")
        print(f"Recommendation: {finding['recommendation']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

