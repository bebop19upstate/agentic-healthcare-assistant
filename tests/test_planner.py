from src.planner import plan

def test_plan_returns_list_of_subtasks():
    result = plan("Book me a cardiologist appointment")
    assert len(result.subtasks) >= 1

def test_plan_booking_only_query_includes_appointment_tool():
    result = plan("I need to book an appointment with a dermatologist")
    tools_used = {st.tool for st in result.subtasks}
    assert "appointment" in tools_used

def test_plan_combined_scenario_includes_all_tools():
    query = (
        "My 70-year-old father has chronic kidney disease. "
        "I want to book a nephrologist for him. "
        "Also, can you summarize latest treatment methods?"
    )
    result = plan(query)
    tools_used = {st.tool for st in result.subtasks}
    assert "appointment" in tools_used
    assert "disease_search" in tools_used
