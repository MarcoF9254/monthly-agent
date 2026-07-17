from dataclasses import dataclass, field
from typing import Any, Literal


VERIFICATION_RESULT_CONTRACT_VERSION = "verification-result/v1"
VerificationClassification = Literal["success", "semantic_rejection", "resource_rejection"]


@dataclass(frozen=True, kw_only=True)
class VerificationResult:
    contract_version: str = field(default=VERIFICATION_RESULT_CONTRACT_VERSION, init=False)
    success: bool
    classification: VerificationClassification
    rule_id: str | None
    primary_component: str | None
    rejection_stage: str | None
    message: str
    outcome: dict[str, Any] | None = None

    def to_payload(self) -> dict[str, Any]:
        """Return the authoritative verification-result/v1 JSON payload."""
        return {
            "contract_version": self.contract_version,
            "success": self.success,
            "classification": self.classification,
            "rule_id": self.rule_id,
            "primary_component": self.primary_component,
            "rejection_stage": self.rejection_stage,
            "message": self.message,
            "outcome": self.outcome,
        }


class VerificationFailure(Exception):
    def __init__(
        self,
        rule_id: str,
        component: str,
        stage: str,
        message: str,
        classification: VerificationClassification = "semantic_rejection",
    ):
        super().__init__(message)
        self.result = VerificationResult(
            success=False,
            classification=classification,
            rule_id=rule_id,
            primary_component=component,
            rejection_stage=stage,
            message=message,
        )


def reject(rule_id: str, component: str, stage: str, message: str) -> None:
    raise VerificationFailure(rule_id, component, stage, message)


def reject_resource(rule_id: str, component: str, stage: str, message: str) -> None:
    raise VerificationFailure(rule_id, component, stage, message, "resource_rejection")
