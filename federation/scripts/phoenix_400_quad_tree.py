#!/usr/bin/env python3
"""Deterministic lazy materializer for the Phoenix 400^4 logic space.

400 agents × 400 logic trees × 400 sub-actions × 400 sub-logic trees
= 25,600,000,000 logical leaves.

The system deliberately does NOT write 25.6B records. It generates stable
identifiers and bounded shards so the complete space is addressable without
pretending that a physically materialized corpus exists.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from itertools import product
from typing import Iterator

N = 400
LEAVES = N ** 4

@dataclass(frozen=True)
class Node:
    agent: int
    logic_tree: int
    sub_action: int
    sub_logic_tree: int

    @property
    def id(self) -> str:
        return f"A{self.agent:03d}.L{self.logic_tree:03d}.S{self.sub_action:03d}.Q{self.sub_logic_tree:03d}"

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.id.encode()).hexdigest()


def node(agent: int, logic_tree: int, sub_action: int, sub_logic_tree: int) -> Node:
    vals = (agent, logic_tree, sub_action, sub_logic_tree)
    if any(not 1 <= x <= N for x in vals):
        raise ValueError("indices must be in 1..400")
    return Node(*vals)


def shard(agent: int, logic_tree: int, limit: int = 1000) -> Iterator[Node]:
    """Enumerate a bounded shard for one agent/tree pair."""
    if not 1 <= agent <= N or not 1 <= logic_tree <= N:
        raise ValueError("agent and logic_tree must be in 1..400")
    if limit < 1:
        return
    for sub_action, sub_logic_tree in product(range(1, N + 1), repeat=2):
        if (sub_action - 1) * N + sub_logic_tree > limit:
            break
        yield node(agent, logic_tree, sub_action, sub_logic_tree)


def manifest() -> dict:
    return {
        "schema": "phoenix-400-quad-tree/v1",
        "agents": N,
        "logic_trees_per_agent": N,
        "sub_actions_per_tree": N,
        "sub_logic_trees_per_sub_action": N,
        "logical_leaves": LEAVES,
        "materialization": "lazy",
        "addressing": "A###.L###.S###.Q###",
        "verification": "deterministic SHA-256 identifier per node",
        "safety": "no network execution, credentials, secrets, or external side effects",
    }


def prove() -> dict:
    samples = [
        node(1, 1, 1, 1),
        node(400, 400, 400, 400),
        node(217, 89, 303, 144),
    ]
    assert LEAVES == 25_600_000_000
    assert len({x.id for x in samples}) == len(samples)
    assert all(len(x.digest) == 64 for x in samples)
    return {"status": "VERIFIED", "logical_leaves": LEAVES, "samples": [asdict(x) | {"digest": x.digest} for x in samples]}


if __name__ == "__main__":
    print(json.dumps({"manifest": manifest(), "prove": prove()}, indent=2))
