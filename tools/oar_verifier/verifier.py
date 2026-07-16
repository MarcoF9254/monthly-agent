from pathlib import Path

from .authority import verify_anchor_snapshot, verify_ordinary_membership, verify_publication_bootstrap
from .bundle import load_scenario
from .errors import VerificationFailure, VerificationResult
from .lifecycle import resolve

_LAST_TRACE: tuple[str, ...] = ()


def _trace_for_tests() -> tuple[str, ...]:
    return _LAST_TRACE


def verify(
    repository_root: Path,
    scenario_root: Path,
    bundle_root_path: Path,
    trust_anchor_path: Path,
) -> VerificationResult:
    global _LAST_TRACE
    trace: list[str] = []
    _LAST_TRACE = ()
    try:
        scenario = load_scenario(repository_root, scenario_root, bundle_root_path, trust_anchor_path)
        snapshot = verify_anchor_snapshot(scenario)
        verify_publication_bootstrap(scenario, snapshot)
        entries = verify_ordinary_membership(scenario, snapshot)
        outcome = resolve(scenario, entries, trace.append)
        _LAST_TRACE = tuple(trace)
        return VerificationResult(True, None, None, None, "Fictional authority scenario verified.", outcome)
    except VerificationFailure as failure:
        _LAST_TRACE = tuple(trace)
        return failure.result
