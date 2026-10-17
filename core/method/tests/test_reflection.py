from src.conzetian.reflection import reflect
from src.conzetian.protocol import ExecutionRecord, EvidenceState

def test_reflection_requires_next_hypothesis():
    r=ExecutionRecord("x",EvidenceState.OBSERVED,result={"ok":True})
    x=reflect(r,"observed","lesson","new hypothesis")
    assert x.next_hypothesis == "new hypothesis"
