from src.memory.vector_store import VectorStore

_patient_stores: dict[int, VectorStore] = {}


def _get_store(patient_id: int) -> VectorStore:
    if patient_id not in _patient_stores:
        _patient_stores[patient_id] = VectorStore()
    return _patient_stores[patient_id]


def add_memory(patient_id: int, text: str) -> None:
    store = _get_store(patient_id)
    store.add_summary(patient_id, text)


def get_context(patient_id: int, query: str, k: int = 3) -> str:
    store = _get_store(patient_id)
    results = store.retrieve_similar(query, k=k)
    if not results:
        return ""
    return " ".join(results)
