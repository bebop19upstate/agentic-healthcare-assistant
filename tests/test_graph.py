import json
import pytest
from src.graph import app, AgentState
from src.tools.appointment_tool import DOCTORS_FILE

ORIGINAL_DOCTORS = [
    {"doctor_id": 1, "name": "Dr. Rao", "specialty": "nephrology",
     "available_slots": ["2026-09-10 10:00", "2026-09-10 14:00", "2026-09-12 09:00"]},
    {"doctor_id": 2, "name": "Dr. Chen", "specialty": "cardiology",
     "available_slots": ["2026-09-11 09:00", "2026-09-11 15:00"]},
    {"doctor_id": 3, "name": "Dr. Patel", "specialty": "dermatology",
     "available_slots": ["2026-09-13 11:00"]},
]


@pytest.fixture(autouse=True)
def reset_doctors_file():
    with open(DOCTORS_FILE, "w") as f:
        json.dump(ORIGINAL_DOCTORS, f, indent=2)
    yield
    with open(DOCTORS_FILE, "w") as f:
        json.dump(ORIGINAL_DOCTORS, f, indent=2)


def make_initial_state(query: str, patient_id: int = 1) -> AgentState:
    return {
        "query": query,
        "patient_id": patient_id,
        "plan": [],
        "tool_results": {},
        "final_answer": "",
    }


def test_state_schema_initializes_correctly():
    state = make_initial_state("test query")
    assert state["query"] == "test query"
    assert state["tool_results"] == {}


def test_planner_node_updates_state():
    state = make_initial_state("Book me a cardiologist")
    result = app.invoke(state)
    assert len(result["plan"]) >= 1


def test_full_graph_sample_scenario_end_to_end():
    query = (
        "My 70-year-old father has chronic kidney disease. "
        "I want to book a nephrologist for him. "
        "Also, can you summarize latest treatment methods?"
    )
    state = make_initial_state(query)
    result = app.invoke(state)

    assert "ehr" in result["tool_results"]
    assert "appointment" in result["tool_results"]
    assert "disease_search" in result["tool_results"]
    assert len(result["final_answer"]) > 0
