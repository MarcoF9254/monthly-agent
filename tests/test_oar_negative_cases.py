import json
from pathlib import Path

import pytest

from tools.oar_verifier.mutations import materialize_case, validate_n15
from tools.oar_verifier.verifier import verify


ROOT = Path(__file__).resolve().parents[1]
POSITIVE = ROOT / "examples" / "contract-fixtures" / "owner-authority-resolution" / "positive"
CORPUS = json.loads(
    (ROOT / "examples/contract-fixtures/bounded-authority-input/negative/negative-cases.json").read_text()
)


@pytest.mark.parametrize("case", CORPUS["cases"], ids=lambda case: case["fixture_id"])
def test_exact_negative_first_failure(case, tmp_path):
    if case["fixture_id"] == "OAR-N15":
        result = validate_n15(case)
        classification = "construction-invariant"
    else:
        source = POSITIVE / case["source_scenario"]
        target = tmp_path / case["fixture_id"]
        bundle, anchor = materialize_case(case, source, target)
        result = verify(ROOT, target, bundle, anchor)
        classification = "ordinary-verifier first-failure"
    assert not result.success
    assert result.rule_id == case["expected_rule_id"]
    assert result.primary_component == case["expected_primary_component"]
    assert result.rejection_stage == case["expected_rejection_stage"]
    assert classification == (
        "construction-invariant" if case["fixture_id"] == "OAR-N15" else "ordinary-verifier first-failure"
    )


def test_only_n15_may_use_symbolic_context(tmp_path):
    n15 = next(case for case in CORPUS["cases"] if case["fixture_id"] == "OAR-N15")
    other = dict(n15)
    other["fixture_id"] = "OAR-N14"
    with pytest.raises(ValueError):
        validate_n15(other)
    with pytest.raises(ValueError):
        materialize_case(n15, POSITIVE / "post-revocation", tmp_path / "n15")
