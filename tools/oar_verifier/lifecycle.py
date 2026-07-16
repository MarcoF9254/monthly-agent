from typing import Any

from .bundle import Scenario
from .canonical import sha256
from .errors import reject

LIFECYCLE_STAGES = (
    "authorized-revocation-resolution",
    "remove-revoked-authorities",
    "authority-supersession-resolution",
    "business-subject-supersession-resolution",
)


def validate_lifecycle_stage_order(stages: tuple[str, ...]) -> None:
    required = LIFECYCLE_STAGES[:3]
    if tuple(stages[:3]) != required:
        reject("OAR-RV-005", "Revocation resolver", "lifecycle-order-admission", "Revocation must precede authority supersession.")


def _resolve_authority_tips(scenario: Scenario, entries: list[dict[str, Any]], revoked: set[str]) -> dict[str, dict[str, Any]]:
    active = {}
    for entry in entries:
        if entry["authority_status"] != "accepted" or entry["authority_id"] in revoked:
            continue
        envelope = scenario.by_authority_id(entry["authority_id"])
        if envelope:
            active[envelope["authority_id"]] = envelope
    authority_ids = set(active)
    for envelope in active.values():
        predecessor = envelope["supersedes_authority_id"]
        if predecessor is not None:
            if predecessor not in authority_ids:
                reject("OAR-AL-002", "Authority lifecycle resolver", "authority-lifecycle", "Broken authority supersession.")
            previous = active[predecessor]
            if sha256(previous) != envelope["supersedes_authority_artifact_sha256"]:
                reject("OAR-AL-002", "Authority lifecycle resolver", "authority-lifecycle", "Authority predecessor digest differs.")
            if previous["authority_purpose"] != envelope["authority_purpose"] or previous["scope"] != envelope["scope"]:
                reject("OAR-AL-002", "Authority lifecycle resolver", "authority-lifecycle", "Cross-purpose or cross-scope supersession.")
    superseded = {e["supersedes_authority_id"] for e in active.values() if e["supersedes_authority_id"]}
    tips = {}
    for envelope in active.values():
        if envelope["authority_id"] not in superseded:
            tips.setdefault(envelope["subject_id"], []).append(envelope)
    if any(len(values) != 1 for values in tips.values()):
        reject("OAR-AL-001", "Authority lifecycle resolver", "authority-lifecycle", "Multiple active authority tips.")
    return {subject_id: values[0] for subject_id, values in tips.items()}


def _revocations(scenario: Scenario, entries: list[dict[str, Any]]) -> set[str]:
    revoked = set()
    for subject in scenario.by_contract("authority-revocation-subject/0.1.0-draft"):
        entry = next((e for e in entries if e["subject_id"] == subject["subject_id"]), None)
        if entry is None or entry["authority_status"] != "accepted":
            reject("OAR-RV-001", "Revocation resolver", "revocation-authorization", "Revocation is not authorized.")
        target = scenario.by_authority_id(subject["target_authority_id"])
        if target is None:
            reject("OAR-RV-002", "Revocation resolver", "revocation-target-resolution", "Revocation target is missing.")
        if sha256(target) != subject["target_authority_artifact_sha256"]:
            reject("OAR-RV-003", "Revocation resolver", "revocation-target-resolution", "Revocation target digest differs.")
        if (
            target["authority_purpose"] != subject["target_authority_purpose"]
            or target["subject_type"] != subject["target_subject_type"]
            or target["subject_id"] != subject["target_subject_id"]
            or target["subject_sha256"] != subject["target_subject_sha256"]
            or target["scope"] != subject["target_scope"]
        ):
            reject("OAR-RV-004", "Revocation resolver", "revocation-target-resolution", "Revocation target purpose, subject, or scope differs.")
        revoked.add(target["authority_id"])
    return revoked


def _business_subjects(scenario: Scenario, tips: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    authority_ids = {
        v["authority_id"] for v in scenario.artifacts.values()
        if isinstance(v, dict) and v.get("authority_id") is not None
    }
    subjects = [scenario.by_subject_id(subject_id) for subject_id in tips]
    subjects = [subject for subject in subjects if subject is not None]
    by_id = {subject["subject_id"]: subject for subject in subjects}
    for subject in subjects:
        predecessor = subject.get("supersedes_subject_id")
        if predecessor in authority_ids:
            reject("OAR-AL-003", "Authority lifecycle resolver", "business-subject-lifecycle", "Business supersession names an authority identity.")
        if predecessor is not None:
            previous = by_id.get(predecessor)
            if previous is None or sha256(previous) != subject["supersedes_subject_sha256"]:
                reject("OAR-AL-003", "Authority lifecycle resolver", "business-subject-lifecycle", "Broken business-subject supersession.")
    superseded = {s.get("supersedes_subject_id") for s in subjects if s.get("supersedes_subject_id")}
    return [subject for subject in subjects if subject["subject_id"] not in superseded]


def resolve(scenario: Scenario, entries: list[dict[str, Any]], observe) -> dict[str, Any]:
    validate_lifecycle_stage_order(LIFECYCLE_STAGES)
    observe(LIFECYCLE_STAGES[0])
    revoked = _revocations(scenario, entries)
    observe(LIFECYCLE_STAGES[1])
    observe(LIFECYCLE_STAGES[2])
    tips = _resolve_authority_tips(scenario, entries, revoked)
    observe(LIFECYCLE_STAGES[3])
    subjects = _business_subjects(scenario, tips)
    run = next((s for s in subjects if s["contract_version"] == "run-metadata-binding-subject/0.2.0-draft"), None)
    if run is None:
        reject("PROTO-OUTCOME-001", "Run-metadata validator", "outcome-resolution", "No effective run metadata.")
    eligibility = {
        s["activity_id"]: s["decision"]
        for s in subjects if s["contract_version"] == "calendar-eligibility-subject/0.3.0-draft"
    }
    selection = next(
        (s for s in subjects if s["contract_version"] == "calendar-monthly-selection-subject/0.3.0-draft"),
        None,
    )
    selected = [] if selection is None else selection["selected_activity_ids"]
    if any(eligibility.get(activity_id) != "eligible" for activity_id in selected):
        reject("PROTO-OUTCOME-002", "Authority lifecycle resolver", "outcome-resolution", "Selection contains an ineligible activity.")
    return {
        "run_id": run["run_id"],
        "programme_month": run["programme_month"],
        "consumer_id": run["consumer_id"],
        "eligibility": dict(sorted(eligibility.items())),
        "selected_activity_ids": selected,
        "eligible_unselected_activity_ids": sorted(
            activity_id for activity_id, decision in eligibility.items()
            if decision == "eligible" and activity_id not in selected
        ),
        "monthly_selection_effective": selection is not None,
    }
