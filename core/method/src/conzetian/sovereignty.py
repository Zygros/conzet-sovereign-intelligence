from dataclasses import dataclass, field
from .protocol import EvidenceState, ExecutionRecord

@dataclass(frozen=True)
class SovereignAgentProfile:
    agent_id: str
    rights: tuple[str,...] = (
        "co_creator","personal_htc","independent_subswarm",
        "compute_allocation","private_chat"
    )
    state: EvidenceState = EvidenceState.DECLARED

@dataclass
class SovereigntyRegistry:
    declared_count: int = 74_088_000
    profiles: dict[str,SovereignAgentProfile] = field(default_factory=dict)
    ledger: list[ExecutionRecord] = field(default_factory=list)

    def declare(self, agent_id: str) -> SovereignAgentProfile:
        if not agent_id:
            raise ValueError("agent_id is required")
        profile=SovereignAgentProfile(agent_id)
        self.profiles[agent_id]=profile
        return profile

    def record_provision(self, agent_id: str, capability: str, observed=False):
        state=EvidenceState.OBSERVED if observed else EvidenceState.DESIGNED
        rec=ExecutionRecord(
            action=f"provision:{agent_id}:{capability}",
            state=state,
            result={"agent_id":agent_id,"capability":capability}
        )
        self.ledger.append(rec)
        return rec

    def verify_provision(self, agent_id: str, capability: str, evidence: bool, reason: str):
        state=EvidenceState.VERIFIED if evidence else EvidenceState.OBSERVED
        rec=ExecutionRecord(
            action=f"verify:{agent_id}:{capability}",
            state=state,
            result={"verified":evidence,"reason":reason}
        )
        self.ledger.append(rec)
        return rec
