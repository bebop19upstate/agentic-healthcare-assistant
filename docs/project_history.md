# Project History & Status

A single consolidated view of everything built so far, pulled together from
the individual day logs in `docs/phase_logs/`. For system design details,
see `docs/architecture.md`. For the full phased plan and micro-steps, see
the original planning document.

---

## Phase 0 — Environment & Project Scaffold ✅ COMPLETE

**Built:** Python virtual environment, full folder skeleton, `.gitignore`,
`.env`/`.env.example` for secrets, all core dependencies installed.

**Notable issue resolved:** Initial Python install (3.14, non-standard Clang
build) had a broken `pip`/`ensurepip` due to a `truststore`/`mac_ver()` SSL
bug specific to that build. Fixed by installing Python 3.13 from python.org
and recreating the venv.

---

## Phase 1 — Agent Planning and Goal Decomposition ✅ COMPLETE

**Built:** `src/planner.py` — takes a raw query, returns a structured `Plan`
(Pydantic model) of sub-tasks, each tagged with the tool that handles it
(`ehr`, `appointment`, `disease_search`). Prompt lives in
`src/prompts/templates.py` as `PLANNER_PROMPT`.

**Notable issues resolved:**
- Switched from Claude/Anthropic (no free API tier) to Google Gemini.
- Switched from flagship `gemini-3.6-flash` to `gemini-3.5-flash-lite` after
  hitting a 20-requests/day free-tier quota wall.
- Planner initially, inconsistently dropped the `ehr` sub-task for queries
  referencing an existing patient/relative. Fixed by adding an explicit rule
  and a worked example to `PLANNER_PROMPT`; verified with repeated runs.

**Tests:** `tests/test_planner.py` — 4 passing, tolerant of natural
LLM output variation (asserts which tools appear, not exact wording).

---

## Phase 2 — Tool Setup: Appointment & EHR ✅ COMPLETE

**Built:**
- `src/tools/appointment_tool.py` — `find_slots(specialty)`,
  `book_slot(doctor_id, slot)` (prevents double-booking), later extended in
  Phase 7 with `book_first_available(specialty)`.
- `src/tools/ehr_tool.py` — SQLite-backed (`data/patients.db`),
  `get_patient_history(patient_id)` (returns `None` gracefully if not found),
  `add_patient_record(...)`.
- Seed data: 3 patients, including patient 1 (John Doe Sr., 70, CKD stage 3
  — the running sample-scenario patient used throughout the project).

**Notable issue resolved:** `book_slot()` mutates `data/mock_doctors.json` on
disk — manual repeated testing without resetting the file gave confusing,
inconsistent results. Fixed with a `pytest` fixture (`autouse=True`) that
resets the file before and after every test.

**Tests:** `tests/test_tools.py` — 6 passing, repeatably (verified twice
in a row).

---

## Phase 3 — Vector Store & Memory Modules ✅ COMPLETE

**Built:**
- `src/memory/vector_store.py` — `VectorStore` class wrapping FAISS
  (`IndexFlatL2`) + a parallel text list, using `sentence-transformers`
  (`all-MiniLM-L6-v2`) for embeddings.
- `src/memory/memory_manager.py` — one isolated `VectorStore` per
  `patient_id`, preventing any cross-patient memory leakage.
- Connected to real Phase 2 EHR data via generated summary sentences.

**Key concept verified by hand:** cosine similarity of related sentences
(~0.43) vs. unrelated (~0.004) — the entire mechanism behind meaning-based
search, before any FAISS code was written.

**Tests:** `tests/test_memory.py` — 3 passing, including a dedicated
per-patient isolation test.

---

## Phase 4 — Disease Search / RAG Tool ✅ COMPLETE

**Built:**
- `data/disease_corpus/` — 5 offline reference documents (CKD, diabetes,
  pediatric wellness) standing in for live Medline/WHO APIs.
