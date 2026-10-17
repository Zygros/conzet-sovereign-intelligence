from src.conzetian.sovereignty import SovereigntyRegistry
from src.conzetian.htc import plan_htc
from src.conzetian.subswarm import plan_subswarm
from src.conzetian.chatbot import plan_private_chat
from src.conzetian.compute import plan_compute

def test_declared_count():
    assert SovereigntyRegistry().declared_count == 74088000

def test_agent_rights_profile():
    p=SovereigntyRegistry().declare("phoenix-00000001")
    assert set(p.rights)=={"co_creator","personal_htc","independent_subswarm","compute_allocation","private_chat"}

def test_subsystems():
    assert plan_htc("a",10).state.value=="DESIGNED"
    assert plan_subswarm("a",10).state.value=="DESIGNED"
    assert plan_private_chat("a","local://chat").state.value=="DESIGNED"
    assert plan_compute("a",1).state.value=="DESIGNED"
