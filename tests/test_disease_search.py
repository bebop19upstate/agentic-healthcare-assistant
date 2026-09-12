from src.tools.disease_search_tool import chunk_text, retrieve_chunks, search_disease_info


def test_chunking_splits_text_into_pieces():
    text = " ".join(["word"] * 250)
    chunks = chunk_text(text, max_words=100)
    assert len(chunks) == 3
    assert len(chunks[0].split()) == 100
    assert len(chunks[2].split()) == 50


def test_retrieve_relevant_chunks_for_known_topic():
    results = retrieve_chunks("kidney disease symptoms and causes", k=1)
    assert len(results) == 1
    assert "kidney" in results[0].lower()


def test_disease_search_tool_returns_grounded_answer():
    answer = search_disease_info("What medication is used first for type 2 diabetes?")
    assert "metformin" in answer.lower()
