# Day 7 — End-to-End Testing & Edge Cases

## What I did
- Wrote 5 scenarios in plain English with explicit expected behavior BEFORE
  any code, including two real design decisions: unknown patient = stop
  entirely (don't partially proceed), ambiguous query = ask "Could you tell
  me more about what you need?" verbatim
- Discovered every graph node ran unconditionally regardless of the plan —
  added _tool_in_plan() checks so nodes skip work (including LLM calls)
  when their tool wasn't requested
- Found and fixed appointment_node hardcoded to always book nephrology
  regardless of requested specialty
- Found and fixed a substring-matching bug: "cardiology" didn't match
  "cardiologist" — fixed by matching shared word roots instead of full words
- Built real EHR write capability (append_patient_note); found and fixed a
  multi-subtask bug where ehr_node only processed the FIRST sub-task tagged
  "ehr," silently ignoring a second one (the actual write instruction)
- Found the write was persisting the raw instruction text as the "note"
  instead of clean clinical content — added an LLM extraction step to fix it
- Added conditional routing (StateGraph conditional edges) for real, for
  patient-existence checking (stops entirely on unknown patient) and
  ambiguous-query detection (empty plan -> hardcoded clarification message)
- Found the planner sometimes phrased an EHR-write request as a READ
  sub-task, missing the write entirely — fixed with an explicit prompt rule
  + worked example, verified 3/3 consistent afterward
- Hit two terminal/tooling mixups mid-session (pasted a stale diagnostic
  command instead of the actual fix script) — resolved by re-verifying
  file state directly (grep for function definitions) rather than assuming

## What I learned
- A graph "working" (no crash, plausible final answer) is NOT the same as
  it doing the right thing — the silent EHR-write failure produced a
  fluent, confident-sounding reply while doing nothing at all
- LLM non-determinism affects MORE than wording — it can affect which
  ACTION TYPE (read vs. write) gets inferred for a sub-task, not just
  phrasing details. Same root cause, new manifestation, one phase later
- Substring matching for classification (specialty detection, read/write
  detection) is fragile — natural language variation (cardiologist vs.
  cardiology; "log that" vs "add a note") breaks simple keyword checks.
  The most durable fix is usually upstream, in the prompt that generates
  the text being matched, not downstream keyword lists
- Conditional edges in LangGraph need a router FUNCTION (not just a bool)
  returning a string key that maps to the next node
- Always verify file state directly (grep, cat) rather than trust that a
  previous command definitely ran correctly, especially after any terminal
  confusion

## Status
Phase 7 complete: all 5 scenarios implemented and passing, tests/test_graph.py
now has 8/8 tests covering the original combined scenario plus every edge
case. Multiple real correctness bugs found and fixed, not just theoretical
ones. mock_doctors.json reset to clean seed state.
Next: Phase 8 (Model evaluation with QAEvalChain).
