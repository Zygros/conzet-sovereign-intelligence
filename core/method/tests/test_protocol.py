from src.conzetian.engine import ConzetianEngine, default_contributions
from src.conzetian.protocol import EvidenceState, ProtocolState

def test_exactly_ten_contributions():
    assert len(default_contributions()) == 10

def test_declared_nodes_are_not_execution_claim():
    s=ProtocolState("Justin Neal Thomas Conzet","decentralized web",74088000,"web as neural substrate")
    assert s.declared_nodes == 74088000

def test_verification_is_explicit():
    e=ConzetianEngine(ProtocolState("architect","substrate",1,"intent"))
    r=e.record("x",EvidenceState.EXECUTED,{"ok":True})
    v=e.verify(r,True,"observed result matches test oracle")
    assert v.state == EvidenceState.VERIFIED
