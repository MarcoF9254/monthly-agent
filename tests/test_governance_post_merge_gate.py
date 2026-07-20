import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
TOOL = ROOT / "tools" / "governance_post_merge_gate.py"
SPEC = importlib.util.spec_from_file_location("governance_post_merge_gate", TOOL)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def git(repo, *args, check=True):
    return subprocess.run(["git", *args], cwd=repo, check=check, capture_output=True, text=True).stdout.strip()


def write(repo, path, text):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def merged_repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "remote", "add", "origin", "https://github.com/MarcoF9254/monthly-agent.git")
    write(tmp_path, "activity.txt", "base\n")
    base = commit(tmp_path, "base")
    git(tmp_path, "branch", "main")
    git(tmp_path, "checkout", "-q", "-b", "review")
    write(tmp_path, "activity.txt", "reviewed\n")
    reviewed = commit(tmp_path, "review")
    git(tmp_path, "checkout", "-q", "main")
    git(tmp_path, "merge", "--no-ff", "review", "-m", "merge")
    merge = git(tmp_path, "rev-parse", "HEAD")
    return tmp_path, base, reviewed, merge


def envelope(base, reviewed, merge, paths=None, main_ref="refs/heads/main"):
    return {
        "version": 1, "repository": "MarcoF9254/monthly-agent", "merge_commit": merge,
        "expected_base": base, "expected_reviewed_head": reviewed,
        "expected_landed_paths": ["activity.txt"] if paths is None else paths, "main_ref": main_ref,
    }


def run_tool(repo, value):
    return subprocess.run([sys.executable, str(TOOL), "-"], cwd=repo, input=json.dumps(value), capture_output=True, text=True)


def test_happy_path_and_output_contract(merged_repo, monkeypatch):
    path, base, reviewed, merge = merged_repo
    monkeypatch.chdir(path)
    result = gate.evaluate(envelope(base, reviewed, merge))
    assert result["overall_status"] == "PASS"
    assert result["observed_parents"] == [base, reviewed]
    assert result["observed_main"] == merge
    assert result["main_ref_freshness"] == "CALLER_RESPONSIBILITY"
    assert all(check["status"] == "PASS" for check in result["checks"].values())


def test_single_parent_fails_topology(merged_repo, monkeypatch):
    path, base, reviewed, _ = merged_repo
    monkeypatch.chdir(path)
    result = gate.evaluate(envelope(base, reviewed, reviewed, main_ref="refs/heads/review"))
    assert result["checks"]["merge_topology"]["status"] == "FAIL"
    assert result["checks"]["merge_topology"]["parent_count"] == 1


def test_wrong_first_and_second_parent(merged_repo, monkeypatch):
    path, base, reviewed, merge = merged_repo
    monkeypatch.chdir(path)
    wrong_first = gate.evaluate(envelope("f" * 40, reviewed, merge))
    wrong_second = gate.evaluate(envelope(base, base, merge))
    assert wrong_first["checks"]["first_parent_binding"]["status"] == "FAIL"
    assert wrong_second["checks"]["second_parent_binding"]["status"] == "FAIL"


def test_reviewed_head_not_descendant(merged_repo, monkeypatch):
    path, base, reviewed, merge = merged_repo
    monkeypatch.chdir(path)
    git(path, "checkout", "-q", "--orphan", "unrelated")
    git(path, "rm", "-rf", ".")
    write(path, "other", "x\n")
    unrelated = commit(path, "unrelated")
    result = gate.evaluate(envelope(base, unrelated, merge, main_ref="refs/heads/main"))
    assert result["checks"]["reviewed_head_ancestry"]["status"] == "FAIL"


def test_extra_commit_causes_second_parent_mismatch(merged_repo, monkeypatch):
    path, base, reviewed, _ = merged_repo
    monkeypatch.chdir(path)
    git(path, "checkout", "-q", "review")
    write(path, "extra.txt", "extra\n")
    later = commit(path, "later")
    git(path, "checkout", "-q", "main")
    git(path, "reset", "--hard", base)
    git(path, "merge", "--no-ff", "review", "-m", "later merge")
    merge = git(path, "rev-parse", "HEAD")
    result = gate.evaluate(envelope(base, reviewed, merge, ["activity.txt", "extra.txt"]))
    assert later != reviewed
    assert result["checks"]["second_parent_binding"]["status"] == "FAIL"


