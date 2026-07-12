import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.validation_findings_json import (
    build_validation_artifact,
    valid_run_id,
    validate_finding_contract,
    write_validation_artifact,
)
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


def emit(args, status: str, findings: list, *, message=None, error=None) -> bool:
    if not args.json_output:
        return True
    artifact = build_validation_artifact(
        tool="business_validator", run_id=args.run_id, status=status,
        source_artifact=args.input_json, findings=findings, message=message, error=error,
    )
    try:
        write_validation_artifact(Path(args.json_output), artifact)
    except OSError as exc:
        print_error(f"Could not write JSON artifact {args.json_output}: {exc}")
        return False
    return True


def execution_error(args, message: str, error_type="execution_error", target="runtime") -> int:
    print_error(message)
    emit(args, "error", [], error={"type": error_type, "target": target, "message": message})
    return 2


def run(args) -> int:
    input_path = Path(args.input_json)
    try:
        data = load_json(input_path)
    except FileNotFoundError:
        return execution_error(args, f"Input file not found: {input_path}", "file_not_found", "input")
    except json.JSONDecodeError as exc:
        return execution_error(args, f"Invalid JSON in input file {input_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}", "invalid_json", "input")
    except OSError as exc:
        return execution_error(args, f"Could not read input file {input_path}: {exc}", "unreadable_file", "input")

    if not isinstance(data, list):
        message = f"{input_path}: expected a JSON array of activity records."
        print("FAIL")
        print(message)
        return 1 if emit(args, "fail", [], message=message) else 2

    findings = []
    for index, record in enumerate(data):
        for rule in RULES:
            for result in rule.check(record, index=index):
                problems = validate_finding_contract(result)
                if problems:
                    rule_id = result.get("rule_id") if isinstance(result, dict) else None
                    identity = rule_id or getattr(rule, "RULE_ID", "<unavailable>")
                    message = f"Internal finding invariant failure at record index {index}, rule_id {identity}: {'; '.join(problems)}"
                    return execution_error(args, message)
                findings.append(result)

    if not findings:
        print("PASS")
        return 0 if emit(args, "pass", []) else 2
    print("FAIL")
    for finding in findings:
        print(f"Record {finding['index']} (activity_id: {finding['activity_id']}), rule_id: {finding['rule_id']}, field: {finding['field']}, path: {finding['path']}, severity: {finding['severity']}")
        print(f"Message: {finding['message']}")
        print(f"Recommendation: {finding['recommendation']}")
    return 1 if emit(args, "fail", findings) else 2


def main(argv=None) -> int:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Validate extracted activity records against monthly-agent business rules.")
    parser.add_argument("input_json", help="Path to a JSON file containing an array of activity records.")
    parser.add_argument("--run-id")
    parser.add_argument("--json-output")
    args = parser.parse_args(argv)
    if args.json_output and not args.run_id:
        parser.error("--run-id is required when --json-output is provided")
    if args.run_id and not valid_run_id(args.run_id):
        parser.error("--run-id must use YYYY-MM-rNN with r01 or greater")
    try:
        return run(args)
    except Exception as exc:
        return execution_error(args, f"Unexpected runtime failure: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
