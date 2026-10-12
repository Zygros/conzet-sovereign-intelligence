"""Governed daemon factory: plans tasks from a declarative registry; never self-executes code."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ALLOWED_TASK_STATES = {"PLANNED", "BLOCKED"}

def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "conzetian-daemon-registry/1.0":
        raise ValueError("unsupported daemon registry schema")
    daemons = data.get("daemons")
    if not isinstance(daemons, list):
        raise ValueError("daemons must be a list")
    ids = set()
    for daemon in daemons:
        if not isinstance(daemon, dict):
            raise ValueError("each daemon entry must be an object")
        daemon_id = daemon.get("id")
        if not isinstance(daemon_id, str) or not daemon_id.strip():
            raise ValueError("each daemon requires a non-empty id")
        if daemon_id in ids:
            raise ValueError("duplicate daemon id: " + daemon_id)
        ids.add(daemon_id)
        if daemon.get("mode") not in {"observe", "plan", "verify"}:
            raise ValueError("unsupported mode for daemon: " + daemon_id)
        if daemon.get("enabled") is not True:
            continue
        if daemon.get("adapter") not in (None, ""):
            raise ValueError("external adapters must be registered in trusted runtime, not in JSON")
    return data

def plan_cycle(registry: dict[str, Any], cycle_id: str) -> list[dict[str, Any]]:
    if not isinstance(cycle_id, str) or not cycle_id.strip():
        raise ValueError("cycle_id must be a non-empty string")
    tasks = []
    for daemon in registry["daemons"]:
        if daemon.get("enabled") is not True:
            continue
        tasks.append({
            "schema": "conzetian-daemon-task/1.0",
            "cycle_id": cycle_id,
            "task_id": cycle_id + ":" + daemon["id"],
            "daemon_id": daemon["id"],
            "purpose": daemon["purpose"],
            "mode": daemon["mode"],
            "state": "PLANNED" if daemon["mode"] in {"observe", "plan"} else "BLOCKED",
            "requires_trusted_adapter": daemon.get("requires_trusted_adapter", False),
            "automatic_execution": False,
            "evidence_required": True,
        })
    return tasks

def write_plan(registry_path: Path, output_path: Path, cycle_id: str) -> list[dict[str, Any]]:
    registry = load_registry(registry_path)
    tasks = plan_cycle(registry, cycle_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"schema": "conzetian-daemon-cycle/1.0", "tasks": tasks}, indent=2) + "\n", encoding="utf-8")
    return tasks

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cycle-id", required=True)
    args = parser.parse_args()
    planned = write_plan(args.registry, args.output, args.cycle_id)
    print(json.dumps({"status": "PLANNED", "task_count": len(planned), "output": str(args.output)}, indent=2))