"""Central deterministic resource limits for the fictional verifier."""

from .errors import reject_resource

MAX_ARTIFACT_INVENTORY = 64
MAX_JSON_FILE_BYTES = 256 * 1024
MAX_TOTAL_JSON_BYTES = 2 * 1024 * 1024
MAX_SNAPSHOT_ENTRIES = 256
MAX_LIFECYCLE_DEPTH = 64


def enforce_limit(value: int, maximum: int, rule_id: str, component: str, stage: str, message: str) -> None:
    if value > maximum:
        reject_resource(rule_id, component, stage, message)


def enforce_inventory_count(value: int) -> None:
    enforce_limit(value, MAX_ARTIFACT_INVENTORY, "PROTO-RESOURCE-INVENTORY", "Bundle verifier", "resource-admission", "Artifact inventory limit exceeded.")


def enforce_file_bytes(value: int) -> None:
    enforce_limit(value, MAX_JSON_FILE_BYTES, "PROTO-RESOURCE-FILE-BYTES", "Bundle verifier", "resource-admission", "Individual JSON byte limit exceeded.")


def enforce_total_bytes(value: int) -> None:
    enforce_limit(value, MAX_TOTAL_JSON_BYTES, "PROTO-RESOURCE-TOTAL-BYTES", "Bundle verifier", "resource-admission", "Total admitted JSON byte limit exceeded.")


def enforce_snapshot_entries(value: int) -> None:
    enforce_limit(value, MAX_SNAPSHOT_ENTRIES, "PROTO-RESOURCE-SNAPSHOT-ENTRIES", "Registry snapshot validator", "resource-admission", "Snapshot entry limit exceeded.")


def enforce_lifecycle_depth(value: int) -> None:
    enforce_limit(value, MAX_LIFECYCLE_DEPTH, "PROTO-RESOURCE-LIFECYCLE-DEPTH", "Authority lifecycle resolver", "resource-admission", "Lifecycle traversal depth exceeded.")
