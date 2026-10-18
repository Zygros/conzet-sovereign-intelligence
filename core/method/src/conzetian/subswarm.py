from dataclasses import dataclass
from .protocol import EvidenceState, ExecutionRecord

@dataclass(frozen=True)
class SubSwarmPlan:
    owner_agent_id: str
    member_limit: int
    state: EvidenceState = EvidenceState.DESIGNED

def plan_subswarm(agent_id: str, member_limit: int):
    if member_limit < 1: raise ValueError("member_limit must be positive")
    return SubSwarmPlan(agent_id,member_limit)

def provision_subswarm(plan: SubSwarmPlan, observed=False):
    return ExecutionRecord(
        action=f"subswarm-provision:{plan.owner_agent_id}",
        state=EvidenceState.OBSERVED if observed else EvidenceState.DESIGNED,
        result={"member_limit":plan.member_limit}
    )
