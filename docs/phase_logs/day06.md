# Day 6 — LangGraph Orchestration

## What I did
- Defined AgentState (TypedDict) as the shared state schema
- Built a one-node graph (planner only) before adding anything else
- Verified conditional routing mechanism in isolation with a fake 2-branch
  scratch graph, before touching real tools
- Added ehr_node, appointment_node, disease_search_node one at a time,
  testing after each addition
- Added composer_node, producing the first fully coherent end-to-end reply
  combining all three tool results
- Used app.stream() to inspect the state trace node-by-node
- Wrote tests/test_graph.py, 3/3 passing, with a fixture resetting
  mock_doctors.json (same mutation-safety pattern as test_tools.py)

## What I learned
- Python executes top to bottom — a function must be DEFINED before code
  that references it runs, even inside the same file. Hit this directly:
  graph-wiring code referenced ehr_node before its def existed further down.
- A tool node should be given its own FOCUSED sub-task text (from the
  planner's plan), not the raw full query — passing the whole mixed query
  to disease_search_node caused it to comment on booking, which it had no
  business seeing. Fixed with a _get_subtask_query() helper.
- app.stream() shows the state after each node individually — genuinely
  useful for debugging, since it shows exactly where an answer might go
  wrong, not just the final result.
- Fluent-sounding LLM output still needs a careful read — caught the
  composer addressing "you" when the query was from an attendant asking on
  behalf of a parent, and a typo ("CKidney Disease") in one generation.
- Known follow-up: ehr_node still uses the raw query for memory lookup
  (same bug class as disease_search had) — not yet triggered, but flagged
  for before Phase 7's testing.

## Status
Phase 6 complete: src/graph.py has a full 5-node LangGraph pipeline
(planner -> ehr -> appointment -> disease_search -> composer), producing
coherent, grounded final answers. tests/test_graph.py passing 3/3.
Next: Phase 7 (end-to-end testing & edge cases).
