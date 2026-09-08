# Day 1 — Agent Planning and Goal Decomposition

## What I did
- Built a fake hardcoded planner first, then the real Gemini-backed version
- Designed and hand-tested the planner prompt in Google AI Studio before coding it
- Defined Pydantic models (SubTask, Plan) to validate LLM output
- Wired prompt + LLM + parsing into plan()
- Wrote tests tolerant of natural LLM output variation

## What I learned
- LLM output is non-deterministic even for the same input — design around it,
  don't fight it
- Gemini 3.6 Flash deprecated temperature/top_p/top_k entirely — sampling
  params are silently ignored on this model family
- pytest needs `pythonpath = ["."]` in pyproject.toml (or `python -m pytest`)
  to resolve `src.` imports correctly

## Snags hit
- First prompt attempt got a direct medical answer instead of JSON — fixed by
  being much more explicit ("you are a planner, not a medical assistant")
- temperature=0 had no effect (deprecated on this model) — accepted output
  variation instead and wrote tests that check for tool presence, not exact
  wording/count
- ModuleNotFoundError on `src` in pytest — fixed with pyproject.toml pythonpath

## Status
Phase 1 complete: src/planner.py, src/prompts/templates.py, tests/test_planner.py
all working. Next: Phase 2 (appointment & EHR tools).
