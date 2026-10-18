from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

class EvidenceState(str, Enum):
    DECLARED="DECLARED"; DESIGNED="DESIGNED"; EXECUTED="EXECUTED"; OBSERVED="OBSERVED"; VERIFIED="VERIFIED"; ANCHORED="ANCHORED"

@dataclass(frozen=True)
class ProtocolState:
    architect: str
    substrate: str
    declared_nodes: int
    intent: str

@dataclass(frozen=True)
class Contribution:
    id: int
    name: str
    objective: str
    evidence_required: tuple[str, ...]

@dataclass
class ExecutionRecord:
    action: str
    state: EvidenceState
    result: Any = None
    hypothesis: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self):
        return {"action":self.action,"state":self.state.value,"result":self.result,"hypothesis":self.hypothesis,"timestamp":self.timestamp}
