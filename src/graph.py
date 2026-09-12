from typing import TypedDict


class AgentState(TypedDict):
    query: str
    patient_id: int | None
    plan: list[dict]
    tool_results: dict
    final_answer: str
