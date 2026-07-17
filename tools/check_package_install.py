import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install a built wheel in an isolated environment and verify package metadata."
    )
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args(argv)
    wheel = args.wheel.resolve()
    if not wheel.is_file() or wheel.suffix != ".whl":
        parser.error(f"wheel does not exist: {wheel}")

    with tempfile.TemporaryDirectory(prefix="monthly-agent-wheel-") as directory:
        target = Path(directory) / "site-packages"
        run(["uv", "pip", "install", "--target", str(target), str(wheel)])
        probe = (
            "import importlib.metadata, importlib.util, json; "
            "print(json.dumps({"
            "'version': importlib.metadata.version('monthly-agent'), "
            "'oar_verifier': importlib.util.find_spec('tools.oar_verifier') is not None, "
            "'business_rules': importlib.util.find_spec('validators.business_rules') is not None"
            "}, sort_keys=True))"
        )
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(target)
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        result = json.loads(completed.stdout)
        if result != {
            "business_rules": True,
            "oar_verifier": True,
            "version": "0.0.0",
        }:
            raise RuntimeError(f"unexpected installed-package probe: {result}")
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
