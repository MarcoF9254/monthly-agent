#!/usr/bin/env python3
"""Offline, mechanical PR-envelope validation against a local Git repository."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import PurePosixPath
from typing import Any


SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
HTTPS_ORIGIN_RE = re.compile(
    r"^https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)
SSH_ORIGIN_RE = re.compile(
    r"^git@github\.com:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?$"
)


class GitFailure(Exception):
    """A local Git query failed or returned unusable data."""


def _git(arguments: list[str], *, text: bool = True) -> str | bytes:
    try:
        result = subprocess.run(
            ["git", *arguments],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=text,
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
    errors: list[str] = []
    required = {"version", "repository", "expected_base", "expected_head", "allowed_paths"}
    if not isinstance(value, dict):
        return ["input must be a JSON object"]
    missing = sorted(required - value.keys())
    extra = sorted(value.keys() - required)
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if extra:
        errors.append("unknown fields: " + ", ".join(extra))
    if value.get("version") != 1 or isinstance(value.get("version"), bool):
        errors.append("version must be 1")
    repository = value.get("repository")
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        errors.append("repository must be OWNER/REPO")
    for field in ("expected_base", "expected_head"):
        sha = value.get(field)
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            errors.append(f"{field} must be a full 40-hex SHA")
    paths = value.get("allowed_paths")
    if not isinstance(paths, list):
        errors.append("allowed_paths must be an array")
    else:
        if any(not _valid_path(path) for path in paths):
            errors.append("allowed_paths must contain normalized repository-relative Git paths")
        if all(isinstance(path, str) for path in paths) and len(paths) != len(set(paths)):
            errors.append("allowed_paths must not contain duplicates")
    return sorted(errors)


def _canonical_origin(origin: str) -> str | None:
    origin = origin.strip()
    for pattern in (HTTPS_ORIGIN_RE, SSH_ORIGIN_RE):
        match = pattern.fullmatch(origin)
        if match:
            return match.group(1)
    return None


def _commit(sha: str) -> str | None:
    try:
        object_type = _git(["cat-file", "-t", sha]).strip()
        observed = _git(["rev-parse", "--verify", sha]).strip()
    except GitFailure:
        return None
    if object_type != "commit" or not SHA_RE.fullmatch(observed) or observed.lower() != sha.lower():
        return None
    return observed.lower()


def _changed_paths(base: str, head: str) -> list[str]:
    raw = _git(
        ["diff-tree", "-r", "--no-commit-id", "--name-status", "-z", "-M", "-C", base, head],
        text=False,
    )
    if not isinstance(raw, bytes):
        raise GitFailure
    try:
        fields = raw.decode("utf-8", "surrogateescape").split("\0")
    except UnicodeError as exc:
        raise GitFailure from exc
    if fields[-1] != "":
        raise GitFailure
    fields.pop()
    paths: list[str] = []
    index = 0
    while index < len(fields):
        status = fields[index]
        index += 1
        if not re.fullmatch(r"[ACDMRTUXB](?:[0-9]{1,3})?", status):
            raise GitFailure
        path_count = 2 if status[0] in {"R", "C"} else 1
        if index + path_count > len(fields):
            raise GitFailure
        candidates = fields[index : index + path_count]
        if any(not path or "\x00" in path for path in candidates):
            raise GitFailure
        paths.extend(candidates)
        index += path_count
    return sorted(set(paths))


def evaluate(value: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}

    try:
        observed_repository = _canonical_origin(str(_git(["config", "--get", "remote.origin.url"])))
    except GitFailure:
        observed_repository = None
    repository_pass = observed_repository == value["repository"]
    checks["repository_identity"] = {
        "status": "PASS" if repository_pass else "FAIL",
        "observed": observed_repository,
    }

    base = _commit(value["expected_base"])
    checks["base_commit"] = {"status": "PASS" if base else "FAIL", "observed": base}

    try:
        observed_head_raw = str(_git(["rev-parse", "HEAD"])).strip()
        observed_head = observed_head_raw.lower() if SHA_RE.fullmatch(observed_head_raw) else None
    except GitFailure:
        observed_head = None
    head_object = _commit(value["expected_head"])
    head_pass = head_object is not None and observed_head == value["expected_head"].lower()
    checks["exact_head"] = {"status": "PASS" if head_pass else "FAIL", "observed": observed_head}

    ancestry_pass = False
    if base and head_object:
        try:
            _git(["merge-base", "--is-ancestor", base, head_object])
            ancestry_pass = True
        except GitFailure:
            pass
    checks["ancestry"] = {"status": "PASS" if ancestry_pass else "FAIL"}

    changed_paths: list[str] = []
    paths_available = False
    if base and head_object:
        try:
            changed_paths = _changed_paths(base, head_object)
            paths_available = True
        except GitFailure:
            pass
    unauthorized = sorted(set(changed_paths) - set(value["allowed_paths"])) if paths_available else []
    path_pass = paths_available and not unauthorized
    checks["changed_path_allowlist"] = {
        "status": "PASS" if path_pass else "FAIL",
        "changed_paths": changed_paths,
        "unauthorized_paths": unauthorized,
    }

    return {
        "version": 1,
        "overall_status": "PASS" if all(check["status"] == "PASS" for check in checks.values()) else "FAIL",
        "checks": checks,
    }


def _emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) > 1:
        _emit({"version": 1, "overall_status": "INVALID", "errors": ["usage: governance_pr_gate.py [INPUT.json|-]"]})
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
    except Exception:
        _emit({
            "version": 1,
            "overall_status": "FAIL",
            "errors": ["internal_validation_failure"],
        })
        return 1
    _emit(result)
    return 0 if result["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
