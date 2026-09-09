from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
a = model.encode("The patient has chronic kidney disease")
b = model.encode("CKD treatment options")
c = model.encode("The weather is sunny today")

def cosine(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

print("kidney vs treatment:", cosine(a, b))
print("kidney vs weather:", cosine(a, c))

import faiss

texts = ["patient has CKD", "patient booked cardiology", "weather is sunny"]
vectors = model.encode(texts)
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

query_vec = model.encode(["kidney treatment"])
distances, indices = index.search(np.array(query_vec), k=2)
print("Top 2 matches:", [texts[i] for i in indices[0]])
