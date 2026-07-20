#!/usr/bin/env python3
"""Exact-head CI adapter for the trusted governance PR gate."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping


SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
ALLOWED_PATHS = [
    ".github/workflows/governance-pr-gate-shadow.yml",
    "tools/governance_pr_gate_ci.py",
    "tests/test_governance_pr_gate_ci.py",
]


class InputError(ValueError):
    """The GitHub event or environment cannot form a safe invocation."""


def _required_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise InputError(f"{name} must be a non-empty string")
    return value


def build_context(event: Any, env: Mapping[str, str]) -> dict[str, Any]:
    if not isinstance(event, dict) or not isinstance(event.get("pull_request"), dict):
        raise InputError("event must contain pull_request")
    pr = event["pull_request"]
    try:
        repository = _required_string(event["repository"]["full_name"], "repository.full_name")
        number = pr["number"]
        base = _required_string(pr["base"]["sha"], "pull_request.base.sha").lower()
        head = _required_string(pr["head"]["sha"], "pull_request.head.sha").lower()
        base_repo = _required_string(pr["base"]["repo"]["full_name"], "pull_request.base.repo.full_name")
        head_repo = _required_string(pr["head"]["repo"]["full_name"], "pull_request.head.repo.full_name")
    except (KeyError, TypeError) as exc:
        raise InputError("event is missing required pull-request fields") from exc
    if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
        raise InputError("pull_request.number must be a positive integer")
    if not SHA_RE.fullmatch(base) or not SHA_RE.fullmatch(head):
        raise InputError("base and head must be full 40-hex SHAs")
    if repository != base_repo:
        raise InputError("event repository must equal base repository")
    if _required_string(env.get("GITHUB_REPOSITORY"), "GITHUB_REPOSITORY") != repository:
        raise InputError("GITHUB_REPOSITORY must equal event repository")
    return {
        "repository": repository,
        "pr_number": number,
        "expected_base": base,
        "expected_head": head,
        "base_repository": base_repo,
        "head_repository": head_repo,
        "eligibility": "same_repository" if head_repo == base_repo else "fork_unsupported",
        "workflow_run_id": _required_string(env.get("GITHUB_RUN_ID"), "GITHUB_RUN_ID"),
        "workflow_run_attempt": _required_string(env.get("GITHUB_RUN_ATTEMPT"), "GITHUB_RUN_ATTEMPT"),
    }


def _observed_head(candidate_dir: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=candidate_dir, check=False,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = result.stdout.strip().lower()
    return value if result.returncode == 0 and SHA_RE.fullmatch(value) else None


def make_evidence(context: dict[str, Any], observed_head: str | None, exit_code: int,
                  validator_result: Any) -> dict[str, Any]:
    mechanical = "PASS" if exit_code == 0 else "NO_MECHANICAL_PASS"
    return {
        "version": 1,
        **context,
        "observed_candidate_head": observed_head,
        "validator_exit_code": exit_code,
        "mechanical_result": mechanical,
        "validator_result": validator_result,
    }


def run(event: Any, env: Mapping[str, str], candidate_dir: Path,
        validator_path: Path) -> tuple[int, dict[str, Any]]:
    context = build_context(event, env)
    observed = _observed_head(candidate_dir) if candidate_dir.is_dir() else None
    if context["eligibility"] != "same_repository":
        result = {"version": 1, "overall_status": "INVALID", "errors": ["fork_pr_unsupported"]}
        return 1, make_evidence(context, observed, 1, result)

    envelope = {
        "version": 1,
        "repository": context["repository"],
        "expected_base": context["expected_base"],
        "expected_head": context["expected_head"],
        "allowed_paths": ALLOWED_PATHS,
    }
    try:
        completed = subprocess.run(
            [sys.executable, str(validator_path), "-"],
            cwd=candidate_dir,
            input=json.dumps(envelope),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        exit_code = completed.returncode
        try:
            validator_result: Any = json.loads(completed.stdout)
        except json.JSONDecodeError:
            validator_result = {
                "version": 1, "overall_status": "FAIL",
                "errors": ["validator_output_not_json"],
            }
            exit_code = 1
    except (OSError, subprocess.SubprocessError):
        exit_code = 1
        validator_result = {
            "version": 1, "overall_status": "FAIL",
            "errors": ["validator_unavailable"],
        }
    return exit_code, make_evidence(context, observed, exit_code, validator_result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_repo_dir", type=Path)
    parser.add_argument("--event-path", type=Path, default=None)
    args = parser.parse_args(argv)
    event_path = args.event_path or (Path(os.environ["GITHUB_EVENT_PATH"]) if os.environ.get("GITHUB_EVENT_PATH") else None)
    try:
        if event_path is None:
            raise InputError("GITHUB_EVENT_PATH is required")
        event = json.loads(event_path.read_text(encoding="utf-8"))
        code, evidence = run(event, os.environ, args.candidate_repo_dir.resolve(), Path(__file__).with_name("governance_pr_gate.py").resolve())
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        code = 2
        evidence = {
            "version": 1, "mechanical_result": "NO_MECHANICAL_PASS",
            "validator_exit_code": 2,
            "validator_result": {"version": 1, "overall_status": "INVALID", "errors": [str(exc)]},
        }
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
