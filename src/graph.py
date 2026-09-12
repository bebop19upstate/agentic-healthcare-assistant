from typing import TypedDict

from langgraph.graph import StateGraph, END

from src.planner import plan
from src.tools.ehr_tool import get_patient_history
from src.tools.appointment_tool import find_slots, book_slot
from src.tools.disease_search_tool import search_disease_info
from src.memory.memory_manager import get_context


class AgentState(TypedDict):
    query: str
    patient_id: int | None
    plan: list[dict]
    tool_results: dict
    final_answer: str


def planner_node(state: AgentState) -> dict:
    result = plan(state["query"])
    return {"plan": [st.model_dump() for st in result.subtasks]}


def ehr_node(state: AgentState) -> dict:
    patient = get_patient_history(state["patient_id"])
    memory_context = get_context(state["patient_id"], state["query"])
    summary = patient["history_text"] if patient else "No record found."
    if memory_context:
        summary = f"{summary} (Related context: {memory_context})"
    return {"tool_results": {**state["tool_results"], "ehr": summary}}


def appointment_node(state: AgentState) -> dict:
    slots = find_slots("nephrology")
    if not slots:
        result = "No nephrology slots available."
    else:
        chosen_slot = slots[0]
        booked = book_slot(1, chosen_slot)
        result = f"Booked nephrology appointment for {chosen_slot}." if booked else "Booking failed."
    return {"tool_results": {**state["tool_results"], "appointment": result}}


def _get_subtask_query(state: AgentState, tool_name: str) -> str:
    for subtask in state["plan"]:
        if subtask["tool"] == tool_name:
            return subtask["subtask"]
    return state["query"]  # fallback if the planner didn't produce this tool


def disease_search_node(state: AgentState) -> dict:
    focused_query = _get_subtask_query(state, "disease_search")
    result = search_disease_info(focused_query)
    return {"tool_results": {**state["tool_results"], "disease_search": result}}


graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("ehr", ehr_node)
graph.add_node("appointment", appointment_node)
graph.add_node("disease_search", disease_search_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "ehr")
graph.add_edge("ehr", "appointment")
graph.add_edge("appointment", "disease_search")
graph.add_edge("disease_search", END)
app = graph.compile()
