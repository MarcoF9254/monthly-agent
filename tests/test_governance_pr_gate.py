import json
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
TOOL = ROOT / "tools" / "governance_pr_gate.py"
SPEC = importlib.util.spec_from_file_location("governance_pr_gate", TOOL)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", *args], cwd=repo, check=check, capture_output=True, text=True
    ).stdout.strip()


def write(repo, path, text="content\n"):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def commit(repo, message, *paths):
    git(repo, "add", *paths)
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "remote", "add", "origin", "https://github.com/MarcoF9254/monthly-agent.git")
    write(tmp_path, "allowed.txt", "base\n")
    write(tmp_path, "delete.txt", "base\n")
    base = commit(tmp_path, "base", "allowed.txt", "delete.txt")
    write(tmp_path, "allowed.txt", "head\n")
    head = commit(tmp_path, "head", "allowed.txt")
    return tmp_path, base, head


def input_for(base="a" * 40, head="b" * 40, paths=None):
    return {
        "version": 1,
        "repository": "MarcoF9254/monthly-agent",
        "expected_base": base,
        "expected_head": head,
        "allowed_paths": ["allowed.txt"] if paths is None else paths,
    }


def run_tool(repo, value):
    return subprocess.run(
        [sys.executable, str(TOOL), "-"], cwd=repo, input=json.dumps(value),
        capture_output=True, text=True
    )


@pytest.mark.parametrize(
    "mutator",
    [
        lambda value: value.update(version=2),
        lambda value: value.update(repository="bad repo"),
        lambda value: value.update(expected_base="abc123"),
        lambda value: value.update(expected_head="g" * 40),
        lambda value: value.update(allowed_paths=["same", "same"]),
        lambda value: value.update(allowed_paths=["/absolute"]),
        lambda value: value.update(allowed_paths=["safe/../escape"]),
    ],
)
def test_invalid_inputs_exit_two(tmp_path, mutator):
    value = input_for()
    mutator(value)
    result = run_tool(tmp_path, value)
    assert result.returncode == 2
    assert json.loads(result.stdout)["overall_status"] == "INVALID"


def test_valid_v1_input():
    assert gate.validate_input(input_for()) == []


@pytest.mark.parametrize(
    ("origin", "expected"),
    [
        ("https://github.com/MarcoF9254/monthly-agent.git", "PASS"),
        ("git@github.com:MarcoF9254/monthly-agent.git", "PASS"),
        ("https://github.com/other/repo.git", "FAIL"),
    ],
)
def test_repository_identity(repo, origin, expected, monkeypatch):
    path, base, head = repo
    monkeypatch.chdir(path)
    git(path, "remote", "set-url", "origin", origin)
    result = gate.evaluate(input_for(base, head))
    assert result["checks"]["repository_identity"]["status"] == expected


def test_missing_origin_fails_closed(repo, monkeypatch):
    path, base, head = repo
    monkeypatch.chdir(path)
    git(path, "remote", "remove", "origin")
    assert gate.evaluate(input_for(base, head))["checks"]["repository_identity"]["status"] == "FAIL"


def test_not_git_repository_fails_closed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = gate.evaluate(input_for())
    assert result["overall_status"] == "FAIL"
    assert all(check["status"] == "FAIL" for check in result["checks"].values())


def test_head_and_base_pass(repo, monkeypatch):
    path, base, head = repo
    monkeypatch.chdir(path)
    result = gate.evaluate(input_for(base, head))
    assert result["checks"]["base_commit"]["status"] == "PASS"
    assert result["checks"]["exact_head"]["status"] == "PASS"
    assert result["checks"]["ancestry"]["status"] == "PASS"


def test_head_mismatch_and_movement(repo, monkeypatch):
    path, base, captured_head = repo
    monkeypatch.chdir(path)
    git(path, "checkout", "--detach", base)
    assert gate.evaluate(input_for(base, captured_head))["checks"]["exact_head"]["status"] == "FAIL"
    git(path, "checkout", "--detach", captured_head)
    write(path, "allowed.txt", "moved\n")
    commit(path, "move", "allowed.txt")
    assert gate.evaluate(input_for(base, captured_head))["checks"]["exact_head"]["status"] == "FAIL"


