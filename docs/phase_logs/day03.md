# Day 3 — Vector Store & Memory Modules

## What I did
- Installed sentence-transformers, verified embedding similarity intuition
  by hand (cosine similarity: related sentences ~0.43, unrelated ~0.004)
- Built a minimal FAISS index by hand before wrapping it in a class
- Wrote VectorStore class (src/memory/vector_store.py) wrapping FAISS + a
  parallel text list for translating index results back to readable text
- Wrote memory_manager.py with per-patient isolated VectorStore instances,
  so one patient's memory never leaks into another's query results
- Connected real seeded EHR data (Phase 2) into memory via generated summaries
- Wrote tests/test_memory.py, 3/3 passing

## What I learned
- Cosine similarity: higher = more related (range ~-1 to 1). FAISS's
  IndexFlatL2 measures distance instead: lower = more similar — opposite
  direction, easy to get confused if not careful
- FAISS only stores vectors, not the original text — need a parallel
  list/dict to map results back to something readable
- Per-patient memory isolation requires either separate VectorStore instances
  per patient, or storing patient_id alongside each vector and filtering —
  chose separate instances for simplicity at this scale
- Each `python -c` invocation is a fresh process — in-memory state (like
  patient stores) doesn't persist between separate script runs, only within
  one script/session

## Status
Phase 3 complete: src/memory/vector_store.py, src/memory/memory_manager.py,
tests/test_memory.py all working, 3/3 tests passing.
Next: Phase 4 (RAG-based disease search tool).
