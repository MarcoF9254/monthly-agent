import copy
from pathlib import Path

import pytest

from tools.oar_verifier.bundle import Scenario
from tools.oar_verifier.errors import VerificationFailure
from tools.oar_verifier.lifecycle import (
    _business_subjects,
    _outcome_from_subjects,
    _resolve_authority_tips,
)


SCOPE = {
    "run_id": "fictional-run-2099-01-oar",
    "consumer_id": "calendar-renderer",
    "programme_month": "2099-01",
    "registry_purpose": "calendar-authority-resolution",
}


def _run(subject_id="run-1"):
    return {"contract_version": "run-metadata-binding-subject/0.2.0-draft", "subject_id": subject_id, "run_id": SCOPE["run_id"], "consumer_id": SCOPE["consumer_id"], "programme_month": SCOPE["programme_month"]}


def _selection(subject_id="selection-1"):
    return {"contract_version": "calendar-monthly-selection-subject/0.3.0-draft", "subject_id": subject_id, "run_id": SCOPE["run_id"], "consumer_id": SCOPE["consumer_id"], "programme_month": SCOPE["programme_month"], "selected_activity_ids": []}


def _eligibility(subject_id="eligibility-1", activity_id="activity-1"):
    return {"contract_version": "calendar-eligibility-subject/0.3.0-draft", "subject_id": subject_id, "run_id": SCOPE["run_id"], "consumer_id": SCOPE["consumer_id"], "activity_id": activity_id, "decision": "eligible"}


@pytest.mark.parametrize(
    ("duplicate", "rule_id"),
    [
        (_run("run-2"), "PROTO-AMBIGUOUS-RUN-METADATA"),
        (_selection("selection-2"), "PROTO-AMBIGUOUS-MONTHLY-SELECTION"),
        (_eligibility("eligibility-2"), "PROTO-AMBIGUOUS-CALENDAR-ELIGIBILITY"),
    ],
)
def test_multiple_effective_business_key_candidates_fail_closed(duplicate, rule_id):
    subjects = [_run(), _selection(), _eligibility(), duplicate]
    with pytest.raises(VerificationFailure) as captured:
        _outcome_from_subjects(subjects)
    assert captured.value.result.rule_id == rule_id


def test_candidate_order_does_not_change_ambiguity_result():
    subjects = [_run(), _run("run-2"), _selection(), _eligibility()]
    failures = []
    for candidates in (subjects, list(reversed(subjects))):
        with pytest.raises(VerificationFailure) as captured:
            _outcome_from_subjects(candidates)
        failures.append(captured.value.result)
    assert failures[0] == failures[1]


def test_identical_disconnected_active_candidates_are_not_deduplicated():
    first = _selection()
    second = copy.deepcopy(first)
    second["subject_id"] = "selection-2"
    with pytest.raises(VerificationFailure) as captured:
        _outcome_from_subjects([_run(), _eligibility(), first, second])
    assert captured.value.result.rule_id == "PROTO-AMBIGUOUS-MONTHLY-SELECTION"


def _scenario(artifacts):
    return Scenario(Path("."), Path("."), {}, Path("."), {}, artifacts, [])


def test_authority_supersession_cycle_fails_closed(monkeypatch):
    a = {"authority_id": "a", "subject_id": "subject", "authority_purpose": "run-metadata-binding", "scope": SCOPE, "supersedes_authority_id": "b", "supersedes_authority_artifact_sha256": "digest-b"}
    b = {"authority_id": "b", "subject_id": "subject", "authority_purpose": "run-metadata-binding", "scope": SCOPE, "supersedes_authority_id": "a", "supersedes_authority_artifact_sha256": "digest-a"}
    scenario = _scenario({"a": a, "b": b})
    entries = [{"authority_id": "a", "authority_status": "accepted"}, {"authority_id": "b", "authority_status": "accepted"}]
    monkeypatch.setattr("tools.oar_verifier.lifecycle.sha256", lambda value: "digest-" + value["authority_id"])
    with pytest.raises(VerificationFailure) as captured:
        _resolve_authority_tips(scenario, entries, set())
    assert captured.value.result.rule_id == "OAR-AL-002"


def test_business_subject_supersession_cycle_fails_closed(monkeypatch):
    a = {"subject_id": "a", "supersedes_subject_id": "b", "supersedes_subject_sha256": "digest-b"}
    b = {"subject_id": "b", "supersedes_subject_id": "a", "supersedes_subject_sha256": "digest-a"}
    scenario = _scenario({"a": a, "b": b})
    monkeypatch.setattr("tools.oar_verifier.lifecycle.sha256", lambda value: "digest-" + value["subject_id"])
    with pytest.raises(VerificationFailure) as captured:
        _business_subjects(scenario, {"a": {}, "b": {}})
    assert captured.value.result.rule_id == "OAR-AL-003"
