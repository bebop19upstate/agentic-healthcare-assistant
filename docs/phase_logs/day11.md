# Day 11 — Documentation & Polish

## What I did
- Filled in docs/architecture.md properly: component table, a mermaid graph
  diagram matching the actual Phase 7 wiring (including conditional edges),
  a "what's mocked vs. real" table, and key design decisions/trade-offs
- Did a genuine fresh-environment test: fresh venv, installed purely from
  requirements.txt, recreated databases, ran the full test suite and the
  Streamlit app — all succeeded
- Found two real, previously undocumented gaps: (1) a per-minute Gemini
  rate limit (15 req/min) that the full test suite can trip when run
  back-to-back, and (2) the implicit multi-step setup needed for .env and
  the databases, since both are gitignored
- Accidentally lost the entire .venv (and the intended backup) mid-test —
  rebuilt it completely from requirements.txt alone as an unplanned but
  genuine "what if this gets deleted" recovery drill; confirmed rebuild
  worked via a full pytest run afterward
- Wrote the real README.md, entirely grounded in what the fresh-environment
  test actually required, not assumed from memory

## What I learned
- A per-minute rate limit is a DIFFERENT failure mode than the daily quota
  hit in Phase 1 — same underlying constraint (free tier), different time
  window, different trigger (test suite burst vs. accumulated daily usage)
- requirements.txt alone was sufficient to fully rebuild the project's
  dependencies from a completely fresh, even accidentally-deleted, venv —
  validating that Phase 0's `pip freeze` habit paid off
- Writing documentation from an actual clean-room test surfaces real gaps
  that writing from memory never would have caught (the rate limit,
  specifically, was invisible until an unusually large batch of real calls
  happened at once)

## Status
Phase 11 complete: docs/architecture.md is comprehensive (component table,
diagram, lifecycle trace, mocked-vs-real, design decisions, known
limitations), README.md is complete and verified against a real fresh
install. Environment fully rebuilt and confirmed working (8/8 graph tests
passing) after an accidental venv loss mid-phase.
Next: Phase 12 (final packaging & optional deployment).
