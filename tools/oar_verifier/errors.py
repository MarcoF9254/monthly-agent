from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VerificationResult:
    success: bool
    rule_id: str | None
    primary_component: str | None
    rejection_stage: str | None
    message: str
    outcome: dict[str, Any] | None = None


class VerificationFailure(Exception):
    def __init__(self, rule_id: str, component: str, stage: str, message: str):
        super().__init__(message)
        self.result = VerificationResult(False, rule_id, component, stage, message)


def reject(rule_id: str, component: str, stage: str, message: str) -> None:
    raise VerificationFailure(rule_id, component, stage, message)
