#!/usr/bin/env python3
"""Offline, mechanical post-merge validation against a local Git repository."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import PurePosixPath
from typing import Any


SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
HTTPS_ORIGIN_RE = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$")
SSH_ORIGIN_RE = re.compile(r"^git@github\.com:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?$")


class GitFailure(Exception):
    """A local Git query failed or returned unusable data."""


def _git(arguments: list[str], *, text: bool = True) -> str | bytes:
    try:
        result = subprocess.run(
            ["git", *arguments], check=False, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=text,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitFailure from exc
    if result.returncode != 0:
        raise GitFailure
    return result.stdout


def _valid_path(path: Any) -> bool:
    if not isinstance(path, str) or not path or "\\" in path or "\x00" in path or path == ".":
        return False
    if path.startswith("/") or re.match(r"^[A-Za-z]:", path):
        return False
    parts = PurePosixPath(path).parts
    return ".." not in parts and "." not in parts and "//" not in path


def validate_input(value: Any) -> list[str]:
    required = {
        "version", "repository", "merge_commit", "expected_base",
        "expected_reviewed_head", "expected_landed_paths", "main_ref",
    }
    if not isinstance(value, dict):
        return ["input must be a JSON object"]
    errors: list[str] = []
    missing = sorted(required - value.keys())
    extra = sorted(value.keys() - required)
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if extra:
        errors.append("unknown fields: " + ", ".join(extra))
    if value.get("version") != 1 or isinstance(value.get("version"), bool):
        errors.append("version must be 1")
    if not isinstance(value.get("repository"), str) or not REPOSITORY_RE.fullmatch(value.get("repository", "")):
        errors.append("repository must be OWNER/REPO")
    for field in ("merge_commit", "expected_base", "expected_reviewed_head"):
        if not isinstance(value.get(field), str) or not SHA_RE.fullmatch(value.get(field, "")):
            errors.append(f"{field} must be a full 40-hex SHA")
    paths = value.get("expected_landed_paths")
    if not isinstance(paths, list):
        errors.append("expected_landed_paths must be an array")
    else:
        if any(not _valid_path(path) for path in paths):
            errors.append("expected_landed_paths must contain normalized repository-relative Git paths")
        if all(isinstance(path, str) for path in paths) and len(paths) != len(set(paths)):
            errors.append("expected_landed_paths must not contain duplicates")
    if not isinstance(value.get("main_ref"), str) or not value.get("main_ref") or "\x00" in value.get("main_ref", ""):
        errors.append("main_ref must be a non-empty string")
    return sorted(errors)


def _canonical_origin(origin: str) -> str | None:
    for pattern in (HTTPS_ORIGIN_RE, SSH_ORIGIN_RE):
        match = pattern.fullmatch(origin.strip())
        if match:
            return match.group(1)
    return None


def _commit(sha: str) -> str | None:
    try:
        object_type = _git(["cat-file", "-t", sha]).strip()
        observed = _git(["rev-parse", "--verify", sha]).strip()
    except GitFailure:
        return None
    if object_type != "commit" or not SHA_RE.fullmatch(str(observed)) or str(observed).lower() != sha.lower():
        return None
    return str(observed).lower()


def _resolve(arguments: list[str]) -> str | None:
    try:
        observed = str(_git(["rev-parse", *arguments])).strip()
    except GitFailure:
        return None
    return observed.lower() if SHA_RE.fullmatch(observed) else None


def _is_ancestor(base: str, head: str) -> bool:
    try:
        _git(["merge-base", "--is-ancestor", base, head])
        return True
    except GitFailure:
        return False


def _changed_paths(base: str, head: str) -> list[str]:
    raw = _git(["diff-tree", "-r", "--no-commit-id", "--name-status", "-z", base, head], text=False)
    if not isinstance(raw, bytes):
        raise GitFailure
    fields = raw.decode("utf-8", "surrogateescape").split("\0")
    if not fields or fields[-1] != "":
        raise GitFailure
    fields.pop()
    paths: list[str] = []
    index = 0
    while index < len(fields):
        status = fields[index]
        index += 1
        if status not in {"A", "M", "D", "T"} or index >= len(fields):
            raise GitFailure
        path = fields[index]
        index += 1
        if not path or "\x00" in path:
            raise GitFailure
        paths.append(path)
    return sorted(set(paths))


def evaluate(value: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}
    merge = _commit(value["merge_commit"])
    base = _commit(value["expected_base"])
    reviewed = _commit(value["expected_reviewed_head"])

    try:
        observed_repository = _canonical_origin(str(_git(["config", "--get", "remote.origin.url"])))
    except GitFailure:
        observed_repository = None
    checks["repository_identity"] = {"status": "PASS" if observed_repository == value["repository"] else "FAIL", "observed": observed_repository}
    checks["merge_commit_object"] = {"status": "PASS" if merge else "FAIL", "observed": merge}

    parents: list[str] | None = None
    if merge:
        try:
            raw_parents = str(_git(["rev-parse", f"{merge}^@"]))
            raw_parents = raw_parents.splitlines()
            if all(SHA_RE.fullmatch(parent) for parent in raw_parents):
                parents = [parent.lower() for parent in raw_parents]
        except GitFailure:
            pass
    parent_count = len(parents) if parents is not None else 0
    checks["merge_topology"] = {"status": "PASS" if parent_count == 2 else "FAIL", "parent_count": parent_count, "observed_parents": parents}

    ancestry = bool(base and reviewed and _is_ancestor(base, reviewed))
    checks["reviewed_head_ancestry"] = {"status": "PASS" if ancestry else "FAIL"}
    first = _resolve([f"{merge}^1"]) if merge else None
    second = _resolve([f"{merge}^2"]) if merge else None
    checks["first_parent_binding"] = {"status": "PASS" if first == value["expected_base"].lower() else "FAIL", "expected": value["expected_base"].lower(), "observed": first}
    checks["second_parent_binding"] = {"status": "PASS" if second == value["expected_reviewed_head"].lower() else "FAIL", "expected": value["expected_reviewed_head"].lower(), "observed": second}

    merge_tree = _resolve([f"{merge}^{{tree}}"] ) if merge else None
    reviewed_tree = _resolve([f"{reviewed}^{{tree}}"] ) if reviewed else None
    tree_pass = merge_tree is not None and reviewed_tree is not None and merge_tree == reviewed_tree
    checks["reviewed_tree_integrity"] = {"status": "PASS" if tree_pass else "FAIL", "merge_tree": merge_tree, "reviewed_tree": reviewed_tree}

    landed: list[str] = []
    landed_available = False
    if base and merge:
        try:
            landed = _changed_paths(base, merge)
            landed_available = True
        except (GitFailure, UnicodeError):
            pass
    expected_paths = sorted(value["expected_landed_paths"])
    extra = sorted(set(landed) - set(expected_paths)) if landed_available else []
    missing = sorted(set(expected_paths) - set(landed)) if landed_available else expected_paths
    checks["landed_scope"] = {"status": "PASS" if landed_available and not extra and not missing else "FAIL", "observed": landed, "expected": expected_paths, "extra": extra, "missing": missing}

    observed_main = _resolve([value["main_ref"]])
    main_check: dict[str, Any] = {"status": "FAIL", "observed_main": observed_main}
    if observed_main == merge and merge is not None:
        main_check["status"] = "PASS"
    elif observed_main and merge and _is_ancestor(merge, observed_main):
        main_check["reason"] = "main_advanced_beyond_target_merge"
    else:
        main_check["reason"] = "main_ref_mismatch"
    checks["main_binding"] = main_check

    return {
        "version": 1, "overall_status": "PASS" if all(check["status"] == "PASS" for check in checks.values()) else "FAIL",
        "repository": value["repository"], "merge_commit": value["merge_commit"].lower(),
        "expected_base": value["expected_base"].lower(), "expected_reviewed_head": value["expected_reviewed_head"].lower(),
        "observed_parents": parents, "main_ref": value["main_ref"], "observed_main": observed_main,
        "main_ref_freshness": "CALLER_RESPONSIBILITY", "observed_landed_paths": landed, "checks": checks,
    }


def _emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) > 1:
        _emit({"version": 1, "overall_status": "INVALID", "errors": ["usage: governance_post_merge_gate.py [INPUT.json|-]"]})
        return 2
    try:
        if arguments and arguments[0] != "-":
            with open(arguments[0], encoding="utf-8") as stream:
                value = json.load(stream)
        else:
            value = json.load(sys.stdin)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _emit({"version": 1, "overall_status": "INVALID", "errors": [f"invalid input: {type(exc).__name__}"]})
        return 2
    errors = validate_input(value)
    if errors:
        _emit({"version": 1, "overall_status": "INVALID", "errors": errors})
        return 2
    try:
        result = evaluate(value)
        _emit(result)
    except Exception:
        try:
            _emit({"version": 1, "overall_status": "FAIL", "errors": ["internal_validation_failure"]})
        except Exception:
            sys.stdout.write('{"errors":["serialization_failure"],"overall_status":"FAIL","version":1}\n')
        return 1
    return 0 if result["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
