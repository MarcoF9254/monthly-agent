from typing import Any

from .bundle import FICTIONAL_SCOPE, Scenario
from .canonical import sha256
from .errors import reject
from .limits import enforce_lifecycle_depth


ORDINARY_SUBJECT_VERSIONS = {
    "calendar-eligibility-subject/0.3.0-draft",
    "calendar-monthly-selection-subject/0.3.0-draft",
    "run-metadata-binding-subject/0.2.0-draft",
    "authority-revocation-subject/0.1.0-draft",
}


def _scope_for(subject: dict[str, Any]) -> dict[str, Any]:
    version = subject["contract_version"]
    if version == "calendar-eligibility-subject/0.3.0-draft":
        return {
            "run_id": subject["run_id"],
            "consumer_id": subject["consumer_id"],
            "activity_id": subject["activity_id"],
        }
    if version == "authority-revocation-subject/0.1.0-draft":
        return FICTIONAL_SCOPE
    return {
        "run_id": subject["run_id"],
        "consumer_id": subject["consumer_id"],
        "programme_month": subject["programme_month"],
        "registry_purpose": "calendar-authority-resolution",
    }


def verify_anchor_snapshot(scenario: Scenario) -> dict[str, Any]:
    bundle = scenario.bundle
    anchor = scenario.anchor
    snapshots = scenario.by_contract("authority-registry-snapshot/0.2.0-draft")
    current = next((s for s in snapshots if s["snapshot_id"] == bundle["snapshot_id"]), None)
    if current is None:
        reject("BAI-BV-001", "Bundle verifier", "snapshot-resolution", "Effective snapshot is absent.")
    digest = sha256(current)
    if anchor["authorized_tip_id"] != current["snapshot_id"] or bundle["snapshot_id"] != current["snapshot_id"]:
        reject("BAI-TA-003", "Bundle verifier", "trust-anchor-binding", "Anchor, bundle, and snapshot tip disagree.")
    if anchor["expected_snapshot_artifact_sha256"] != digest or bundle["snapshot_artifact_sha256"] != digest:
        reject("OAR-BS-006", "Bundle verifier", "trust-anchor-binding", "Anchor does not pin the complete snapshot.")
    if anchor["registry_id"] != current["registry_id"] or bundle["registry_id"] != current["registry_id"]:
        reject("BAI-TA-003", "Bundle verifier", "trust-anchor-binding", "Registry identity disagreement.")
    if current["scope"] != FICTIONAL_SCOPE or bundle["scope"] != current["scope"] or anchor["scope"] != current["scope"]:
        reject("PROTO-SCOPE-002", "Bundle verifier", "trust-anchor-binding", "Exact scope disagreement.")

    by_id = {snapshot["snapshot_id"]: snapshot for snapshot in snapshots}
    seen = set()
    node = current
    depth = 0
    while node["supersedes_snapshot_id"] is not None:
        if node["snapshot_id"] in seen:
            reject("BAI-LC-005", "Lifecycle resolver", "snapshot-lineage", "Cyclic snapshot lineage.")
        seen.add(node["snapshot_id"])
        depth += 1
        enforce_lifecycle_depth(depth)
        predecessor = by_id.get(node["supersedes_snapshot_id"])
        if predecessor is None or sha256(predecessor) != node["supersedes_snapshot_artifact_sha256"]:
            reject("BAI-LC-005", "Lifecycle resolver", "snapshot-lineage", "Broken snapshot predecessor.")
        if predecessor["registry_id"] != current["registry_id"] or predecessor["scope"] != current["scope"]:
            reject("BAI-LC-004", "Lifecycle resolver", "snapshot-lineage", "Cross-scope snapshot supersession.")
        node = predecessor
    superseded = {s["supersedes_snapshot_id"] for s in snapshots if s["supersedes_snapshot_id"]}
    tips = [s for s in snapshots if s["snapshot_id"] not in superseded]
    if len(tips) != 1 or tips[0]["snapshot_id"] != current["snapshot_id"]:
        reject("BAI-LC-003", "Lifecycle resolver", "snapshot-lineage", "Snapshot tip is ambiguous.")
    return current


