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

## Update: model swap
- gemini-3.6-flash's free tier daily quota is only 20 requests/day — far too
  low for iterative testing. Switched to gemini-3.5-flash-lite: higher quota,
  faster responses, same family.
- Strengthened planner prompt with an explicit ehr rule + worked example after
  noticing the model inconsistently dropped the ehr sub-task for scenarios
  referencing an existing patient. Verified consistency with 5 manual runs
  before trusting it in tests.
- Tightened tests to assert the full expected tool set for the combined
  scenario, and added a test with a different patient/condition to confirm
  the model generalized the rule rather than pattern-matching the example.