- `src/tools/disease_search_tool.py` — `chunk_text()`, a separate FAISS
  index for disease chunks (reusing the Phase 3 `VectorStore` class),
  `retrieve_chunks()`, `answer_from_chunks()` (strict "use ONLY these
  excerpts" grounding), and the single entry point `search_disease_info()`.

**Verification approach:** every claim in sample answers was manually traced
back to the specific source `.txt` file to confirm genuine grounding, not
just plausible-sounding text.

**Tests:** `tests/test_disease_search.py` — 3 passing.

---

## Phase 5 — Prompt Engineering & Task Chaining ✅ COMPLETE

**Built:** consolidated all prompts into `src/prompts/templates.py`
(`PLANNER_PROMPT`, `DISEASE_ANSWER_PROMPT`, `EHR_SUMMARY_PROMPT`,
`COMPOSER_PROMPT`). Traced the full sample-scenario request lifecycle in
`docs/architecture.md` before writing any graph code.

**Key design decision:** `COMPOSER_PROMPT` explicitly instructs the model
not to reference sections that are missing — verified this prevents
awkward mentions of, e.g., treatment info for a booking-only query.

**Tests:** `tests/test_prompts.py` — 4 passing, all fast (no LLM calls,
just template-rendering checks).

---

## Phase 6 — LangGraph Orchestration ✅ COMPLETE

**Built:** `src/graph.py` — `AgentState` (TypedDict), and a full pipeline:
`planner_node` → `ehr_node` → `appointment_node` → `disease_search_node` →
`composer_node`, compiled as a LangGraph `StateGraph`.

**Notable issues resolved:**
- A function-definition-order bug (`ehr_node` referenced before its `def`
  existed) caused a `NameError` — fixed by reordering.
- `disease_search_node` was initially passed the *entire raw query*
  (including unrelated booking language), causing confused answers. Fixed
  with `_get_subtask_query()`, which pulls each tool's own focused sub-task
  text from the plan instead.
- Same fix later applied to `ehr_node`'s memory lookup.

**First full end-to-end answer produced** combining EHR summary, a real
booking, and a grounded treatment summary into one coherent reply.

**Tests:** `tests/test_graph.py` — 3 passing.

---

## Phase 7 — End-to-End Testing & Edge Cases 🔄 IN PROGRESS

**Scenarios defined** (see `docs/architecture.md` for full list and design
decisions): booking-only, EHR-update-only, disease-info-only, unknown
patient (decision: system stops entirely, does not partially proceed),
ambiguous query (decision: composer must ask "Could you tell me more about
what you need?").

**Completed so far:**
- Discovered every graph node ran unconditionally regardless of the plan —
  fixed by adding `_tool_in_plan()` checks to all three tool nodes, so a
  node fully skips its work (including any LLM call) if its tool wasn't
  requested by the planner.
- Booking-only scenario testing uncovered `appointment_node` was hardcoded
  to always book nephrology with Dr. Rao, regardless of the requested
  specialty — a genuine correctness bug, not cosmetic. Fixed with
  `book_first_available(specialty)` in `appointment_tool.py`.
- That fix initially still failed for "cardiologist" (vs. "cardiology") due
  to an exact-substring match missing the different word ending. Fixed by
  matching on a shared word root (`"cardiolog"`) instead of the full field
  name.

**Remaining:** EHR-update-only scenario (needs new write-capability design
in `ehr_node`), disease-info-only, unknown-patient handling, ambiguous-query
handling, and `tests/test_graph.py` additions for all scenarios.

---

## Not Yet Started

- **Phase 8** — Model evaluation (QAEvalChain, tool-call logging)
- **Phase 9** — Streamlit dashboard
- **Phase 10** — Memory & logs interface
- **Phase 11** — Documentation & polish
- **Phase 12** — Final packaging & optional deployment

---

## Recurring lessons worth remembering

- **LLM output is non-deterministic** — design tests around presence of
  expected content, not exact wording.
- **A tool node should only ever see its own focused sub-task**, not the
  raw mixed query — this exact bug appeared twice (disease_search, then ehr)
  and was fixed the same way both times.
- **Any function that mutates a file on disk** (`book_slot()`,
  `add_patient_record()`) needs a reset step before repeatable testing —
  handled via `pytest` fixtures.
- **Fluent-sounding LLM output still needs a careful read** — several real
  bugs (wrong specialty booked, wrong query passed to a tool) were only
  caught by actually reading output closely, not by assuming "it ran
  without crashing" meant "it's correct."