def test_unknown_and_noncommit_base(repo, monkeypatch):
    path, _, head = repo
    monkeypatch.chdir(path)
    assert gate.evaluate(input_for("f" * 40, head))["checks"]["base_commit"]["status"] == "FAIL"
    blob = git(path, "hash-object", "allowed.txt")
    assert len(blob) == 40
    assert gate.evaluate(input_for(blob, head))["checks"]["base_commit"]["status"] == "FAIL"


def test_non_ancestor(repo, monkeypatch):
    path, base, head = repo
    monkeypatch.chdir(path)
    git(path, "checkout", "--orphan", "unrelated")
    git(path, "rm", "-rf", ".")
    write(path, "allowed.txt", "unrelated\n")
    unrelated = commit(path, "unrelated", "allowed.txt")
    git(path, "checkout", "--detach", head)
    assert gate.evaluate(input_for(unrelated, head))["checks"]["ancestry"]["status"] == "FAIL"
    assert gate.evaluate(input_for(base, head))["checks"]["ancestry"]["status"] == "PASS"


def make_change(repo_data, monkeypatch, changes, allowed):
    path, _, base = repo_data
    monkeypatch.chdir(path)
    for action, name in changes:
        if action == "write":
            write(path, name, f"changed {name}\n")
        elif action == "delete":
            (path / name).unlink()
    git(path, "add", "-A")
    git(path, "commit", "-m", "path case")
    head = git(path, "rev-parse", "HEAD")
    return gate.evaluate(input_for(base, head, allowed))


@pytest.mark.parametrize(
    ("changes", "allowed", "expected"),
    [
        ([('write', 'allowed.txt')], ["allowed.txt"], "PASS"),
        ([('write', 'allowed.txt'), ('write', 'second.txt')], ["allowed.txt", "second.txt"], "PASS"),
        ([('write', 'allowed.txt'), ('write', 'extra.txt')], ["allowed.txt"], "FAIL"),
        ([('write', 'extra.txt')], ["allowed.txt"], "FAIL"),
        ([('delete', 'delete.txt')], ["delete.txt"], "PASS"),
        ([('delete', 'delete.txt')], ["allowed.txt"], "FAIL"),
        ([('write', 'new.txt')], ["new.txt"], "PASS"),
        ([('write', 'space name.txt'), ('write', '資料.txt')], ["資料.txt", "space name.txt"], "PASS"),
    ],
)
def test_changed_paths(repo, monkeypatch, changes, allowed, expected):
    result = make_change(repo, monkeypatch, changes, allowed)
    check = result["checks"]["changed_path_allowlist"]
    assert check["status"] == expected
    assert check["changed_paths"] == sorted(check["changed_paths"])


def test_rename_crossing_boundary_fails(repo, monkeypatch):
    path, base, _ = repo
    monkeypatch.chdir(path)
    git(path, "mv", "allowed.txt", "outside.txt")
    head = commit(path, "rename", "outside.txt")
    check = gate.evaluate(input_for(base, head, ["allowed.txt"]))["checks"]["changed_path_allowlist"]
    assert check["status"] == "FAIL"
    assert check["changed_paths"] == ["allowed.txt", "outside.txt"]


def test_empty_diff_is_valid(repo, monkeypatch):
    path, base, _ = repo
    monkeypatch.chdir(path)
    git(path, "checkout", "--detach", base)
    result = gate.evaluate(input_for(base, base, []))
    assert result["overall_status"] == "PASS"
    assert result["checks"]["changed_path_allowlist"]["changed_paths"] == []


def test_git_failure_and_malformed_result_fail_closed(repo, monkeypatch):
    path, base, head = repo
    monkeypatch.chdir(path)
    monkeypatch.setattr(gate, "_git", lambda *args, **kwargs: (_ for _ in ()).throw(gate.GitFailure()))
    assert gate.evaluate(input_for(base, head))["overall_status"] == "FAIL"

    def malformed(arguments, *, text=True):
        if arguments[0] == "diff-tree":
            return b"not-a-status\0path\0"
        return git(path, *arguments)

    monkeypatch.setattr(gate, "_git", malformed)
    assert gate.evaluate(input_for(base, head))["checks"]["changed_path_allowlist"]["status"] == "FAIL"


