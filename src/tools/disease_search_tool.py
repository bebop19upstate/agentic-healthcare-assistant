def chunk_text(text: str, max_words: int = 100) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

import os
from src.memory.vector_store import VectorStore

CORPUS_DIR = "data/disease_corpus"

_disease_store = VectorStore()
_loaded = False


def _load_corpus() -> None:
    global _loaded
    if _loaded:
        return
    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(CORPUS_DIR, filename)
            with open(filepath) as f:
                text = f.read()
            for chunk in chunk_text(text):
                _disease_store.add_summary(patient_id=0, text=chunk)  # patient_id unused here, 0 as a placeholder
    _loaded = True


def retrieve_chunks(query: str, k: int = 3) -> list[str]:
    _load_corpus()
    return _disease_store.retrieve_similar(query, k=k)
