"""PHOENIX Tool Factory — capability-gap -> tool package compiler.

The factory creates auditable tool artifacts; it does not execute generated code.
Generated tools must pass structural checks before a separate runtime may promote them.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FACTORY_VERSION = "0.1.0"
SAFE_NAME = re.compile(r"^[a-z][a-z0-9_]{2,63}$")


@dataclass(frozen=True)
class ToolSpec:
    name: str
    purpose: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    implementation: str
    tests: str
    dependencies: tuple[str, ...] = ()
    authority: str = "local-sandbox"


@dataclass(frozen=True)
class FactoryReceipt:
    tool_name: str
    factory_version: str
    generated_at: str
    source_sha256: str
    files: tuple[str, ...]
    checks: dict[str, bool]


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_name(name: str) -> None:
    if not SAFE_NAME.fullmatch(name):
        raise ValueError("tool name must be 3-64 chars, lowercase snake_case")


def _validate_python(source: str) -> None:
    tree = ast.parse(source)
    banned = {"Import", "ImportFrom"}
    for node in ast.walk(tree):
        if type(node).__name__ in banned:
            raise ValueError("generated implementation may not import modules")
        if isinstance(node, (ast.Call, ast.Attribute)):
            text = ast.unparse(node)
            if any(x in text for x in ("__import__", "eval(", "exec(", "os.system", "subprocess")):
                raise ValueError("unsafe execution primitive detected")


def _module(spec: ToolSpec) -> str:
    return f'''"""Generated PHOENIX tool: {spec.name}."""
from __future__ import annotations

INPUT_SCHEMA = {json.dumps(spec.input_schema, indent=2)}
OUTPUT_SCHEMA = {json.dumps(spec.output_schema, indent=2)}


def run(payload):
    """Pure tool entry point. External I/O belongs behind an authorized adapter."""
{spec.implementation}
'''


def build_tool(spec: ToolSpec, root: str | Path) -> FactoryReceipt:
    """Compile a tool spec into a package and append a deterministic receipt."""
    _validate_name(spec.name)
    _validate_python(spec.implementation)
    if not spec.tests.strip():
        raise ValueError("at least one test is required")

    root = Path(root)
    package = root / spec.name
    package.mkdir(parents=True, exist_ok=True)
    module_path = package / "tool.py"
    test_path = package / "test_tool.py"
    manifest_path = package / "tool.json"

    module = _module(spec)
    module_path.write_text(module, encoding="utf-8")
    test_path.write_text(spec.tests, encoding="utf-8")
    source_sha = _sha256(module)
    manifest = {
        "factory_version": FACTORY_VERSION,
        "name": spec.name,
        "purpose": spec.purpose,
        "input_schema": spec.input_schema,
        "output_schema": spec.output_schema,
        "dependencies": list(spec.dependencies),
        "authority": spec.authority,
        "source_sha256": source_sha,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "promotion": "blocked-until-independent-verification",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    receipt = FactoryReceipt(
        tool_name=spec.name,
        factory_version=FACTORY_VERSION,
        generated_at=manifest["generated_at"],
        source_sha256=source_sha,
        files=("tool.py", "test_tool.py", "tool.json"),
        checks={"name": True, "ast": True, "tests_present": True, "manifest": True},
    )
    (package / "factory_receipt.json").write_text(
        json.dumps(asdict(receipt), indent=2) + "\n", encoding="utf-8"
    )
    return receipt


def discover_and_build(gaps: list[dict[str, Any]], root: str | Path) -> list[FactoryReceipt]:
    """Turn explicitly described capability gaps into tool artifacts.

    This is intentionally a compiler, not an autonomous authority layer: callers
    provide the implementation candidate and tests; promotion remains separate.
    """
    receipts = []
    for gap in gaps:
        spec = ToolSpec(
            name=gap["name"],
            purpose=gap["purpose"],
            input_schema=gap["input_schema"],
            output_schema=gap["output_schema"],
            implementation=gap["implementation"],
            tests=gap["tests"],
            dependencies=tuple(gap.get("dependencies", ())),
            authority=gap.get("authority", "local-sandbox"),
        )
        receipts.append(build_tool(spec, root))
    return receipts


if __name__ == "__main__":
    print("PHOENIX Tool Factory", FACTORY_VERSION)
    print("Mode: compile artifacts; do not execute generated code")
