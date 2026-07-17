from pathlib import Path

from .authority import verify_anchor_snapshot, verify_ordinary_membership, verify_publication_bootstrap
from .bundle import load_scenario
from .errors import VerificationFailure, VerificationResult
from .lifecycle import resolve


def verify(
    repository_root: Path,
    scenario_root: Path,
    bundle_root_path: Path,
    trust_anchor_path: Path,
) -> VerificationResult:
    result, _trace = _verify_with_trace(repository_root, scenario_root, bundle_root_path, trust_anchor_path)
    return result


def _verify_with_trace(
    repository_root: Path,
    scenario_root: Path,
    bundle_root_path: Path,
    trust_anchor_path: Path,
) -> tuple[VerificationResult, tuple[str, ...]]:
    trace: list[str] = []
    try:
        scenario = load_scenario(repository_root, scenario_root, bundle_root_path, trust_anchor_path)
        snapshot = verify_anchor_snapshot(scenario)
        verify_publication_bootstrap(scenario, snapshot)
        entries = verify_ordinary_membership(scenario, snapshot)
        outcome = resolve(scenario, entries, trace.append)
        return VerificationResult(
            success=True,
            classification="success",
            rule_id=None,
            primary_component=None,
            rejection_stage=None,
            message="Fictional authority scenario verified.",
            outcome=outcome,
        ), tuple(trace)
    except VerificationFailure as failure:
        return failure.result, tuple(trace)
