import inspect
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.oar_verifier.lifecycle import LIFECYCLE_STAGES
from tools.oar_verifier.verifier import _verify_with_trace, verify


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "contract-fixtures" / "owner-authority-resolution" / "positive"
CLI = ROOT / "tools" / "verify_fictional_authority.py"


def run_scenario(name: str):
    scenario = FIXTURES / name
    return verify(ROOT, scenario, scenario / "resolution-bundle-root.json", scenario / "trust-anchor.json")


def test_pre_revocation_outcome():
    result = run_scenario("pre-revocation")
    assert result.success
    assert result.outcome == {
        "run_id": "fictional-run-2099-01-oar",
        "programme_month": "2099-01",
        "consumer_id": "calendar-renderer",
        "eligibility": {
            "example-activity-2099-01-001": "eligible",
            "example-activity-2099-01-002": "eligible",
        },
        "selected_activity_ids": ["example-activity-2099-01-001"],
        "eligible_unselected_activity_ids": ["example-activity-2099-01-002"],
        "monthly_selection_effective": True,
    }


def test_post_revocation_outcome_and_actual_trace():
    scenario = FIXTURES / "post-revocation"
    result, trace = _verify_with_trace(
        ROOT, scenario, scenario / "resolution-bundle-root.json", scenario / "trust-anchor.json"
    )
    assert result.success
    assert result.outcome["selected_activity_ids"] == []
    assert result.outcome["monthly_selection_effective"] is False
    assert trace == LIFECYCLE_STAGES
    assert trace.index("authorized-revocation-resolution") < trace.index("authority-supersession-resolution")


def test_repeated_execution_is_deterministic():
    first = run_scenario("post-revocation")
    second = run_scenario("post-revocation")
    assert second == first
    assert first.classification == second.classification == "success"


def test_public_api_has_no_lifecycle_configuration():
    parameters = inspect.signature(verify).parameters
    assert set(parameters) == {"repository_root", "scenario_root", "bundle_root_path", "trust_anchor_path"}
    assert all("lifecycle" not in name and "resolution_context" not in name for name in parameters)


def test_verification_has_no_network_and_writes_no_fixture(monkeypatch):
    scenario = FIXTURES / "pre-revocation"
    before = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in scenario.glob("*.json")
    }
    def prohibited(*args, **kwargs):
        raise AssertionError("network access attempted")
    monkeypatch.setattr("socket.create_connection", prohibited)
    assert run_scenario("pre-revocation").success
    after = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in scenario.glob("*.json")
    }
    assert after == before


def test_cli_executes_with_separately_supplied_anchor():
    scenario = FIXTURES / "pre-revocation"
    result = subprocess.run(
        [sys.executable, str(CLI), "--scenario-root", str(scenario), "--bundle-root",
         str(scenario / "resolution-bundle-root.json"), "--trust-anchor",
         str(scenario / "trust-anchor.json")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["success"] is True
    assert payload["classification"] == "success"
    assert payload["outcome"]["selected_activity_ids"] == ["example-activity-2099-01-001"]