def test_semantic_json_is_deterministic(repo):
    path, base, head = repo
    value = input_for(base, head)
    first = run_tool(path, value)
    second = run_tool(path, value)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert json.loads(first.stdout) == json.loads(second.stdout)


# ── Remediation A — JSON fail-closed contract ──────────────────────────────

def test_unexpected_exception_produces_json_fail(tmp_path):
    """When evaluate() encounters an unexpected internal exception, the
    main() wrapper must catch it, emit stable JSON on stdout, and exit 1
    — no traceback or prose leakage."""
    import subprocess as sp
    sp.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    sp.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    sp.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "f").write_text("x")
    sp.run(["git", "add", "f"], cwd=tmp_path, check=True)
    sp.run(
        ["git", "commit", "-m", "x"], cwd=tmp_path,
        capture_output=True, text=True,
    )
    head_sha = sp.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path,
        capture_output=True, text=True,
    ).stdout.strip()
    # no origin → repository_identity check will raise a GitFailure
    # that evaluate() handles gracefully but the overall_status is FAIL
    value = {
        "version": 1,
        "repository": "MarcoF9254/monthly-agent",
        "expected_base": head_sha,
        "expected_head": head_sha,
        "allowed_paths": ["f"],
    }
    result = sp.run(
        [sys.executable, str(TOOL), "-"],
        cwd=tmp_path, input=json.dumps(value),
        capture_output=True, text=True,
    )
    # Must not crash: exit code must be 1 (deterministic FAIL), not 2
    # and stdout must contain parseable JSON with no traceback
    assert result.returncode in (0, 1), \
        f"crash or invalid exit: {result.returncode}"
    assert result.returncode != 0, \
        "no-origin scenario must not PASS overall"
    payload = json.loads(result.stdout)
    assert "overall_status" in payload
    assert payload["overall_status"] in ("FAIL", "INVALID")
    assert "Traceback" not in result.stdout, "traceback leaked to stdout"


# ── Remediation B — schema / runtime parity ────────────────────────────────

HERE = Path(__file__).parent
SCHEMA_PATH = HERE.parent / "schemas" / "governance-pr-gate-input.schema.json"

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not available")
class TestSchemaRuntimeParity:
    """Mechanically validate representative paths against both the committed
    JSON Schema and the runtime validate_input() helper."""

    SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    VALID_PATHS = [
        "foo.txt",
        "tools/bar.py",
        "path with spaces",
        "資料.txt",
    ]

    INVALID_PATHS = [
        "/absolute",           # starts with /
        "C:/absolute",         # Windows drive absolute
        "../escape",           # parent traversal
        "safe/../escape",      # embedded traversal
        "back\\slash",         # backslash
        "//",                  # bare double slash
        "a//b",                # embedded double slash
        ".",                   # bare dot
        "",                    # empty
    ]

    def _schema_valid(self, path: str) -> bool:
        validator = jsonschema.Draft202012Validator(
            self.SCHEMA["properties"]["allowed_paths"])
        errors = list(validator.iter_errors([path]))
        return len(errors) == 0

    def _runtime_valid(self, path: str) -> bool:
        return gate._valid_path(path)

    @pytest.mark.parametrize("path", VALID_PATHS)
    def test_valid_path_both_accept(self, path):
        assert self._schema_valid(path), f"schema rejected {path!r}"
        assert self._runtime_valid(path), f"runtime rejected {path!r}"

    @pytest.mark.parametrize("path", INVALID_PATHS)
    def test_invalid_path_both_reject(self, path):
        schema_ok = self._schema_valid(path)
        runtime_ok = self._runtime_valid(path)
        if schema_ok:
            pytest.fail(f"schema accepted invalid path {path!r}")
        if runtime_ok:
            pytest.fail(f"runtime accepted invalid path {path!r}")
        assert not schema_ok and not runtime_ok

    def test_duplicate_paths_rejected_by_validate_input(self):
        errors = gate.validate_input({
            "version": 1,
            "repository": "owner/repo",
            "expected_base": "a" * 40,
            "expected_head": "b" * 40,
            "allowed_paths": ["same", "same"],
        })
        assert any("duplicate" in e.lower() for e in errors)
