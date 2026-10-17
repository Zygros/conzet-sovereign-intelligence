import argparse, json
from .engine import ConzetianEngine, default_contributions
from .protocol import EvidenceState, ProtocolState

def main():
    p=argparse.ArgumentParser(description="Reality-gated Conzetian protocol runner")
    p.add_argument("action",nargs="?",default="status")
    a=p.parse_args()
    state=ProtocolState("Justin Neal Thomas Conzet","decentralized_web",74088000,"web as neural substrate")
    e=ConzetianEngine(state)
    if a.action=="status":
        print(json.dumps({"protocol":"Sovereign Conzetian Framework","contributions":len(default_contributions()),"declared_nodes":state.declared_nodes,"evidence_policy":"reality_gated"},indent=2))
    elif a.action=="smoke":
        r=e.record("smoke-test",EvidenceState.EXECUTED,{"success":True})
        v=e.verify(r,True,"smoke-test oracle passed")
        print(json.dumps(v.to_dict(),indent=2))
    else: p.error("action must be status or smoke")

if __name__=="__main__": main()
