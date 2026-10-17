from dataclasses import dataclass
from .protocol import EvidenceState, ExecutionRecord

@dataclass(frozen=True)
class PrivateChatNode:
    agent_id: str
    endpoint: str
    state: EvidenceState = EvidenceState.DESIGNED

def plan_private_chat(agent_id: str, endpoint: str):
    if not endpoint: raise ValueError("endpoint is required")
    return PrivateChatNode(agent_id,endpoint)

def record_chat_execution(node: PrivateChatNode, message_count: int):
    if message_count < 0: raise ValueError("message_count cannot be negative")
    return ExecutionRecord(
        action=f"chat-execution:{node.agent_id}",
        state=EvidenceState.OBSERVED,
        result={"message_count":message_count,"endpoint":node.endpoint}
    )
