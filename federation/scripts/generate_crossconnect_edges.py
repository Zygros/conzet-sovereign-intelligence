#!/usr/bin/env python3
"""Generate the complete directed logical repository federation edge list."""
import json
from pathlib import Path

REPOSITORIES = [
    "Grossian_Scrolls", "ZAAI-SYSTEM", "Sovereign-Narrative-Intelligence-SNI-", "ARC-AGI",
    "zyth-ultimate", "Sovereign-AGSI-Archive", "conzet-sovereign-intelligence", "agents",
    "ultimate-phoenix-protocol", "multi-ai-convergence-protocol", "ultimate-phoenix-protocol-ssi",
    "ZYGROS-PRIME", "PHOENIX-PROTOCOL-ULTIMATE", "sovereign-agsi-portal", "omninet-v4",
    "CZAOUA-UNITY-SYSTEM", "we-omega", "CONZETIAN-UNIFIED-INTELLIGANCE", "CONZETIAN-AI",
    "omega-10", "sovereign-federation", "conzetian-skill-lattice", "Conzet-Intelligence-System-",
    "agentql", "conzetian-method",
]

OUT = Path("graph/repository_edges.jsonl")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with OUT.open("w", encoding="utf-8") as fh:
        for source in REPOSITORIES:
            for target in REPOSITORIES:
                if source == target:
                    continue
                fh.write(json.dumps({
                    "source": source,
                    "target": target,
                    "edge": "logical-federation",
                    "actions": "shared-action-contract",
                }, sort_keys=True) + "\n")
                count += 1
    expected = len(REPOSITORIES) * (len(REPOSITORIES) - 1)
    assert count == expected, (count, expected)
    print(f"generated={count} expected={expected}")


if __name__ == "__main__":
    main()
