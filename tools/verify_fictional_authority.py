import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.oar_verifier import verify


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify one fictional year-2099 OAR scenario offline.")
    parser.add_argument("--scenario-root", required=True)
    parser.add_argument("--bundle-root", required=True)
    parser.add_argument("--trust-anchor", required=True)
    args = parser.parse_args(argv)
    repository_root = ROOT_DIR
    result = verify(
        repository_root,
        Path(args.scenario_root),
        Path(args.bundle_root),
        Path(args.trust_anchor),
    )
    print(json.dumps({
        "success": result.success,
        "classification": result.classification,
        "rule_id": result.rule_id,
        "primary_component": result.primary_component,
        "rejection_stage": result.rejection_stage,
        "message": result.message,
        "outcome": result.outcome,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
