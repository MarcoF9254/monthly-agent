from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import identity_sha256, load_json, sha256
from .errors import reject
from .limits import (
    enforce_file_bytes,
    enforce_inventory_count,
    enforce_snapshot_entries,
    enforce_total_bytes,
)
from .schema_validation import SchemaSet


FICTIONAL_SCOPE = {
    "run_id": "fictional-run-2099-01-oar",
    "consumer_id": "calendar-renderer",
    "programme_month": "2099-01",
    "registry_purpose": "calendar-authority-resolution",
}


@dataclass
class Scenario:
    root: Path
    anchor_path: Path
    anchor: dict[str, Any]
    bundle_path: Path
    bundle: dict[str, Any]
    artifacts: dict[str, dict[str, Any]]
    inventory: list[dict[str, Any]]

    def by_contract(self, version: str) -> list[dict[str, Any]]:
        return [value for value in self.artifacts.values() if value.get("contract_version") == version]

    def by_authority_id(self, authority_id: str) -> dict[str, Any] | None:
        return next((v for v in self.artifacts.values() if v.get("authority_id") == authority_id), None)

    def by_subject_id(self, subject_id: str) -> dict[str, Any] | None:
        return next(
            (v for v in self.artifacts.values() if v.get("subject_id") == subject_id and "authority_id" not in v),
            None,
        )


def _contained(root: Path, path: Path) -> Path:
    if path.is_absolute():
        reject("PROTO-FS-002", "Bundle verifier", "filesystem-admission", "Absolute inventory path prohibited.")
    resolved = (root / path).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        reject("PROTO-FS-003", "Bundle verifier", "filesystem-admission", "Inventory path escapes scenario root.")
    return resolved


def _exact_scope(value: Any) -> None:
    if value != FICTIONAL_SCOPE:
        reject("PROTO-SCOPE-001", "Operational caller", "fictional-scope-admission", "Prototype accepts only the exact fictional 2099 scope.")


def load_scenario(
    repository_root: Path,
    scenario_root: Path,
    bundle_root_path: Path,
    trust_anchor_path: Path,
) -> Scenario:
    root = scenario_root.resolve(strict=True)
    bundle_path = bundle_root_path.resolve(strict=True)
    if not trust_anchor_path.exists():
        reject("BAI-TA-001", "Operational caller", "production-admission", "External trust anchor is missing.")
    anchor_path = trust_anchor_path.resolve(strict=True)
    bundle_bytes = bundle_path.stat().st_size
    anchor_bytes = anchor_path.stat().st_size
    enforce_file_bytes(bundle_bytes)
    enforce_file_bytes(anchor_bytes)
    admitted_bytes = bundle_bytes + anchor_bytes
    enforce_total_bytes(admitted_bytes)
    for supplied in (bundle_path, anchor_path):
        try:
            supplied.relative_to(root)
        except ValueError:
            reject("PROTO-FS-003", "Bundle verifier", "filesystem-admission", "Supplied input escapes scenario root.")
        if supplied.is_symlink():
            reject("PROTO-FS-004", "Bundle verifier", "filesystem-admission", "Symlink input prohibited.")
    schemas = SchemaSet(repository_root)
    bundle = load_json(bundle_path)
    anchor = load_json(anchor_path)
    schemas.validate(bundle, "bundle-root")
    schemas.validate(anchor, "trust-anchor")
    _exact_scope(bundle.get("scope"))
    _exact_scope(anchor.get("scope"))

    inventory = bundle["artifact_inventory"]
    enforce_inventory_count(len(inventory))
    logical = {}
    physical = set()
    for item in inventory:
        logical_id = item["logical_id"]
        if logical_id in logical:
            reject("BAI-BV-003", "Bundle verifier", "bundle-logical-identity", "Duplicate or conflicting logical identity.")
        logical[logical_id] = item["artifact_sha256"]
        path = Path(item["artifact_path"])
        if path in physical:
            reject("PROTO-FS-005", "Bundle verifier", "bundle-logical-identity", "Duplicate physical artifact path.")
        physical.add(path)

    artifacts = {}
    resolved_declared = set()
    for item in inventory:
        relative = Path(item["artifact_path"])
        resolved = _contained(root, relative)
        if not resolved.exists() or not resolved.is_file():
            reject("BAI-BV-001", "Bundle verifier", "bundle-completeness", "Declared artifact is missing.")
        if resolved.is_symlink():
            reject("PROTO-FS-004", "Bundle verifier", "filesystem-admission", "Symlink artifact prohibited.")
        resolved = resolved.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError:
            reject("PROTO-FS-003", "Bundle verifier", "filesystem-admission", "Resolved artifact escapes scenario root.")
        resolved_declared.add(resolved)
        artifact_bytes = resolved.stat().st_size
        enforce_file_bytes(artifact_bytes)
        admitted_bytes += artifact_bytes
        enforce_total_bytes(admitted_bytes)
        artifact = load_json(resolved)
        if artifact.get("contract_version") == "authority-registry-snapshot/0.2.0-draft":
            enforce_snapshot_entries(len(artifact.get("entries", [])))
        schemas.validate(artifact, "bundle-artifact", item["artifact_type"])
        artifacts[item["artifact_path"]] = artifact

    external = {anchor_path, bundle_path}
    visible = {
        path.resolve(strict=True)
        for path in root.rglob("*.json")
        if path.resolve(strict=True) not in external
    }
    if visible - resolved_declared:
        reject("BAI-BV-002", "Bundle verifier", "bundle-completeness", "Undeclared physical JSON artifact.")
    if resolved_declared - visible:
        reject("BAI-BV-001", "Bundle verifier", "bundle-completeness", "Declared artifact is missing.")

    for item in inventory:
        if sha256(artifacts[item["artifact_path"]]) != item["artifact_sha256"]:
            reject("BAI-BV-005", "Bundle verifier", "bundle-hash-verification", "Declared artifact digest mismatch.")

    keys = [(i["artifact_type"], i["logical_id"], i["artifact_path"]) for i in inventory]
    if keys != sorted(keys):
        reject("BAI-BV-004", "Bundle verifier", "bundle-ordering", "Bundle inventory is not canonical.")
    expected_bundle = "bundle_sha256_" + identity_sha256(bundle, "bundle_id")
    if bundle["bundle_id"] != expected_bundle:
        reject("PROTO-BUNDLE-001", "Bundle verifier", "bundle-identity", "Bundle identity digest mismatch.")

    return Scenario(root, anchor_path, anchor, bundle_path, bundle, artifacts, inventory)
