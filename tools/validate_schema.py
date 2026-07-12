import argparse
import json
import sys
from pathlib import Path

from jsonschema import exceptions, validators

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.validation_findings_json import (
    build_validation_artifact,
    valid_run_id,
    write_validation_artifact,
)


SCHEMA_PATH = ROOT_DIR / "schemas" / "activity.schema.json"
SCHEMA_RECOMMENDATION = (
    "Fix the JSON structure so the record validates against schemas/activity.schema.json."
)


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


def format_path(error_path) -> str:
    parts = list(error_path)
    if not parts:
        return "<record>"
    rendered = ""
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else (f".{part}" if rendered else str(part))
    return rendered


def top_level_field(path: str) -> str:
    if path == "<record>":
        return "<record>"
    indexes = [index for index in (path.find("["), path.find(".")) if index != -1]
    return path if not indexes else path[: min(indexes)]


def emit(args, status: str, findings: list, *, message=None, error=None) -> bool:
    if not args.json_output:
        return True
    artifact = build_validation_artifact(
        tool="schema_validator", run_id=args.run_id, status=status,
        source_artifact=args.input_json, findings=findings, message=message, error=error,
    )
    try:
        write_validation_artifact(Path(args.json_output), artifact)
    except OSError as exc:
        print_error(f"Could not write JSON artifact {args.json_output}: {exc}")
        return False
    return True


def execution_error(args, error_type: str, target: str, message: str) -> int:
    print_error(message)
    return 2 if emit(args, "error", [], error={"type": error_type, "target": target, "message": message}) else 2


def run(args) -> int:
    input_path = Path(args.input_json)
    try:
        schema = load_json(SCHEMA_PATH)
    except FileNotFoundError:
        return execution_error(args, "file_not_found", "schema", f"Schema file not found: {SCHEMA_PATH}")
    except json.JSONDecodeError as exc:
        return execution_error(args, "invalid_json", "schema", f"Invalid JSON in schema file {SCHEMA_PATH}: {exc.msg} at line {exc.lineno}, column {exc.colno}")
    except OSError as exc:
        return execution_error(args, "unreadable_file", "schema", f"Could not read schema file {SCHEMA_PATH}: {exc}")

    try:
        data = load_json(input_path)
    except FileNotFoundError:
        return execution_error(args, "file_not_found", "input", f"Input file not found: {input_path}")
    except json.JSONDecodeError as exc:
        return execution_error(args, "invalid_json", "input", f"Invalid JSON in input file {input_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}")
    except OSError as exc:
        return execution_error(args, "unreadable_file", "input", f"Could not read input file {input_path}: {exc}")

    if not isinstance(data, list):
        message = f"{input_path}: expected a JSON array of activity records."
        print("FAIL")
        print(message)
        return 1 if emit(args, "fail", [], message=message) else 2

    try:
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
    except exceptions.SchemaError as exc:
        return execution_error(args, "invalid_schema", "schema", f"Invalid schema in {SCHEMA_PATH}: {exc.message}")

    validator = validator_class(schema)
    failures = []
    for index, record in enumerate(data):
        activity_id = record.get("activity_id") if isinstance(record, dict) else None
        if not isinstance(activity_id, str) or not activity_id:
            activity_id = "<missing>"
        for error in sorted(validator.iter_errors(record), key=lambda item: (list(item.path), item.message)):
            path = format_path(error.path)
            failures.append({
                "index": index, "activity_id": activity_id, "rule_id": "SCHEMA",
                "field": top_level_field(path), "path": path, "severity": "critical",
                "message": error.message, "recommendation": SCHEMA_RECOMMENDATION,
            })

    if not failures:
        print("PASS")
        return 0 if emit(args, "pass", []) else 2
    print("FAIL")
    for failure in failures:
        print(f"Record {failure['index']} (activity_id: {failure['activity_id']}), rule_id: {failure['rule_id']}, field: {failure['field']}, path: {failure['path']}, severity: {failure['severity']}")
        print(f"Message: {failure['message']}")
        print(f"Recommendation: {failure['recommendation']}")
    return 1 if emit(args, "fail", failures) else 2


def main(argv=None) -> int:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Validate extracted activity records against schemas/activity.schema.json.")
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
        return execution_error(args, "execution_error", "runtime", f"Unexpected runtime failure: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
