#!/usr/bin/env python3
"""Render a deterministic Phoenix agent activation plan from the role registry.

This tool validates role definitions and emits a dispatch plan. It does not
start language-model workers, create remote processes, or execute agent tasks.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "agents" / "registry.json"


def load_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("agents"), list):
        raise ValueError("registry must be an object containing an agents list")
    return data


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    agents = registry.get("agents", [])
    ids: list[str] = []
    for index, agent in enumerate(agents):
        prefix = f"agents[{index}]"
        if not isinstance(agent, dict):
            errors.append(f"{prefix} must be an object")
            continue
        agent_id = agent.get("id")
        if not isinstance(agent_id, str) or not agent_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        ids.append(agent_id)
        for field in ("name", "mission", "layer"):
            if not isinstance(agent.get(field), str) or not agent[field].strip():
                errors.append(f"{agent_id}.{field} must be a non-empty string")
        for field in ("inputs", "outputs", "permissions", "prohibited", "depends_on"):
            if not isinstance(agent.get(field), list):
                errors.append(f"{agent_id}.{field} must be a list")
        if agent_id in agent.get("depends_on", []):
            errors.append(f"{agent_id} cannot depend on itself")
    if len(ids) != len(set(ids)):
        errors.append("agent IDs must be unique")
    known = set(ids)
    for agent in agents:
        if isinstance(agent, dict) and isinstance(agent.get("depends_on"), list):
            for dependency in agent["depends_on"]:
                if dependency not in known:
                    errors.append(f"{agent.get('id', '<unknown>')} has unknown dependency {dependency}")
    return errors


def build_plan(registry: dict[str, Any]) -> dict[str, Any]:
    agents = registry["agents"]
    return {
        "schema_version": "1.0.0",
        "system": registry.get("system", "Phoenix Protocol"),
        "status": "PLAN_GENERATED_NO_WORKERS_STARTED",
        "agent_count": len(agents),
        "execution_boundary": (
            "Role definitions and dispatch order only. No model workers or remote "
            "processes are started by this command."
        ),
        "dispatch_plan": [
            {
                "sequence": index + 1,
                "agent_id": agent["id"],
                "name": agent["name"],
                "mission": agent["mission"],
                "depends_on": agent["depends_on"],
                "permissions": agent["permissions"],
                "requires_approval_for_side_effects": True,
                "status": "DEFINED_READY_FOR_RUNTIME_BINDING",
            }
            for index, agent in enumerate(agents)
        ],
        "operating_invariants": registry.get("operating_invariants", []),
        "activation_requirements": [
            "Bind each role to an actual model/runtime and tool allowlist.",
            "Provide scoped credentials through the runtime secret manager, never in the registry.",
            "Enforce dependency readiness and explicit approval for external side effects.",
            "Persist task IDs, input/output hashes, tool calls, errors, and test receipts.",
            "Run a bounded task end-to-end and obtain independent reproduction before promotion.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        registry = load_registry(args.registry)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    errors = validate_registry(registry)
    if errors:
        print(json.dumps({"status": "INVALID", "errors": errors}, indent=2))
        return 2
    if args.validate_only:
        print(json.dumps({"status": "VALID", "agent_count": len(registry["agents"])}, indent=2))
        return 0
    print(json.dumps(build_plan(registry), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
