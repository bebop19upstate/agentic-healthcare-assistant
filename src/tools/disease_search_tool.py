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


import os as _os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

_llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

DISEASE_ANSWER_PROMPT = """Answer the question using ONLY the excerpts below. Do not use any outside knowledge, even if you know more about the topic. If the excerpts don't contain enough information to answer, say so explicitly rather than guessing.

Excerpts:
{excerpts}

Question: {question}

Answer:"""


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return str(content)


def answer_from_chunks(question: str, chunks: list[str]) -> str:
    excerpts = "\n\n".join(f"- {c}" for c in chunks)
    prompt = DISEASE_ANSWER_PROMPT.format(excerpts=excerpts, question=question)
    response = _llm.invoke(prompt)
    return _extract_text(response.content)


def search_disease_info(query: str, k: int = 2) -> str:
    chunks = retrieve_chunks(query, k=k)
    if not chunks:
        return "No relevant information found in the medical reference corpus."
    return answer_from_chunks(query, chunks)
