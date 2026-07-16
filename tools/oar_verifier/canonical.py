import hashlib
import json
from pathlib import Path
from typing import Any

import rfc8785

from .errors import reject


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            reject("PROTO-JSON-001", "Bundle verifier", "json-admission", "Duplicate JSON object key.")
        result[key] = value
    return result


def _constant(value: str):
    reject("PROTO-JSON-002", "Bundle verifier", "json-admission", f"Non-I-JSON number: {value}.")


def load_json_bytes(data: bytes) -> Any:
    try:
        text = data.decode("utf-8-sig")
        return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except UnicodeError:
        reject("PROTO-JSON-003", "Bundle verifier", "json-admission", "JSON is not valid UTF-8.")
    except json.JSONDecodeError:
        reject("PROTO-JSON-004", "Bundle verifier", "json-admission", "Malformed JSON.")


def load_json(path: Path) -> Any:
    try:
        return load_json_bytes(path.read_bytes())
    except OSError:
        reject("PROTO-FS-001", "Bundle verifier", "filesystem-admission", "JSON input is unreadable.")


def canonical_bytes(value: Any) -> bytes:
    try:
        return rfc8785.dumps(value)
    except (rfc8785.CanonicalizationError, TypeError, ValueError, UnicodeError):
        reject("PROTO-JCS-001", "Bundle verifier", "canonicalization", "RFC 8785 canonicalization failed.")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def identity_sha256(value: dict[str, Any], identity_field: str) -> str:
    material = dict(value)
    material.pop(identity_field, None)
    return sha256(material)
