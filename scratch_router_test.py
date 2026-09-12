from typing import TypedDict
from langgraph.graph import StateGraph, END


class FakeState(TypedDict):
    query: str
    branch_taken: str


def fake_router(state: FakeState) -> str:
    if "book" in state["query"].lower():
        return "branch_a"
    return "branch_b"


def branch_a_node(state: FakeState) -> dict:
    return {"branch_taken": "A (booking-related)"}


def branch_b_node(state: FakeState) -> dict:
    return {"branch_taken": "B (not booking-related)"}


graph = StateGraph(FakeState)
graph.add_node("branch_a", branch_a_node)
graph.add_node("branch_b", branch_b_node)
graph.set_conditional_entry_point(fake_router, {"branch_a": "branch_a", "branch_b": "branch_b"})
graph.add_edge("branch_a", END)
graph.add_edge("branch_b", END)
app = graph.compile()

print(app.invoke({"query": "I want to book an appointment", "branch_taken": ""}))
print(app.invoke({"query": "What's the weather like?", "branch_taken": ""}))
