"""Test-support mutation engine. The ordinary verifier never imports this module."""

import copy
import json
import shutil
from pathlib import Path
from typing import Any

from .canonical import identity_sha256, sha256
from .errors import VerificationFailure, VerificationResult
from .lifecycle import LIFECYCLE_STAGES, validate_lifecycle_stage_order


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _pointer(value: Any, pointer: str):
    parts = pointer.strip("/").split("/") if pointer else []
    parent = value
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


def _set(value: Any, pointer: str, replacement: Any) -> None:
    parent, key = _pointer(value, pointer)
    if isinstance(parent, list):
        parent.append(copy.deepcopy(replacement)) if key == "-" else parent.__setitem__(int(key), copy.deepcopy(replacement))
    else:
        parent[key] = copy.deepcopy(replacement)


def _remove(value: Any, pointer: str) -> None:
    parent, key = _pointer(value, pointer)
    parent.pop(int(key)) if isinstance(parent, list) else parent.pop(key)


def _artifact_type(value: dict[str, Any]) -> str:
    if "authority_id" in value:
        return (
            "registry-publication-envelope"
            if value.get("authority_purpose") == "calendar-registry-publication"
            else "authority-envelope"
        )
    return {
        "authority-revocation-subject/0.1.0-draft": "authority-revocation-subject",
        "calendar-eligibility-subject/0.3.0-draft": "calendar-eligibility-subject",
        "calendar-monthly-selection-subject/0.3.0-draft": "calendar-monthly-selection-subject",
        "registry-publication-subject/0.1.0-draft": "registry-publication-subject",
        "authority-registry-snapshot/0.2.0-draft": "registry-snapshot",
        "run-metadata-binding-subject/0.2.0-draft": "run-metadata-binding-subject",
    }[value["contract_version"]]


def _logical_id(value: dict[str, Any]) -> str:
    return value.get("authority_id") or value.get("subject_id") or value["snapshot_id"]


def _rebuild_bundle(state: dict[str, dict[str, Any]]) -> None:
    root = state["resolution-bundle-root.json"]
    inventory = []
    for name, value in state.items():
        if name in {"resolution-bundle-root.json", "trust-anchor.json"}:
            continue
        inventory.append({
            "artifact_type": _artifact_type(value),
            "logical_id": _logical_id(value),
            "artifact_path": name,
            "artifact_sha256": sha256(value),
        })
    inventory.sort(key=lambda item: (item["artifact_type"], item["logical_id"], item["artifact_path"]))
    root["artifact_inventory"] = inventory
    root["bundle_id"] = "bundle_sha256_" + identity_sha256(root, "bundle_id")


def _cascade(state: dict[str, dict[str, Any]], tokens: list[str], changed: str) -> None:
    snapshot = state["registry-snapshot.json"]
    changed_value = state.get(changed)
    subject_changed = isinstance(changed_value, dict) and "subject_id" in changed_value and "authority_id" not in changed_value
    if "subject_artifact_sha256" in tokens and subject_changed:
        for value in state.values():
            if value.get("authority_id") and value.get("subject_id") == changed_value["subject_id"]:
                value["subject_sha256"] = sha256(changed_value)
    if "authority_envelope_artifact_sha256" in tokens or "snapshot_entries" in tokens:
        envelopes = {v["authority_id"]: v for v in state.values() if v.get("authority_id")}
        for entry in snapshot["entries"]:
            envelope = envelopes.get(entry["authority_id"])
            if envelope is None:
                continue
            entry["authority_artifact_sha256"] = sha256(envelope)
            if subject_changed:
                entry["subject_sha256"] = envelope["subject_sha256"]
    if "publication_subject_sha256" in tokens:
        subject = state["registry-publication-subject.json"]
        subject["entries"] = copy.deepcopy(snapshot["entries"])
        envelope = state["registry-publication-envelope.json"]
        envelope["subject_sha256"] = sha256(subject)
        snapshot["publication_subject_sha256"] = sha256(subject)
    if "publication_envelope_artifact_sha256" in tokens:
        snapshot["publication_authority_artifact_sha256"] = sha256(state["registry-publication-envelope.json"])
    if "complete_snapshot_artifact_sha256" in tokens:
        state["resolution-bundle-root.json"]["snapshot_artifact_sha256"] = sha256(snapshot)
    if "bundle_inventory" in tokens:
        _rebuild_bundle(state)
    elif "bundle_id" in tokens:
        root = state["resolution-bundle-root.json"]
        root["bundle_id"] = "bundle_sha256_" + identity_sha256(root, "bundle_id")
    if "trust_anchor_snapshot_binding" in tokens:
        state["trust-anchor.json"]["expected_snapshot_artifact_sha256"] = sha256(snapshot)


