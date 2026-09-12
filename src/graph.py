from typing import TypedDict

from langgraph.graph import StateGraph, END

from src.planner import plan
from src.tools.ehr_tool import get_patient_history
from src.tools.appointment_tool import find_slots, book_slot, book_first_available
from src.tools.disease_search_tool import search_disease_info
from src.memory.memory_manager import get_context
from src.prompts.templates import COMPOSER_PROMPT
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
_composer_llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return str(content)


class AgentState(TypedDict):
    query: str
    patient_id: int | None
    plan: list[dict]
    tool_results: dict
    final_answer: str


def planner_node(state: AgentState) -> dict:
    result = plan(state["query"])
    return {"plan": [st.model_dump() for st in result.subtasks]}

def _get_subtask_query(state: AgentState, tool_name: str) -> str:
    for subtask in state["plan"]:
        if subtask["tool"] == tool_name:
            return subtask["subtask"]
    return state["query"]  # fallback if the planner didn't produce this tool

def _tool_in_plan(state: AgentState, tool_name: str) -> bool:
    return any(subtask["tool"] == tool_name for subtask in state["plan"])

def ehr_node(state: AgentState) -> dict:
    if not _tool_in_plan(state, "ehr"):
        return {}
    patient = get_patient_history(state["patient_id"])
    focused_query = _get_subtask_query(state, "ehr")
    memory_context = get_context(state["patient_id"], focused_query)
    summary = patient["history_text"] if patient else "No record found."
    if memory_context:
        summary = f"{summary} (Related context: {memory_context})"
    return {"tool_results": {**state["tool_results"], "ehr": summary}}

def appointment_node(state: AgentState) -> dict:
    if not _tool_in_plan(state, "appointment"):
        return {}
    focused_query = _get_subtask_query(state, "appointment").lower()
    specialty_roots = {"nephrolog": "nephrology", "cardiolog": "cardiology", "dermatolog": "dermatology"}
    specialty = next((full for root, full in specialty_roots.items() if root in focused_query), "nephrology")    
    result = book_first_available(specialty)
    return {"tool_results": {**state["tool_results"], "appointment": result}}


def disease_search_node(state: AgentState) -> dict:
    if not _tool_in_plan(state, "disease_search"):
        return {}
    focused_query = _get_subtask_query(state, "disease_search")
    result = search_disease_info(focused_query)
    return {"tool_results": {**state["tool_results"], "disease_search": result}}


def composer_node(state: AgentState) -> dict:
    lines = []
    for tool_name, result in state["tool_results"].items():
        lines.append(f"{tool_name}: {result}")
    results_text = "\n\n".join(lines)
    prompt = COMPOSER_PROMPT.format(results=results_text)
    response = _composer_llm.invoke(prompt)
    return {"final_answer": _extract_text(response.content)}


graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("ehr", ehr_node)
graph.add_node("appointment", appointment_node)
graph.add_node("disease_search", disease_search_node)
graph.add_node("composer", composer_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "ehr")
graph.add_edge("ehr", "appointment")
graph.add_edge("appointment", "disease_search")
graph.add_edge("disease_search", "composer")
graph.add_edge("composer", END)
app = graph.compile()
