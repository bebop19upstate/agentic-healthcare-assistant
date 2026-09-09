import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")
_EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 always produces 384-number vectors


class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(_EMBEDDING_DIM)
        self.texts: list[str] = []

    def add_summary(self, patient_id: int, text: str) -> None:
        vector = _model.encode([text])
        self.index.add(np.array(vector))
        self.texts.append(text)

    def retrieve_similar(self, query: str, k: int = 3) -> list[str]:
        if len(self.texts) == 0:
            return []
        k = min(k, len(self.texts))  # don't ask for more results than we have
        query_vector = _model.encode([query])
        distances, indices = self.index.search(np.array(query_vector), k)
        return [self.texts[i] for i in indices[0]]