def verify_publication_bootstrap(scenario: Scenario, snapshot: dict[str, Any]) -> None:
    subject = scenario.by_subject_id(snapshot["publication_subject_id"])
    envelope = scenario.by_authority_id(snapshot["publication_authority_id"])
    if subject is None or envelope is None:
        reject("OAR-BS-003", "Bundle verifier", "publication-bootstrap", "Publication bootstrap evidence missing.")
    for entry in snapshot["entries"]:
        if entry["authority_id"] == envelope["authority_id"] or entry["authority_artifact_sha256"] == sha256(envelope):
            reject("OAR-BS-001", "Registry publication bootstrap verifier", "publication-bootstrap", "Publication envelope appears in ordinary membership.")
    if envelope["authority_purpose"] != "calendar-registry-publication" or envelope["subject_type"] != "calendar-registry-publication":
        reject("OAR-BS-002", "Registry publication bootstrap verifier", "publication-bootstrap", "Bootstrap purpose is not publication.")
    if (
        sha256(subject) != snapshot["publication_subject_sha256"]
        or envelope["subject_sha256"] != sha256(subject)
        or sha256(envelope) != snapshot["publication_authority_artifact_sha256"]
    ):
        reject("OAR-BS-004", "Registry publication bootstrap verifier", "publication-bootstrap", "Publication digest binding mismatch.")
    core = {
        key: snapshot[key]
        for key in (
            "contract_version", "registry_id", "snapshot_id", "snapshot_version",
            "supersedes_snapshot_id", "supersedes_snapshot_artifact_sha256", "scope", "entries"
        )
    }
    expected = {
        "contract_version": "registry-publication-subject/0.1.0-draft",
        "subject_id": subject["subject_id"],
        "snapshot_contract_version": core.pop("contract_version"),
        **core,
    }
    if subject != expected:
        reject("OAR-BS-004", "Registry publication bootstrap verifier", "publication-bootstrap", "Publication subject does not equal snapshot core.")


def verify_ordinary_membership(scenario: Scenario, snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    entries = snapshot["entries"]
    by_subject = {entry["subject_id"]: entry for entry in entries}
    ordinary_subjects = [
        value for value in scenario.artifacts.values()
        if value.get("contract_version") in ORDINARY_SUBJECT_VERSIONS
    ]
    for subject in ordinary_subjects:
        entry = by_subject.get(subject["subject_id"])
        if entry is None:
            if subject["contract_version"] == "authority-revocation-subject/0.1.0-draft":
                continue
            reject("OAR-SB-003", "Artifact authority verifier", "ordinary-membership", "Subject lacks exact ordinary authority membership.")
        envelope = scenario.by_authority_id(entry["authority_id"])
        if envelope is None:
            reject("OAR-SB-003", "Artifact authority verifier", "ordinary-membership", "Authority envelope is absent.")
        if sha256(envelope) != entry["authority_artifact_sha256"]:
            reject("OAR-SB-001", "Authority subject-binding verifier", "authority-subject-binding", "Envelope artifact digest differs.")
        if (
            envelope["subject_sha256"] != entry["subject_sha256"]
            or envelope["subject_id"] != entry["subject_id"]
            or envelope["subject_type"] != entry["subject_type"]
            or envelope["authority_purpose"] != entry["authority_purpose"]
        ):
            reject("OAR-SB-001", "Authority subject-binding verifier", "authority-subject-binding", "Envelope differs from anchored membership.")
        digest = sha256(subject)
        if envelope["subject_sha256"] != digest or entry["subject_sha256"] != digest:
            reject("OAR-SB-002", "Authority subject-binding verifier", "authority-subject-binding", "Subject content differs from authorized digest.")
        expected_type = {
            "calendar-eligibility-subject/0.3.0-draft": "calendar-eligibility",
            "calendar-monthly-selection-subject/0.3.0-draft": "calendar-monthly-selection",
            "run-metadata-binding-subject/0.2.0-draft": "run-metadata-binding",
            "authority-revocation-subject/0.1.0-draft": "calendar-authority-revocation",
        }[subject["contract_version"]]
        if (
            envelope["subject_id"] != subject["subject_id"]
            or envelope["subject_type"] != expected_type
            or envelope["authority_purpose"] != expected_type
            or entry["subject_type"] != expected_type
            or entry["authority_purpose"] != expected_type
            or envelope["scope"] != _scope_for(subject)
        ):
            reject("OAR-SB-001", "Authority subject-binding verifier", "authority-subject-binding", "Purpose, type, identity, or scope differs.")
    return entries