def materialize_case(case: dict[str, Any], source: Path, target: Path) -> tuple[Path, Path]:
    if case["fixture_id"] == "OAR-N15":
        raise ValueError("OAR-N15 is construction-invariant only.")
    if any(operation["artifact_path"] == "$resolution-context" for operation in case["mutation"]["ordered_operations"]):
        raise ValueError("Symbolic context is authorized only for OAR-N15.")
    shutil.copytree(source, target)
    state = {path.name: _load(path) for path in target.glob("*.json")}
    for operation in case["mutation"]["ordered_operations"]:
        name = operation["artifact_path"]
        op = operation["operation"]
        if op == "replace_value":
            _set(state[name], operation["json_pointer"], operation["value"])
        elif op == "remove_artifact":
            if "json_pointer" in operation:
                _remove(state[name], operation["json_pointer"])
            else:
                state.pop(name)
            if operation.get("remove_bundle_declaration"):
                root = state["resolution-bundle-root.json"]
                root["artifact_inventory"] = [
                    item for item in root["artifact_inventory"] if item["artifact_path"] != name
                ]
        elif op == "add_artifact":
            if "json_pointer" in operation:
                value = operation.get("value")
                if operation.get("derive_from_artifact"):
                    envelope = state[operation["derive_from_artifact"]]
                    value = {
                        "subject_type": envelope["subject_type"],
                        "subject_id": envelope["subject_id"],
                        "subject_sha256": envelope["subject_sha256"],
                        "authority_id": envelope["authority_id"],
                        "authority_purpose": envelope["authority_purpose"],
                        "authority_artifact_sha256": sha256(envelope),
                        **operation.get("entry_overrides", {}),
                    }
                _set(state[name], operation["json_pointer"], value)
            else:
                value = copy.deepcopy(state[operation["template_artifact_path"]])
                value.update(operation.get("overrides", {}))
                state[name] = value
        elif op == "duplicate_artifact":
            parent, key = _pointer(state[name], operation["json_pointer"])
            item = copy.deepcopy(parent[int(key)])
            item.update(operation.get("overrides", {}))
            parent.insert(int(key) + 1, item)
        elif op == "reorder_array":
            parent, key = _pointer(state[name], operation["json_pointer"])
            array = parent[key]
            parent[key] = [array[index] for index in operation["value"]]
        else:
            raise ValueError(f"Unknown mutation operation: {op}")
        if operation.get("rebuild_bundle"):
            _rebuild_bundle(state)
        if operation.get("recompute_dependents"):
            _cascade(state, operation["recompute_dependents"], name)
    for path in target.glob("*.json"):
        if path.name not in state:
            path.unlink()
    for name, value in state.items():
        _write(target / name, value)
    return target / "resolution-bundle-root.json", target / "trust-anchor.json"


def validate_n15(case: dict[str, Any]) -> VerificationResult:
    if case["fixture_id"] != "OAR-N15":
        raise ValueError("Construction-invariant exception applies only to OAR-N15.")
    operations = case["mutation"]["ordered_operations"]
    if len(operations) != 1 or operations[0].get("artifact_path") != "$resolution-context":
        raise ValueError("OAR-N15 must contain exactly one symbolic context mutation.")
    mutated = list(LIFECYCLE_STAGES)
    requested = operations[0]["value"]
    mapping = {
        "revocation": "authorized-revocation-resolution",
        "authority-supersession": "authority-supersession-resolution",
        "business-subject-supersession": "business-subject-supersession-resolution",
    }
    projected = tuple(mapping[value] for value in requested)
    mutated[: len(projected)] = projected
    try:
        validate_lifecycle_stage_order(tuple(mutated))
    except VerificationFailure as failure:
        return failure.result
    raise AssertionError("OAR-N15 symbolic mutation unexpectedly satisfied the fixed invariant.")
