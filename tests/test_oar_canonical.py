import hashlib
import json
from pathlib import Path

import pytest

from tools.oar_verifier.canonical import canonical_bytes, load_json_bytes, sha256
from tools.oar_verifier.errors import VerificationFailure


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "contract-fixtures" / "owner-authority-resolution" / "positive"


def test_rfc_8785_number_vector():
    value = [333333333.33333329, 1e30, 4.50, 2e-3, 0.000000000000000000000000001]
    assert canonical_bytes(value) == b"[333333333.3333333,1e+30,4.5,0.002,1e-27]"


def test_rfc_8785_property_order_and_escaping_vector():
    value = {"b": 1, "a": 2}
    assert canonical_bytes(value) == bytes.fromhex("7b2261223a322c2262223a317d")


@pytest.mark.parametrize("payload", [
    bytes.fromhex("7b2261223a312c2261223a327d"),
    bytes.fromhex("7b2278223a4e614e7d"),
    bytes.fromhex("7b2278223a496e66696e6974797d"),
    bytes.fromhex("7b2278223a2d496e66696e6974797d"),
])
def test_duplicate_keys_and_non_i_json_fail_closed(payload):
    with pytest.raises(VerificationFailure):
        load_json_bytes(payload)


def test_all_fixture_inventory_digests_match_rfc_8785():
    for scenario in FIXTURES.iterdir():
        root = json.loads((scenario / "resolution-bundle-root.json").read_text())
        for item in root["artifact_inventory"]:
            value = json.loads((scenario / item["artifact_path"]).read_text())
            assert sha256(value) == item["artifact_sha256"]
        snapshot = json.loads((scenario / "registry-snapshot.json").read_text())
        assert sha256(snapshot) == root["snapshot_artifact_sha256"]


def test_sha256_is_lowercase_hex():
    digest = sha256({"example": True})
    assert digest == hashlib.sha256(canonical_bytes({"example": True})).hexdigest()
    assert len(digest) == 64 and digest == digest.lower()


@pytest.mark.parametrize("value", [2 ** 60, chr(0xD800)])
def test_unsupported_i_json_values_fail_closed(value):
    with pytest.raises(VerificationFailure):
        canonical_bytes(value)
