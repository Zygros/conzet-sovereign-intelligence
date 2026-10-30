#!/usr/bin/env python3
"""Deterministically validate the Phoenix 420-agent/subagent manifest contract."""
import hashlib
import json
from pathlib import Path

MANIFEST = Path("manifests/PHOENIX_420_AGENT_MANIFEST_WAVE13.json")
OUT = Path("scans/PHOENIX_420_AGENT_MANIFEST_VERIFY_WAVE13.json")


def main():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    agents = m["agents"]["count"]
    subs = m["subagents"]["per_agent"]
    assert agents == 420
    assert subs == 420
    assert agents * subs == 176400
    assert agents * (agents - 1) == 175980
    assert m["topology"]["self_edges"] is False
    assert m["subagents"]["manifest_mode"] == "deterministic_lazy"
    digest = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    result = {
        "schema": "phoenix-agent-manifest-verification/v1",
        "status": "VERIFIED",
        "manifest": str(MANIFEST),
        "agent_count": agents,
        "subagents_per_agent": subs,
        "total_addressable_subagents": agents * subs,
        "directed_agent_edges": agents * (agents - 1),
        "self_edge_check": "PASS",
        "count_check": "PASS",
        "deterministic_manifest_sha256": digest,
        "physical_runtime_claim": False,
        "literal_googleplex_execution": False,
        "live_infinite_web_claim": False
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
