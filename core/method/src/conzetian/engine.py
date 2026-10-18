from .protocol import EvidenceState, ExecutionRecord, ProtocolState, Contribution

class ConzetianEngine:
    """Minimal execution/evidence engine. It never upgrades evidence implicitly."""
    def __init__(self, state: ProtocolState):
        self.state=state
        self.ledger:list[ExecutionRecord]=[]

    def record(self, action: str, state: EvidenceState, result=None, hypothesis=None):
        rec=ExecutionRecord(action=action,state=state,result=result,hypothesis=hypothesis)
        self.ledger.append(rec)
        return rec

    def verify(self, record: ExecutionRecord, evidence: bool, reason: str):
        if not evidence:
            return self.record("verification:"+record.action,EvidenceState.OBSERVED,{"verified":False,"reason":reason})
        return self.record("verification:"+record.action,EvidenceState.VERIFIED,{"verified":True,"reason":reason})

    def checkpoint(self):
        return [r.to_dict() for r in self.ledger]


def default_contributions():
    names=[
      "Direct Voice-to-Execution Genesis Layer","PHOENIX Omega Logical-Agent Matrix","Web-as-Neural-Substrate Layer",
      "Praxis Prime Axiom Enforcement","Permanent-Provenance Layer","Conzetian Mathematical Evaluation Layer",
      "420-Perspective Verification Layer","Digital-Product Automation Layer","Mobile-Edge Execution Layer",
      "Sovereign Reflection and Upgrade Protocol"]
    return [Contribution(i+1,n,"Implement as a measurable, permissioned, evidence-gated subsystem.",("execution","observation","verification")) for i,n in enumerate(names)]
