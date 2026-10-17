"""Independent structural verifier for PHOENIX-generated tool packages.

This verifier intentionally does not execute candidate tool code. It checks
provenance, syntax, and a small fail-closed safety surface before promotion.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any

BANNED_TEXT = ("__import__", "eval(", "exec(", "os.system", "subprocess")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_package(package: str | Path) -> dict[str, Any]:
    root = Path(package)
    tool = root / "tool.py"
    tests = root / "test_tool.py"
    manifest = root / "tool.json"
    receipt = root / "factory_receipt.json"

    checks = {
        "tool_exists": tool.is_file(),
        "tests_exist": tests.is_file(),
        "manifest_exists": manifest.is_file(),
        "receipt_exists": receipt.is_file(),
    }
    if not all(checks.values()):
        return {"verified": False, "checks": checks, "reason": "missing required artifact"}

    source = tool.read_text(encoding="utf-8")
    tree = ast.parse(source)
    checks["syntax"] = True
    checks["no_imports"] = not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))
    checks["no_banned_primitives"] = not any(x in source for x in BANNED_TEXT)

    data = json.loads(manifest.read_text(encoding="utf-8"))
    checks["source_hash"] = data.get("source_sha256") == sha256_file(tool)
    checks["promotion_blocked_until_verification"] = (
        data.get("promotion") == "blocked-until-independent-verification"
    )

    verified = all(checks.values())
    return {
        "verified": verified,
        "checks": checks,
        "tool": data.get("name"),
        "source_sha256": sha256_file(tool),
    }


if __name__ == "__main__":
    import sys

    result = verify_package(sys.argv[1])
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["verified"] else 1)
