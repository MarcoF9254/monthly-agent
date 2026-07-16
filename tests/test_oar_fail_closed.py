import inspect
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.oar_verifier.verifier import verify


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/contract-fixtures/owner-authority-resolution/positive/pre-revocation"
CLI = ROOT / "tools/verify_fictional_authority.py"


def _copy(tmp_path):
    import shutil
    target = tmp_path / "scenario"
    shutil.copytree(SOURCE, target)
    return target


def test_cli_requires_separate_anchor_and_rejects_lifecycle_option():
    missing_anchor = subprocess.run(
        [sys.executable, str(CLI), "--scenario-root", str(SOURCE), "--bundle-root",
         str(SOURCE / "resolution-bundle-root.json")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert missing_anchor.returncode == 2
    assert "--trust-anchor" in missing_anchor.stderr
    lifecycle_argument = subprocess.run(
        [sys.executable, str(CLI), "--scenario-root", str(SOURCE), "--bundle-root",
         str(SOURCE / "resolution-bundle-root.json"), "--trust-anchor",
         str(SOURCE / "trust-anchor.json"), "--lifecycle-order", "anything"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert lifecycle_argument.returncode == 2
    assert "lifecycle-order" in lifecycle_argument.stderr


def test_non_fictional_scope_rejected(tmp_path):
    target = _copy(tmp_path)
    anchor = json.loads((target / "trust-anchor.json").read_text())
    anchor["scope"]["programme_month"] = "2098-01"
    (target / "trust-anchor.json").write_text(json.dumps(anchor), encoding="utf-8")
    result = verify(ROOT, target, target / "resolution-bundle-root.json", target / "trust-anchor.json")
    assert result.rule_id == "PROTO-SCOPE-001"


def test_path_traversal_rejected(tmp_path):
    target = _copy(tmp_path)
    root = json.loads((target / "resolution-bundle-root.json").read_text())
    root["artifact_inventory"][0]["artifact_path"] = "../escape.json"
    (target / "resolution-bundle-root.json").write_text(json.dumps(root), encoding="utf-8")
    result = verify(ROOT, target, target / "resolution-bundle-root.json", target / "trust-anchor.json")
    assert result.rule_id == "PROTO-FS-003"


def test_undeclared_physical_json_rejected(tmp_path):
    target = _copy(tmp_path)
    (target / "extra.json").write_text("{}", encoding="utf-8")
    result = verify(ROOT, target, target / "resolution-bundle-root.json", target / "trust-anchor.json")
    assert result.rule_id == "BAI-BV-002"


def test_declared_missing_artifact_rejected(tmp_path):
    target = _copy(tmp_path)
    (target / "eligibility-subject-001.json").unlink()
    result = verify(ROOT, target, target / "resolution-bundle-root.json", target / "trust-anchor.json")
    assert result.rule_id == "BAI-BV-001"


def test_symlink_artifact_rejected(tmp_path, monkeypatch):
    target = _copy(tmp_path)
    original = Path.is_symlink
    monkeypatch.setattr(
        Path,
        "is_symlink",
        lambda path: path.name == "eligibility-subject-001.json" or original(path),
    )
    result = verify(ROOT, target, target / "resolution-bundle-root.json", target / "trust-anchor.json")
    assert result.rule_id == "PROTO-FS-004"


def test_verifier_does_not_import_mutation_support():
    source = inspect.getsource(sys.modules["tools.oar_verifier.verifier"])
    assert "mutations" not in source
    assert "$resolution-context" not in source


def test_cli_rejects_symbolic_resolution_context():
    result = subprocess.run(
        [sys.executable, str(CLI), "--scenario-root", str(SOURCE), "--bundle-root",
         str(SOURCE / "resolution-bundle-root.json"), "--trust-anchor",
         str(SOURCE / "trust-anchor.json"), "$resolution-context"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "$resolution-context" in result.stderr
