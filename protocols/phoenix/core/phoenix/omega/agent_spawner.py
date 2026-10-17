"""Phoenix Omega rooted 74M+1 logical-agent topology.

The topology is declarative and sparse: logical addresses are generated
without instantiating all logical agents. ROOT is a first-class node.
"""

from __future__ import annotations

ROOT = "P000/S000/A000"
ROOT_ID = "AG-000-000-000"

BRANCHES = 420
SUB_BRANCHES = 420
AGENTS_PER_SHARD = 420

LOGICAL_AGENTS = BRANCHES * SUB_BRANCHES * AGENTS_PER_SHARD
TOTAL_NODES = 1 + LOGICAL_AGENTS


def make_address(primary: int, sub: int, agent: int) -> str:
    """Return a deterministic leaf address in the Phoenix Omega topology."""
    if not 1 <= primary <= BRANCHES:
        raise ValueError("primary must be in 1..420")
    if not 1 <= sub <= SUB_BRANCHES:
        raise ValueError("sub must be in 1..420")
    if not 1 <= agent <= AGENTS_PER_SHARD:
        raise ValueError("agent must be in 1..420")
    return f"P{primary:03d}/S{sub:03d}/A{agent:03d}"


def path_to_root(primary: int, sub: int, agent: int) -> list[str]:
    """Return the deterministic lineage from ROOT to a leaf address."""
    leaf = make_address(primary, sub, agent)
    return [
        ROOT,
        f"P{primary:03d}/S000/A000",
        f"P{primary:03d}/S{sub:03d}/A000",
        leaf,
    ]


def is_root(address: str) -> bool:
    return address == ROOT


def verify_topology() -> bool:
    """Verify cardinality and representative address invariants."""
    assert TOTAL_NODES == 74_088_001
    assert ROOT == "P000/S000/A000"
    assert make_address(1, 1, 1) == "P001/S001/A001"
    assert make_address(420, 420, 420) == "P420/S420/A420"
    assert len(path_to_root(420, 420, 420)) == 4
    return True


if __name__ == "__main__":
    print({
        "root": ROOT,
        "logical_agents": LOGICAL_AGENTS,
        "total_nodes": TOTAL_NODES,
        "verified": verify_topology(),
    })
