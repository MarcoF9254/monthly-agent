import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import governance_pr_gate_ci as ci


BASE = "1" * 40
HEAD = "2" * 40
MERGE = "3" * 40


def event(*, head=HEAD, base=BASE, head_repo="MarcoF9254/monthly-agent"):
    return {
        "repository": {"full_name": "MarcoF9254/monthly-agent"},
        "pull_request": {
            "number": 27,
            "base": {"sha": base, "repo": {"full_name": "MarcoF9254/monthly-agent"}},
            "head": {"sha": head, "repo": {"full_name": head_repo}},
        },
    }


ENV = {
    "GITHUB_REPOSITORY": "MarcoF9254/monthly-agent",
    "GITHUB_SHA": MERGE,
    "GITHUB_RUN_ID": "9001",
    "GITHUB_RUN_ATTEMPT": "2",
}


def fake_subprocess(monkeypatch, *, validator_exit=0, validator_status="PASS", observed=HEAD):
    calls = []

    def invoke(args, **kwargs):
        calls.append((args, kwargs))
        if args[:3] == ["git", "rev-parse", "HEAD"]:
            return SimpleNamespace(returncode=0, stdout=observed + "\n")
        return SimpleNamespace(
            returncode=validator_exit,
            stdout=json.dumps({"version": 1, "overall_status": validator_status}),
            stderr="",
        )

    monkeypatch.setattr(ci.subprocess, "run", invoke)
    return calls


def run_adapter(monkeypatch, tmp_path, **kwargs):
    calls = fake_subprocess(monkeypatch, **kwargs)
    code, evidence = ci.run(event(), ENV, tmp_path, Path("C:/trusted/tools/governance_pr_gate.py"))
    return code, evidence, calls


def test_exact_pr_head_and_base_binding_ignore_github_sha(monkeypatch, tmp_path):
    code, evidence, calls = run_adapter(monkeypatch, tmp_path)
    envelope = json.loads(calls[1][1]["input"])
    assert code == 0
    assert envelope["expected_head"] == HEAD
    assert envelope["expected_base"] == BASE
    assert envelope["expected_head"] != ENV["GITHUB_SHA"]
    assert evidence["expected_head"] == HEAD


def test_candidate_checkout_head_mismatch_remains_visible(monkeypatch, tmp_path):
    _, evidence, _ = run_adapter(monkeypatch, tmp_path, validator_exit=1, validator_status="FAIL", observed=MERGE)
    assert evidence["observed_candidate_head"] == MERGE
    assert evidence["expected_head"] == HEAD
    assert evidence["mechanical_result"] == "NO_MECHANICAL_PASS"


def test_stale_evidence_is_distinguishable(monkeypatch, tmp_path):
    calls = fake_subprocess(monkeypatch)
    _, a = ci.run(event(head="a" * 40), ENV, tmp_path, Path("trusted.py"))
    _, b = ci.run(event(head="b" * 40), ENV, tmp_path, Path("trusted.py"))
    assert a["expected_head"] != b["expected_head"]
    assert len(calls) == 4


def test_same_repository_is_eligible():
    assert ci.build_context(event(), ENV)["eligibility"] == "same_repository"


def test_fork_is_explicitly_unsupported_and_does_not_invoke_validator(monkeypatch, tmp_path):
    calls = fake_subprocess(monkeypatch)
    code, evidence = ci.run(event(head_repo="someone/fork"), ENV, tmp_path, Path("trusted.py"))
    assert code == 1
    assert evidence["eligibility"] == "fork_unsupported"
    assert evidence["mechanical_result"] == "NO_MECHANICAL_PASS"
    assert evidence["validator_result"]["errors"] == ["fork_pr_unsupported"]
    assert len(calls) == 1  # observed HEAD only; no Python validator execution


@pytest.mark.parametrize("bad", [{}, {"pull_request": {}}, event(head="short")])
def test_malformed_event_is_rejected(bad):
    with pytest.raises(ci.InputError):
        ci.build_context(bad, ENV)


@pytest.mark.parametrize(
    ("exit_code", "status", "mechanical"),
    [(0, "PASS", "PASS"), (1, "FAIL", "NO_MECHANICAL_PASS"), (2, "INVALID", "NO_MECHANICAL_PASS")],
)
def test_validator_exit_code_is_preserved(monkeypatch, tmp_path, exit_code, status, mechanical):
    code, evidence, _ = run_adapter(monkeypatch, tmp_path, validator_exit=exit_code, validator_status=status)
    assert code == exit_code
    assert evidence["validator_exit_code"] == exit_code
    assert evidence["validator_result"]["overall_status"] == status
    assert evidence["mechanical_result"] == mechanical


def test_evidence_wrapper_has_exact_head_run_identity(monkeypatch, tmp_path):
    _, evidence, _ = run_adapter(monkeypatch, tmp_path)
    assert (evidence["repository"], evidence["pr_number"]) == ("MarcoF9254/monthly-agent", 27)
    assert (evidence["workflow_run_id"], evidence["workflow_run_attempt"]) == ("9001", "2")
    assert evidence["observed_candidate_head"] == HEAD


def test_trusted_validator_runs_in_candidate_workspace(monkeypatch, tmp_path):
    _, _, calls = run_adapter(monkeypatch, tmp_path)
    args, kwargs = calls[1]
    assert Path(args[1]) == Path("C:/trusted/tools/governance_pr_gate.py")
    assert kwargs["cwd"] == tmp_path


def test_candidate_validator_cannot_self_attest(monkeypatch, tmp_path):
    _, _, calls = run_adapter(monkeypatch, tmp_path)
    command = calls[1][0]
    assert str(tmp_path) not in command[1]
    assert command[-1] == "-"


def test_fixed_allowlist_is_not_candidate_controlled(monkeypatch, tmp_path):
    _, _, calls = run_adapter(monkeypatch, tmp_path)
    assert json.loads(calls[1][1]["input"])["allowed_paths"] == ci.ALLOWED_PATHS


def test_missing_history_validator_failure_is_fail_closed(monkeypatch, tmp_path):
    code, evidence, _ = run_adapter(monkeypatch, tmp_path, validator_exit=1, validator_status="FAIL")
    assert code == 1
    assert evidence["mechanical_result"] == "NO_MECHANICAL_PASS"


def test_workflow_is_shadow_only_and_has_no_merge_authority():
    workflow = Path(".github/workflows/governance-pr-gate-shadow.yml").read_text(encoding="utf-8")
    assert "pull_request_target" not in workflow
    assert "github.sha" not in workflow
    assert "contents: read" in workflow
    assert "pull-requests: write" not in workflow
    assert "Ready" not in workflow
    assert "merge" not in workflow.lower()
    assert "exit 1" in workflow  # mechanical failure remains visible
