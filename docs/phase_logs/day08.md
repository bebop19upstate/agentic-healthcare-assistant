# Day 8 — Model Evaluation

## What I did
- Built a 5-entry eval set (data/eval_set.json) based on Phase 7's scenarios,
  using criteria-based grading rather than exact-match expected answers
- Verified LLM-as-judge grading manually before automating it, catching a
  real mistake (forgot to substitute the actual answer into the grading
  prompt) — the judge correctly flagged it as INCORRECT rather than
  hallucinating a grade for missing input
- Built src/evaluation/evaluator.py: evaluate_all() runs the full graph for
  each eval-set entry and grades the answer against its criteria — 5/5 passed
- Built src/logging_utils.py: timed_tool_call() context manager that times
  and logs every tool call (name, success, latency) to a CSV, even if the
  call raises an exception
- Wired logging into all three tool nodes with one `with` line each
- Built src/evaluation/summary_report.py combining both: answer-quality
  grades + per-tool success rate and average latency in one report

## What I learned
- QAEvalChain (the literal LangChain construct) didn't fit cleanly with this
  project's direct-LLM-call style — built an equivalent "LLM-as-judge"
  pattern by hand instead: a grading prompt + the same ChatGoogleGenerativeAI
  client used everywhere else
- A context manager (@contextmanager, try/except/finally) is a clean way to
  add "always do X before and after, even on failure" behavior with minimal
  code changes to existing functions
- Operational logging surfaced something real just from a handful of test
  runs: disease_search is consistently the slowest tool (755-1900ms, always
  makes an LLM call) vs. appointment (under 1ms, pure file I/O) — useful to
  know before Phase 9's UI needs to show loading states
- Multiple manual code edits (via VS Code) silently failed to save/apply
  during this phase — caught only by re-checking file content with sed/grep
  after each edit rather than assuming a described change actually happened

## Status
Phase 8 complete: 5/5 eval-set scenarios graded correct, operational logging
in place for all 3 tools, summary report working. Baseline established:
100% tool success rate, disease_search averaging ~1.3s, ehr ~0.5s (varies
based on whether a write/LLM extraction happens), appointment ~0.6ms.
Next: Phase 9 (Streamlit dashboard).
