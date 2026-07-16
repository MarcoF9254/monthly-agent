from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from .canonical import load_json
from .errors import reject


CONTRACT_SCHEMAS = {
    "authority-envelope/0.1.0-draft": "owner-authority-resolution/authority-envelope.schema.json",
    "authority-revocation-subject/0.1.0-draft": "owner-authority-resolution/authority-revocation-subject.schema.json",
    "calendar-eligibility-subject/0.3.0-draft": "owner-authority-resolution/calendar-eligibility-subject.schema.json",
    "calendar-monthly-selection-subject/0.3.0-draft": "owner-authority-resolution/calendar-monthly-selection-subject.schema.json",
    "registry-publication-subject/0.1.0-draft": "owner-authority-resolution/registry-publication-subject.schema.json",
    "run-metadata-binding-subject/0.2.0-draft": "owner-authority-resolution/run-metadata-binding-subject.schema.json",
    "authority-registry-snapshot/0.2.0-draft": "bounded-authority-input/authority-registry-snapshot.schema.json",
    "resolution-bundle-root/0.2.0-draft": "bounded-authority-input/resolution-bundle-root.schema.json",
    "bounded-authority-trust-anchor/0.1.0-draft": "bounded-authority-input/trust-anchor.schema.json",
}

TYPE_CONTRACTS = {
    "authority-envelope": {"authority-envelope/0.1.0-draft"},
    "registry-publication-envelope": {"authority-envelope/0.1.0-draft"},
    "authority-revocation-subject": {"authority-revocation-subject/0.1.0-draft"},
    "calendar-eligibility-subject": {"calendar-eligibility-subject/0.3.0-draft"},
    "calendar-monthly-selection-subject": {"calendar-monthly-selection-subject/0.3.0-draft"},
    "registry-publication-subject": {"registry-publication-subject/0.1.0-draft"},
    "registry-snapshot": {"authority-registry-snapshot/0.2.0-draft"},
    "run-metadata-binding-subject": {"run-metadata-binding-subject/0.2.0-draft"},
}


class SchemaSet:
    def __init__(self, repository_root: Path):
        root = repository_root / "schemas" / "drafts"
        self.schemas = {}
        registry = Registry(retrieve=self._deny_remote)
        for version, relative in CONTRACT_SCHEMAS.items():
            schema = load_json(root / relative)
            Draft202012Validator.check_schema(schema)
            self.schemas[version] = schema
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        self.registry = registry

    @staticmethod
    def _deny_remote(uri: str):
        raise RuntimeError(f"Remote schema retrieval prohibited: {uri}")

    def validate(self, artifact: Any, role: str, declared_type: str | None = None) -> None:
        if not isinstance(artifact, dict):
            reject("PROTO-SCHEMA-001", "Subject schema validator", "schema-validation", "Artifact must be an object.")
        version = artifact.get("contract_version")
        expected = TYPE_CONTRACTS.get(declared_type) if declared_type else None
        if version not in self.schemas or (expected is not None and version not in expected):
            reject("PROTO-DISPATCH-001", "Subject schema validator", "schema-dispatch", "Unknown or conflicting contract/type dispatch.")
        role_versions = {
            "trust-anchor": {"bounded-authority-trust-anchor/0.1.0-draft"},
            "bundle-root": {"resolution-bundle-root/0.2.0-draft"},
            "effective-snapshot": {"authority-registry-snapshot/0.2.0-draft"},
        }
        if role in role_versions and version not in role_versions[role]:
            reject("PROTO-DISPATCH-002", "Subject schema validator", "schema-dispatch", "Artifact conflicts with expected boundary role.")
        validator = Draft202012Validator(
            self.schemas[version], registry=self.registry, format_checker=FormatChecker()
        )
        errors = sorted(validator.iter_errors(artifact), key=lambda error: (list(error.path), error.message))
        if errors:
            first = errors[0]
            rule = "OAR-RV-006" if version == "authority-revocation-subject/0.1.0-draft" else "PROTO-SCHEMA-002"
            reject(rule, "Subject schema validator", "subject-schema", "Artifact failed its declared Draft 2020-12 schema.")
