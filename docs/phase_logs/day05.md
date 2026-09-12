# Day 5 — Prompt Engineering & Task Chaining

## What I did
- Consolidated all prompts into src/prompts/templates.py (PLANNER_PROMPT,
  DISEASE_ANSWER_PROMPT, EHR_SUMMARY_PROMPT, COMPOSER_PROMPT)
- Wrote and verified EHR_SUMMARY_PROMPT against the real CKD patient record
  — confirmed the summary added nothing beyond what's in the source data
- Wrote COMPOSER_PROMPT with an explicit "don't mention missing sections"
  instruction, verified it produces clean, focused replies for partial
  result sets (e.g. booking-only)
- Traced the full sample scenario request lifecycle in docs/architecture.md
  before writing any Phase 6 graph code
- Wrote tests/test_prompts.py — 4 fast tests (0.01s), no LLM calls needed
  since they only check template rendering, not model output

## What I learned
- Not every test needs to call a live LLM — template-rendering tests are
  fast, free, and still catch real bugs (missing placeholders, typos)
- A composer prompt needs explicit instructions for the *absence* of
  information, not just what to do with what's present — otherwise it can
  produce awkward non-sequiturs about missing sections nobody asked about
- Writing out the full request lifecycle on paper before coding the graph
  (Phase 6) gives a concrete checklist to verify against once the real
  graph is running, rather than debugging blind

## Status
Phase 5 complete: src/prompts/templates.py consolidated with 4 prompts,
docs/architecture.md has the full request lifecycle trace,
tests/test_prompts.py passing 4/4.
Next: Phase 6 (LangGraph orchestration — wiring it all together).
