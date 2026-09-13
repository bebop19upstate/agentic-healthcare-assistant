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
        "retrieved_memory": "",
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

def test_graph_booking_only_scenario():
    state = make_initial_state("Book me a cardiologist appointment next week")
    result = app.invoke(state)
    assert "appointment" in result["tool_results"]
    assert "ehr" not in result["tool_results"]
    assert "disease_search" not in result["tool_results"]


def test_graph_ehr_only_scenario():
    from src.tools.ehr_tool import add_patient_record, get_patient_history
    add_patient_record(1, "John Doe Sr.", 70, "CKD stage 3")  # reset before test

    state = make_initial_state("Add a note to my father record: started a new blood pressure medication")
    result = app.invoke(state)

    assert "ehr" in result["tool_results"]
    assert "appointment" not in result["tool_results"]
    updated = get_patient_history(1)
    assert "blood pressure" in updated["history_text"].lower()


def test_graph_disease_info_only_scenario():
    state = make_initial_state("What's the latest on kidney disease treatment?")
    result = app.invoke(state)
    assert "disease_search" in result["tool_results"]
    assert "appointment" not in result["tool_results"]
    assert "ehr" not in result["tool_results"]


def test_graph_unknown_patient_handled_gracefully():
    state = make_initial_state("Book me a nephrologist", patient_id=999)
    result = app.invoke(state)
    assert result["tool_results"] == {}
    assert "couldn't find" in result["final_answer"].lower()


def test_graph_ambiguous_query_handled():
    state = make_initial_state("I need help")
    result = app.invoke(state)
    assert result["plan"] == []
    assert result["final_answer"] == "Could you tell me more about what you need?"