def test_merge_tree_differs_from_reviewed_tree(merged_repo, monkeypatch):
    path, base, reviewed, _ = merged_repo
    monkeypatch.chdir(path)
    git(path, "checkout", "-q", "main")
    git(path, "reset", "--hard", base)
    tree = git(path, "rev-parse", f"{reviewed}^{{tree}}")
    write(path, "merge-only.txt", "x\n")
    git(path, "add", "merge-only.txt")
    altered_tree = git(path, "write-tree")
    merge = subprocess.run(
        ["git", "commit-tree", altered_tree, "-p", base, "-p", reviewed, "-m", "altered merge"],
        cwd=path, check=True, capture_output=True, text=True,
    ).stdout.strip()
    git(path, "update-ref", "refs/heads/main", merge)
    result = gate.evaluate(envelope(base, reviewed, merge, ["activity.txt", "merge-only.txt"]))
    assert tree != altered_tree
    assert result["checks"]["reviewed_tree_integrity"]["status"] == "FAIL"


@pytest.mark.parametrize(("paths", "extra", "missing"), [([], ["activity.txt"], []), (["activity.txt", "missing.txt"], [], ["missing.txt"])])
def test_exact_landed_scope(merged_repo, monkeypatch, paths, extra, missing):
    path, base, reviewed, merge = merged_repo
    monkeypatch.chdir(path)
    check = gate.evaluate(envelope(base, reviewed, merge, paths))["checks"]["landed_scope"]
    assert check["status"] == "FAIL"
    assert check["extra"] == extra
    assert check["missing"] == missing


def test_rename_is_deletion_and_addition_without_detection(merged_repo, monkeypatch):
    path, base, _, _ = merged_repo
    monkeypatch.chdir(path)
    git(path, "checkout", "-q", "review")
    git(path, "mv", "activity.txt", "renamed.txt")
    reviewed = commit(path, "rename")
    git(path, "checkout", "-q", "main")
    git(path, "reset", "--hard", base)
    git(path, "merge", "--no-ff", "review", "-m", "rename merge")
    merge = git(path, "rev-parse", "HEAD")
    result = gate.evaluate(envelope(base, reviewed, merge, ["activity.txt", "renamed.txt"]))
    assert result["checks"]["landed_scope"]["status"] == "PASS"
    assert result["observed_landed_paths"] == ["activity.txt", "renamed.txt"]


def test_main_advanced_and_diverged(merged_repo, monkeypatch):
    path, base, reviewed, merge = merged_repo
    monkeypatch.chdir(path)
    write(path, "after.txt", "after\n")
    commit(path, "after")
    advanced = gate.evaluate(envelope(base, reviewed, merge))["checks"]["main_binding"]
    assert advanced["reason"] == "main_advanced_beyond_target_merge"
    git(path, "checkout", "-q", "--orphan", "diverged")
    git(path, "rm", "-rf", ".")
    write(path, "different", "x\n")
    commit(path, "different")
    diverged = gate.evaluate(envelope(base, reviewed, merge, main_ref="refs/heads/diverged"))["checks"]["main_binding"]
    assert diverged["reason"] == "main_ref_mismatch"


def test_missing_history_and_unknown_diff_status_fail_closed(merged_repo, monkeypatch):
    path, base, reviewed, merge = merged_repo
    monkeypatch.chdir(path)
    assert gate.evaluate(envelope(base, reviewed, "f" * 40))["overall_status"] == "FAIL"
    original = gate._git
    def malformed(arguments, *, text=True):
        if arguments[0] == "diff-tree":
            return b"R100\0old\0new\0"
        return original(arguments, text=text)
    monkeypatch.setattr(gate, "_git", malformed)
    assert gate.evaluate(envelope(base, reviewed, merge))["checks"]["landed_scope"]["status"] == "FAIL"


@pytest.mark.parametrize("mutation", [
    lambda value: value.update(merge_commit="bad"),
    lambda value: value.update(version=2),
    lambda value: value.update(expected_landed_paths=["../bad"]),
    lambda value: value.update(extra=True),
])
def test_invalid_input_exits_two(tmp_path, mutation):
    value = envelope("a" * 40, "b" * 40, "c" * 40)
    mutation(value)
    result = run_tool(tmp_path, value)
    assert result.returncode == 2
    assert json.loads(result.stdout)["overall_status"] == "INVALID"


def test_internal_failure_is_structured_no_mechanical_pass(monkeypatch, capsys):
    value = envelope("a" * 40, "b" * 40, "c" * 40)
    monkeypatch.setattr(gate, "evaluate", lambda _: (_ for _ in ()).throw(RuntimeError("boom")))
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO(json.dumps(value)))
    assert gate.main([]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["overall_status"] == "FAIL"
    assert payload["errors"] == ["internal_validation_failure"]
