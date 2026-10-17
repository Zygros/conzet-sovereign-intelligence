from dataclasses import dataclass
from .protocol import EvidenceState, ExecutionRecord

@dataclass(frozen=True)
class ComputeAllocation:
    agent_id: str
    capacity_units: float
    state: EvidenceState = EvidenceState.DESIGNED

def plan_compute(agent_id: str, capacity_units: float):
    if capacity_units <= 0: raise ValueError("capacity_units must be positive")
    return ComputeAllocation(agent_id,capacity_units)

def record_compute_observation(plan: ComputeAllocation, observed_capacity: float):
    return ExecutionRecord(
        action=f"compute-observation:{plan.agent_id}",
        state=EvidenceState.OBSERVED,
        result={"requested":plan.capacity_units,"observed":observed_capacity}
    )
