from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.oar_verifier.lifecycle import LIFECYCLE_STAGES
from tools.oar_verifier.verifier import _verify_with_trace


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "contract-fixtures" / "owner-authority-resolution" / "positive"


def _success(name: str):
    scenario = FIXTURES / name
    return _verify_with_trace(
        ROOT, scenario, scenario / "resolution-bundle-root.json", scenario / "trust-anchor.json"
    )


def _failure():
    scenario = FIXTURES / "pre-revocation"
    return _verify_with_trace(
        ROOT, scenario, scenario / "resolution-bundle-root.json", scenario / "missing-anchor.json"
    )


def test_concurrent_success_success_trace_isolation():
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda index: _success("pre-revocation" if index % 2 else "post-revocation"), range(32)))
    assert all(result.success and trace == LIFECYCLE_STAGES for result, trace in results)


def test_concurrent_success_failure_isolation():
    calls = [_failure if index % 2 else lambda: _success("post-revocation") for index in range(32)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = [future.result() for future in [executor.submit(call) for call in calls]]
    for index, (result, trace) in enumerate(results):
        if index % 2:
            assert not result.success
            assert result.rule_id == "BAI-TA-001"
            assert trace == ()
        else:
            assert result.success
            assert trace == LIFECYCLE_STAGES


def test_failure_does_not_contaminate_later_success():
    failed, failed_trace = _failure()
    succeeded, success_trace = _success("pre-revocation")
    assert not failed.success and failed_trace == ()
    assert succeeded.success and success_trace == LIFECYCLE_STAGES


def test_repeated_public_results_are_identical():
    results = [_success("post-revocation")[0] for _ in range(10)]
    assert all(result == results[0] for result in results)
