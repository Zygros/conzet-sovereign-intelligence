from dataclasses import dataclass
from .protocol import ExecutionRecord

@dataclass(frozen=True)
class Reflection:
    observation: str
    lesson: str
    next_hypothesis: str

def reflect(record: ExecutionRecord, observation: str, lesson: str, next_hypothesis: str):
    if not observation or not lesson or not next_hypothesis:
        raise ValueError("reflection requires observation, lesson, and next_hypothesis")
    return Reflection(observation,lesson,next_hypothesis)
