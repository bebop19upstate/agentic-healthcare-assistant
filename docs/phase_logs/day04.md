# Day 4 — Disease Search / RAG Tool

## What I did
- Built a 5-file offline corpus (CKD, diabetes, pediatric wellness) covering
  all seeded patients' conditions
- Wrote chunk_text() and verified it correctly splits at word-count boundaries
- Built a second, separate FAISS index (via VectorStore) specifically for
  disease chunks, isolated from patient memory
- Wrote retrieve_chunks() and verified retrieval generalizes correctly across
  all 3 topics (CKD, diabetes, pediatric), not just the one I tested first
- Wrote answer_from_chunks() with a strict "use ONLY these excerpts" prompt,
  verified answers are genuinely grounded by tracing each claim back to source
- Wired everything into one entry point: search_disease_info()
- Wrote tests/test_disease_search.py, 3/3 passing

## What I learned
- RAG correctly synthesizes across MULTIPLE retrieved chunks, not just one —
  saw this directly when a CKD answer correctly pulled "dialysis/transplant"
  from ckd_overview.txt while the rest came from ckd_treatment.txt
- Simple word-count chunking can orphan sentence fragments at chunk
  boundaries (lost context) — production systems use overlapping chunks to
  avoid this; acceptable simplification at this project's scale
- Reused VectorStore from Phase 3 for a completely different purpose (disease
  chunks vs. patient memory) by creating a separate instance — same class,
  no data mixing, though the patient_id parameter is an awkward fit here
- Grounding a RAG answer means checking every claim traces back to the
  actual source text, not just that the answer sounds plausible

## Status
Phase 4 complete: src/tools/disease_search_tool.py, tests/test_disease_search.py
all working, 3/3 tests passing.
Next: Phase 5 (prompt engineering & task chaining).
