from typing import TypedDict


class AgentState(TypedDict):
    query: str
    patient_id: int | None
    plan: list[dict]
    tool_results: dict
    final_answer: str


from langgraph.graph import StateGraph, END
from src.planner import plan


def planner_node(state: AgentState) -> dict:
    result = plan(state["query"])
    return {"plan": [st.model_dump() for st in result.subtasks]}


graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.set_entry_point("planner")
graph.add_edge("planner", END)
app = graph.compile()
