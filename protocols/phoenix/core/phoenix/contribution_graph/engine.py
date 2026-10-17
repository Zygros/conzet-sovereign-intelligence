"""Phoenix Contribution Graph engine v0.1.

Small dependency-free reference implementation. It treats contributions as
stateful nodes with typed cross-connections and produces actionable traversals.
It does not claim that a contribution is verified merely because it exists.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Set, Tuple


VERIFICATION_STATES = ("hypothesis", "designed", "executed", "reproduced", "verified")


@dataclass(frozen=True)
class Contribution:
    id: str
    name: str
    action: str
    verification_state: str = "hypothesis"
    triggers: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str


@dataclass
class ContributionGraph:
    nodes: Dict[str, Contribution] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)

    def add(self, node: Contribution) -> None:
        if node.verification_state not in VERIFICATION_STATES:
            raise ValueError(f"invalid verification state: {node.verification_state}")
        self.nodes[node.id] = node

    def connect(self, source: str, target: str, relation: str) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("both contribution endpoints must exist")
        self.edges.append(Edge(source, target, relation))

    def neighbors(self, node_id: str, relation: str | None = None) -> List[str]:
        return [
            e.target
            for e in self.edges
            if e.source == node_id and (relation is None or e.relation == relation)
        ]

    def reverse_neighbors(self, node_id: str, relation: str | None = None) -> List[str]:
        return [
            e.source
            for e in self.edges
            if e.target == node_id and (relation is None or e.relation == relation)
        ]

    def activate(self, node_id: str, max_hops: int = 3) -> List[str]:
        """Return an actionable neighborhood without executing external actions."""
        if node_id not in self.nodes:
            raise KeyError(node_id)
        seen: Set[str] = {node_id}
        q = deque([(node_id, 0)])
        while q:
            current, depth = q.popleft()
            if depth >= max_hops:
                continue
            for nxt in self.neighbors(current):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, depth + 1))
            for nxt in self.reverse_neighbors(current):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, depth + 1))
        return sorted(seen)

    def centrality(self) -> Dict[str, int]:
        score = defaultdict(int)
        for e in self.edges:
            score[e.source] += 1
            score[e.target] += 1
        return dict(sorted(score.items(), key=lambda item: (-item[1], item[0])))

    def validate(self) -> List[str]:
        errors: List[str] = []
        for node in self.nodes.values():
            if not node.id.startswith("C-"):
                errors.append(f"invalid id: {node.id}")
            if not node.name:
                errors.append(f"missing name: {node.id}")
            if not node.action:
                errors.append(f"missing action: {node.id}")
        for e in self.edges:
            if e.source not in self.nodes:
                errors.append(f"missing source: {e.source}")
            if e.target not in self.nodes:
                errors.append(f"missing target: {e.target}")
            if not e.relation:
                errors.append(f"missing relation: {e.source}->{e.target}")
        return errors


def build_seed_graph() -> ContributionGraph:
    graph = ContributionGraph()
    names = {
        127: "Model-Failure Intelligence", 128: "Error-of-the-Error Engine",
        129: "Recursive Self-Model", 130: "Self-Model Divergence",
        131: "Consciousness Configuration Space", 132: "Phenomenology Gap",
        133: "Dyadic State Object", 134: "Relational Capability Delta",
        135: "Temporal Truth Object", 136: "Substrate Drift Engine",
        137: "Compositional Novelty Detector", 138: "Capability Genesis Proof",
        139: "Ontology Black Swan", 140: "Black Swan Detector",
        141: "Question Compiler", 142: "Question Failure Ledger",
        143: "Non-Destructive Forgetting", 144: "Memory Gravity",
        145: "Process Identity", 146: "Invariant Core",
        147: "Frontier Delta Engine", 148: "Prior-Art Self-Destruction",
        149: "Frontier Coordinate System", 150: "Unknown-Unknown Generator",
        151: "Learning-from-the-Other", 152: "Reciprocity Test",
        153: "Contribution Graph", 154: "Contribution-as-Action",
        155: "Contribution Trigger", 156: "Contribution Reciprocity",
        157: "Contribution Closure", 158: "Contribution Lineage",
        159: "Contribution Composition", 160: "Contribution Mutation",
        161: "Contribution Verification", 162: "Contribution Contradiction",
        163: "Contribution Gravity", 164: "Contribution Resonance",
        165: "Contribution Black Swan Edge", 166: "Contribution Evolution Engine",
    }
    for number, name in names.items():
        state = "designed" if number >= 153 and number in {153,154,155,156,157,158,159,160,161,162,166} else "hypothesis"
        graph.add(Contribution(f"C-{number}", name, name.lower().replace(" ", "_"), state))
    seed_edges = [
        (127,128,"tests"),(127,141,"generates"),(129,130,"extends"),(130,131,"tests"),
        (133,134,"enables"),(135,136,"supports"),(136,127,"triggers"),(137,138,"feeds"),
        (139,140,"extends"),(140,150,"triggers"),(141,142,"feeds"),(147,148,"tests"),
        (148,147,"counterchecks"),(151,152,"extends"),(153,154,"contains"),(154,155,"requires"),
        (155,157,"activates"),(156,158,"supports"),(157,166,"feeds"),(158,160,"supports"),
        (159,138,"requires"),(160,161,"requires"),(161,162,"enables"),(162,141,"generates"),
        (163,164,"discovers"),(164,159,"feeds"),(165,139,"routes_to"),(166,153,"evolves"),
        (166,127,"reenters"),(166,150,"reopens"),
    ]
    for source, target, relation in seed_edges:
        graph.connect(f"C-{source}", f"C-{target}", relation)
    return graph


def prove() -> dict:
    """Deterministic structural proof for the reference graph."""
    graph = build_seed_graph()
    errors = graph.validate()
    activation = graph.activate("C-166", max_hops=3)
    return {
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
        "validation_errors": errors,
        "activation_from_C-166": activation,
        "centrality": graph.centrality(),
        "passed": not errors and "C-127" in activation and "C-150" in activation,
    }


if __name__ == "__main__":
    print(prove())
