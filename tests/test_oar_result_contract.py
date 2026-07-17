import json
from pathlib import Path

import pytest

import tools.verify_fictional_authority as cli
from tools.oar_verifier import VerificationResult, verify


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "examples" / "contract-fixtures" / "owner-authority-resolution" / "positive" / "pre-revocation"
EXPECTED_KEYS = {
    "contract_version",
    "success",
    "classification",
    "rule_id",
    "primary_component",
    "rejection_stage",
    "message",
    "outcome",
}


def make_result(classification="success", outcome=None):
    return VerificationResult(
        success=classification == "success",
        classification=classification,
        rule_id=None if classification == "success" else "TEST-RULE",
        primary_component=None if classification == "success" else "Test component",
        rejection_stage=None if classification == "success" else "test-stage",
        message="test result",
        outcome=outcome,
    )


def cli_args():
    return [
        "--scenario-root",
        str(SCENARIO),
        "--bundle-root",
        str(SCENARIO / "resolution-bundle-root.json"),
        "--trust-anchor",
        str(SCENARIO / "trust-anchor.json"),
    ]


def test_verification_result_rejects_positional_construction():
    with pytest.raises(TypeError):
        VerificationResult(True, "success", None, None, None, "message", None)


def test_keyword_only_success_payload_has_exact_version_and_keys():
    outcome = {"selected_activity_ids": ["example-activity-2099-01-001"]}
    payload = make_result(outcome=outcome).to_payload()

    assert set(payload) == EXPECTED_KEYS
    assert payload["contract_version"] == "verification-result/v1"
    assert payload["success"] is True
    assert payload["classification"] == "success"
    assert payload["outcome"] == outcome


@pytest.mark.parametrize("classification", ["semantic_rejection", "resource_rejection"])
def test_rejection_payload_has_null_outcome(classification):
    payload = make_result(classification=classification).to_payload()

    assert set(payload) == EXPECTED_KEYS
    assert payload["success"] is False
    assert payload["classification"] == classification
    assert payload["outcome"] is None


def test_cli_json_matches_authoritative_payload(capsys):
    expected = verify(
        ROOT,
        SCENARIO,
        SCENARIO / "resolution-bundle-root.json",
        SCENARIO / "trust-anchor.json",
    )

    assert cli.main(cli_args()) == 0
    assert json.loads(capsys.readouterr().out) == expected.to_payload()


@pytest.mark.parametrize("classification", ["semantic_rejection", "resource_rejection"])
def test_cli_verified_rejection_exit_code_is_one(monkeypatch, capsys, classification):
    result = make_result(classification=classification)
    monkeypatch.setattr(cli, "verify", lambda *args: result)

    assert cli.main(cli_args()) == 1
    assert json.loads(capsys.readouterr().out) == result.to_payload()


def test_cli_argparse_usage_error_exit_code_is_two():
    with pytest.raises(SystemExit) as failure:
        cli.main([])

    assert failure.value.code == 2
