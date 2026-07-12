import json
import re
from datetime import datetime, timezone
from pathlib import Path


CONTRACT_VERSION = "validation-findings-v1"
TOOLS = {"schema_validator", "business_validator"}
STATUSES = {"pass", "fail", "error"}
SEVERITIES = {"critical", "high", "medium", "low"}
ERROR_TYPES = {
    "file_not_found",
    "unreadable_file",
    "invalid_json",
    "invalid_schema",
    "execution_error",
}
ERROR_TARGETS = {"input", "schema", "runtime"}
FINDING_FIELDS = {
    "index",
    "activity_id",
    "rule_id",
    "field",
    "path",
    "severity",
    "message",
    "recommendation",
}
RUN_ID_PATTERN = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])-r(?:0[1-9]|[1-9]\d)$")


def valid_run_id(run_id: str) -> bool:
    return isinstance(run_id, str) and RUN_ID_PATTERN.fullmatch(run_id) is not None


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_finding_contract(finding: object) -> list[str]:
    if not isinstance(finding, dict):
        return ["finding must be an object"]

    problems = []
    missing = FINDING_FIELDS - finding.keys()
    extra = finding.keys() - FINDING_FIELDS
    if missing:
        problems.append(f"missing fields: {', '.join(sorted(missing))}")
    if extra:
        problems.append(f"invalid fields: {', '.join(sorted(extra))}")

    index = finding.get("index")
    if isinstance(index, bool) or not isinstance(index, int) or index < 0:
        problems.append("index must be a non-negative integer")
    for field in FINDING_FIELDS - {"index", "severity"}:
        value = finding.get(field)
        if not isinstance(value, str) or not value:
            problems.append(f"{field} must be a non-empty string")
    if finding.get("rule_id") == "<missing>":
        problems.append("rule_id must not be <missing>")
    if finding.get("severity") not in SEVERITIES:
        problems.append("severity must be critical, high, medium, or low")
    return problems


def build_validation_artifact(
    *, tool: str, run_id: str, status: str, source_artifact: str,
    findings: list, message: str | None = None, error: dict | None = None,
) -> dict:
    artifact = {
        "contract_version": CONTRACT_VERSION,
        "tool": tool,
        "run_id": run_id,
        "status": status,
        "generated_at": utc_timestamp(),
        "source_artifact": source_artifact,
        "findings": findings,
    }
    if message is not None:
        artifact["message"] = message
    if error is not None:
        artifact["error"] = error
    validate_validation_artifact(artifact)
    return artifact


def validate_validation_artifact(artifact: object) -> None:
    if not isinstance(artifact, dict):
        raise ValueError("artifact must be an object")
    required = {
        "contract_version", "tool", "run_id", "status", "generated_at",
        "source_artifact", "findings",
    }
    missing = required - artifact.keys()
    if missing:
        raise ValueError(f"missing top-level fields: {', '.join(sorted(missing))}")
    if artifact["contract_version"] != CONTRACT_VERSION:
        raise ValueError("invalid contract_version")
    if artifact["tool"] not in TOOLS:
        raise ValueError("invalid tool")
    if not valid_run_id(artifact["run_id"]):
        raise ValueError("invalid run_id")
    if artifact["status"] not in STATUSES:
        raise ValueError("invalid status")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", artifact["generated_at"]):
        raise ValueError("invalid generated_at")
    if not isinstance(artifact["source_artifact"], str):
        raise ValueError("source_artifact must be a string")
    if not isinstance(artifact["findings"], list):
        raise ValueError("findings must be an array")
    for finding in artifact["findings"]:
        problems = validate_finding_contract(finding)
        if problems:
            raise ValueError("invalid finding: " + "; ".join(problems))

    status = artifact["status"]
    if status == "pass" and artifact["findings"]:
        raise ValueError("pass findings must be empty")
    if status in {"pass", "fail"} and "error" in artifact:
        raise ValueError("error must be absent for pass or fail")
    if status == "fail" and not artifact["findings"] and not artifact.get("message"):
        raise ValueError("message is required for fail with empty findings")
    if status == "error":
        if artifact["findings"]:
            raise ValueError("error findings must be empty")
        error = artifact.get("error")
        if not isinstance(error, dict) or set(error) != {"type", "target", "message"}:
            raise ValueError("error object must contain type, target, and message")
        if error["type"] not in ERROR_TYPES or error["target"] not in ERROR_TARGETS:
            raise ValueError("invalid error type or target")
        if not isinstance(error["message"], str) or not error["message"]:
            raise ValueError("error message must be a non-empty string")


def write_validation_artifact(path: Path, artifact: dict) -> None:
    validate_validation_artifact(artifact)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(artifact, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
