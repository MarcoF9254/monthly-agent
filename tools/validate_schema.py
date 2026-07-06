import argparse
import json
import sys
from pathlib import Path

from jsonschema import exceptions
from jsonschema import validators


ROOT_DIR = Path(__file__).resolve().parents[1]
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
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}" if rendered else str(part)
    return rendered


def top_level_field(path: str) -> str:
    if path == "<record>":
        return "<record>"

    bracket_index = path.find("[")
    dot_index = path.find(".")
    indexes = [index for index in (bracket_index, dot_index) if index != -1]
    if not indexes:
        return path
    return path[: min(indexes)]


def main() -> int:
    configure_stdout()

    parser = argparse.ArgumentParser(
        description="Validate extracted activity records against schemas/activity.schema.json."
    )
    parser.add_argument("input_json", help="Path to a JSON file containing an array of activity records.")
    args = parser.parse_args()

    input_path = Path(args.input_json)

    try:
        schema = load_json(SCHEMA_PATH)
    except FileNotFoundError:
        print_error(f"Schema file not found: {SCHEMA_PATH}")
        return 2
    except PermissionError:
        print_error(f"Schema file is not readable: {SCHEMA_PATH}")
        return 2
    except json.JSONDecodeError as error:
        print_error(
            f"Invalid JSON in schema file {SCHEMA_PATH}: "
            f"{error.msg} at line {error.lineno}, column {error.colno}"
        )
        return 2
    except OSError as error:
        print_error(f"Could not read schema file {SCHEMA_PATH}: {error}")
        return 2

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

    try:
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
    except exceptions.SchemaError as error:
        print_error(f"Invalid schema in {SCHEMA_PATH}: {error.message}")
        return 2

    validator = validator_class(schema)

    failures = []
    for index, record in enumerate(data):
        activity_id = record.get("activity_id", "<missing>") if isinstance(record, dict) else "<missing>"
        errors = sorted(
            validator.iter_errors(record),
            key=lambda error: (list(error.path), error.message),
        )

        for error in errors:
            path = format_path(error.path)
            failures.append(
                {
                    "index": index,
                    "activity_id": activity_id,
                    "rule_id": "SCHEMA",
                    "field": top_level_field(path),
                    "path": path,
                    "severity": "critical",
                    "message": error.message,
                    "recommendation": SCHEMA_RECOMMENDATION,
                }
            )

    if not failures:
        print("PASS")
        return 0

    print("FAIL")
    for failure in failures:
        print(
            f"Record {failure['index']} "
            f"(activity_id: {failure['activity_id']}), "
            f"rule_id: {failure['rule_id']}, "
            f"field: {failure['field']}, "
            f"path: {failure['path']}, "
            f"severity: {failure['severity']}"
        )
        print(f"Message: {failure['message']}")
        print(f"Recommendation: {failure['recommendation']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())