# Day 10 — Memory & Logs Interface

## What I did
- Captured planner's plan into st.session_state after each query
- Added retrieved_memory as a new AgentState field, exposed by ehr_node,
  updating every initial-state dict across graph.py, test_graph.py, and
  streamlit_app.py to include the new required field
- Built a 5th "Memory & logs" tab showing: numbered plan with tools,
  retrieved memory context, and the full accumulated tool call log as an
  interactive st.dataframe table
- Added a scenario-replay dropdown covering all 5 Phase 7 test scenarios,
  including dynamic patient_id override (999 for the unknown-patient case)
  so the UI can demo edge cases with one click

## What I learned
- Streamlit's auto-reload only re-runs the top-level script — it does NOT
  re-import already-imported modules (like src/graph.py) within the same
  running process. Adding a new AgentState field caused a KeyError that
  ONLY showed up in the long-running Streamlit server, not in fresh
  `python -c` calls, because the server was still using a stale cached
  version of the graph from before the field existed. Fix: fully restart
  (not just refresh) after changing any imported module, not just the app
  file itself.
- st.dataframe() renders as an interactive JS grid — doesn't copy-paste as
  plain text even when working correctly. A screenshot settled what a
  text-paste couldn't.
- Confirmed patient_check correctly halts the ENTIRE pipeline before any
  tool runs for an unknown patient — verified this concretely by seeing the
  tool call log had zero new rows for that scenario, not just checking the
  final answer text.

## Status
Phase 10 complete: 5-tab dashboard (Chat, Doctor view, Medical info, Metrics,
Memory & logs) with full internal-reasoning visibility and one-click
scenario replay. mock_doctors.json reset to clean seed state.
Next: Phase 11 (documentation & polish).
