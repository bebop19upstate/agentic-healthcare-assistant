from src.memory.vector_store import VectorStore
from src.memory.memory_manager import add_memory, get_context


def test_add_summary_and_retrieve_similar():
    store = VectorStore()
    store.add_summary(1, "Patient has chronic kidney disease")
    store.add_summary(1, "Patient enjoys reading books")
    results = store.retrieve_similar("kidney treatment", k=1)
    assert "kidney" in results[0].lower()


def test_retrieve_similar_returns_k_results():
    store = VectorStore()
    store.add_summary(1, "Summary one about diabetes")
    store.add_summary(1, "Summary two about kidneys")
    store.add_summary(1, "Summary three about allergies")
    results = store.retrieve_similar("medical history", k=3)
    assert len(results) == 3


def test_memory_manager_fetches_context_for_patient():
    add_memory(101, "Patient has chronic kidney disease, stage 3")
    add_memory(102, "Patient has type 2 diabetes")

    context_101 = get_context(101, "kidney treatment")
    context_102 = get_context(102, "kidney treatment")

    assert "kidney" in context_101.lower()
    assert "kidney" not in context_102.lower()
