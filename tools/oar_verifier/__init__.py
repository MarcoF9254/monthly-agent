"""Fictional-only owner-authority resolution prototype."""

from .errors import VerificationResult
from .verifier import verify

__all__ = ["VerificationResult", "verify"]
