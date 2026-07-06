import argparse
import json
import sys
from pathlib import Path

from jsonschema import validators


ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "schemas" / "activity.schema.json"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.loads(handle.read().lstrip("\ufeff"))


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


def main() -> int:
    configure_stdout()

    parser = argparse.ArgumentParser(
        description="Validate extracted activity records against schemas/activity.schema.json."
    )
    parser.add_argument("input_json", help="Path to a JSON file containing an array of activity records.")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    schema = load_json(SCHEMA_PATH)
    data = load_json(input_path)

    if not isinstance(data, list):
        print("FAIL")
        print(f"{input_path}: expected a JSON array of activity records.")
        return 1

    validator_class = validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)

    failures = []
    for index, record in enumerate(data):
        activity_id = record.get("activity_id", "<missing>") if isinstance(record, dict) else "<missing>"
        errors = sorted(
            validator.iter_errors(record),
            key=lambda error: (list(error.path), error.message),
        )

        for error in errors:
            failures.append(
                {
                    "index": index,
                    "activity_id": activity_id,
                    "path": format_path(error.path),
                    "message": error.message,
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
            f"path: {failure['path']}: {failure['message']}"
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
