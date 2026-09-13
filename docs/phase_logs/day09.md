# Day 9 — Streamlit Dashboard

## What I did
- Got a minimal Streamlit app running (title + text), confirming the tooling
  itself worked before adding real logic
- Wired a text input + submit button to the real graph, producing the first
  answer rendered in an actual browser UI
- Added chat history via st.session_state, so multiple exchanges persist
  across submissions instead of each one replacing the last
- Built out 4 tabs: Chat, Doctor view (live doctor/slot data), Medical info
  (raw disease_search result), Metrics (per-tool success rate + latency,
  pulled from the accumulated log file across ALL testing sessions)
- Verified streamlit_app.py contains zero new functions/classes — confirmed
  it's pure UI orchestration importing from src/, no duplicated logic

## What I learned
- Streamlit doesn't automatically add the project root to Python's import
  path the way pytest (with pyproject.toml) does — fixed with an explicit
  sys.path.insert() at the top of the app, calculated relative to the file's
  own location so it works regardless of the working directory
- A "described change didn't land" issue hit again (step 9.3's session-state
  code) — caught by directly cat-ing the file rather than trusting the
  described edit happened, same lesson as Phase 8
- Ctrl+C not fully stopping a Streamlit server (or closing a terminal window
  instead of properly stopping it) leaves a zombie background process. SIX
  accumulated today, several bound to different ports, causing genuinely
  confusing "session state isn't persisting" symptoms that were actually
  "you're looking at a different, stale process" — diagnosed with
  `ps aux | grep streamlit` and fixed with `pkill -9 -f "streamlit run"`
- transformers (a sentence-transformers dependency) has an eager import
  chain that touched an optional torchvision-dependent module under
  Streamlit's execution model specifically — fixed by installing torchvision,
  even though the project never uses image processing directly

## Status
Phase 9 complete: app/streamlit_app.py has a working 4-tab dashboard
(Chat, Doctor view, Medical info, Metrics), all pulling live data from
existing src/ modules with no duplicated logic in the UI layer.
Next: Phase 10 (memory & logs interface).
