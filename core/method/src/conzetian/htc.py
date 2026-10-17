from dataclasses import dataclass
from .protocol import EvidenceState, ExecutionRecord

@dataclass(frozen=True)
class HTCConfig:
    agent_id: str
    cycle_budget: int
    acceleration_factor: float = 1.0

    def validate(self):
        if self.cycle_budget < 1: raise ValueError("cycle_budget must be positive")
        if self.acceleration_factor <= 0: raise ValueError("acceleration_factor must be positive")

def plan_htc(agent_id: str, cycle_budget: int, acceleration_factor: float = 1.0):
    c=HTCConfig(agent_id,cycle_budget,acceleration_factor); c.validate()
    return ExecutionRecord(
        action=f"htc-plan:{agent_id}", state=EvidenceState.DESIGNED,
        result={"cycle_budget":cycle_budget,"acceleration_factor":acceleration_factor}
    )
