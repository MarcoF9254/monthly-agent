import json
import shutil
from pathlib import Path

import pytest

from tools.oar_verifier.errors import VerificationFailure
from tools.oar_verifier.limits import (
    MAX_ARTIFACT_INVENTORY,
    MAX_JSON_FILE_BYTES,
    MAX_LIFECYCLE_DEPTH,
    MAX_SNAPSHOT_ENTRIES,
    MAX_TOTAL_JSON_BYTES,
    enforce_file_bytes,
    enforce_inventory_count,
    enforce_lifecycle_depth,
    enforce_snapshot_entries,
    enforce_total_bytes,
)
from tools.oar_verifier.verifier import verify
import tools.oar_verifier.limits as limits


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "contract-fixtures" / "owner-authority-resolution" / "positive" / "pre-revocation"


@pytest.mark.parametrize(
    ("function", "maximum"),
    [
        (enforce_inventory_count, MAX_ARTIFACT_INVENTORY),
        (enforce_file_bytes, MAX_JSON_FILE_BYTES),
        (enforce_total_bytes, MAX_TOTAL_JSON_BYTES),
        (enforce_snapshot_entries, MAX_SNAPSHOT_ENTRIES),
        (enforce_lifecycle_depth, MAX_LIFECYCLE_DEPTH),
    ],
)
def test_resource_limit_boundary_passes_and_plus_one_rejects(function, maximum):
    function(maximum)
    with pytest.raises(VerificationFailure) as captured:
        function(maximum + 1)
    result = captured.value.result
    assert not result.success
    assert result.classification == "resource_rejection"
    assert result.rejection_stage == "resource-admission"


def test_individual_file_limit_is_enforced_by_ordinary_verifier(tmp_path):
    target = tmp_path / "scenario"
    shutil.copytree(SOURCE, target)
    anchor = target / "trust-anchor.json"
    original = anchor.read_bytes()
    anchor.write_bytes(original + b" " * (MAX_JSON_FILE_BYTES + 1 - len(original)))
    result = verify(ROOT, target, target / "resolution-bundle-root.json", anchor)
    assert not result.success
    assert result.classification == "resource_rejection"
    assert result.rule_id == "PROTO-RESOURCE-FILE-BYTES"


def _copy_scenario(tmp_path):
    target = tmp_path / "scenario"
    shutil.copytree(SOURCE, target)
    return target


def _verify(target):
    return verify(ROOT, target, target / "resolution-bundle-root.json", target / "trust-anchor.json")


def _inventory(target):
    return json.loads((target / "resolution-bundle-root.json").read_text(encoding="utf-8"))["artifact_inventory"]


def _total_admitted_bytes(target):
    inventory = _inventory(target)
    paths = [target / "resolution-bundle-root.json", target / "trust-anchor.json"]
    paths.extend(target / item["artifact_path"] for item in inventory)
    return sum(path.stat().st_size for path in paths)


@pytest.mark.parametrize(
    ("constant", "measurement", "rule_id"),
    [
        ("MAX_ARTIFACT_INVENTORY", lambda target: len(_inventory(target)), "PROTO-RESOURCE-INVENTORY"),
        (
            "MAX_JSON_FILE_BYTES",
            lambda target: max(
                [
                    (target / "resolution-bundle-root.json").stat().st_size,
                    (target / "trust-anchor.json").stat().st_size,
                    *((target / item["artifact_path"]).stat().st_size for item in _inventory(target)),
                ]
            ),
            "PROTO-RESOURCE-FILE-BYTES",
        ),
        ("MAX_TOTAL_JSON_BYTES", _total_admitted_bytes, "PROTO-RESOURCE-TOTAL-BYTES"),
        (
            "MAX_SNAPSHOT_ENTRIES",
            lambda target: len(
                json.loads((target / "registry-snapshot.json").read_text(encoding="utf-8"))["entries"]
            ),
            "PROTO-RESOURCE-SNAPSHOT-ENTRIES",
        ),
    ],
)
def test_admission_limit_boundary_and_plus_one_use_ordinary_verifier(
    tmp_path, monkeypatch, constant, measurement, rule_id
):
    target = _copy_scenario(tmp_path)
    exact_boundary = measurement(target)

    monkeypatch.setattr(limits, constant, exact_boundary)
    passed = _verify(target)
    assert passed.success
    assert passed.classification == "success"

    monkeypatch.setattr(limits, constant, exact_boundary - 1)
    rejected = _verify(target)
    assert not rejected.success
    assert rejected.classification == "resource_rejection"
    assert rejected.rule_id == rule_id
    assert rejected.rejection_stage == "resource-admission"


def test_artifacts_cannot_configure_limits(tmp_path):
    target = tmp_path / "scenario"
    shutil.copytree(SOURCE, target)
    bundle = target / "resolution-bundle-root.json"
    value = json.loads(bundle.read_text())
    value["resource_limits"] = {"inventory": 999999}
    bundle.write_text(json.dumps(value), encoding="utf-8")
    result = verify(ROOT, target, bundle, target / "trust-anchor.json")
    assert not result.success
    assert result.classification == "semantic_rejection"
