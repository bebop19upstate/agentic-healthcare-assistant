# Agentic Healthcare Assistant

A virtual healthcare assistant built with LangGraph, RAG, and long-term memory — capable of booking appointments, reading and updating patient records, and answering medical questions grounded in a reference corpus. Built as the capstone for the Applied Generative AI Specialisation.

## Problem statement

Modern healthcare administration relies on siloed tools with limited automation — appointment scheduling, patient history management, and medical information lookup are often disconnected. This project builds an Agentic Healthcare Assistant that combines an LLM-based planner, three specialized tools (appointment booking, EHR read/write, disease-information RAG), long-term memory, and an evaluation layer into one coordinated system, exposed through a Streamlit dashboard.

Full original problem statement: see the capstone PDF provided with this project.

## Architecture summary

The system is a LangGraph `StateGraph`: a planner decomposes each query into sub-tasks, each tagged with the tool that handles it (`ehr`, `appointment`, or `disease_search`). Conditional routing checks patient existence and query clarity before any tool runs; each tool checks whether the planner actually requested it before doing any work. A composer merges whatever tool results exist into one natural reply.

For the full component table, graph diagram, request lifecycle trace, design decisions, and known limitations, see **[docs/architecture.md](docs/architecture.md)**.

## Setup instructions

**1. Clone the repo and create a virtual environment:**
```bash
git clone https://github.com/bebop19upstate/agentic-healthcare-assistant.git
cd agentic-healthcare-assistant
python3.13 -m venv .venv
source .venv/bin/activate
```
> Use a standard Python 3.11–3.13 release from [python.org](https://www.python.org/downloads/macos/). A non-standard or very new Python build (e.g. an unofficial 3.14 build) may ship with a broken `pip` — if `pip install` fails with a `truststore`/`mac_ver()` SSL error, reinstall Python from python.org and recreate the venv.

**2. Install dependencies:**
```bash
python -m pip install -r requirements.txt
```

**3. Set up your API key:**
```bash
cp .env.example .env
```
Edit `.env` and add a real Gemini API key (`GOOGLE_API_KEY=...`), free at [Google AI Studio](https://aistudio.google.com/) — no credit card required. This project does not use Anthropic/Claude, since Anthropic has no free API tier.

**4. Recreate the local databases** (gitignored, not part of the repo):
```bash
python -c "from src.tools.ehr_tool import init_db; init_db()"
python -c "
from src.tools.ehr_tool import add_patient_record
add_patient_record(1, 'John Doe Sr.', 70, 'CKD stage 3')
add_patient_record(2, 'Maria Gomez', 45, 'Type 2 diabetes, diagnosed 2023. On metformin. Regular A1C monitoring.')
add_patient_record(3, 'Aiden Wu', 8, 'No chronic conditions. Up to date on vaccinations. Seen for seasonal allergies.')
"
```

**5. Verify everything imports correctly:**
```bash
python -c "import langgraph, langchain, faiss, streamlit; print('all good')"
```

## Running tests

```bash
python -m pytest -q
```

Run a single file during active development, rather than the whole suite, to avoid Gemini's free-tier rate limit (15 requests/minute on `gemini-3.5-flash-lite`):
```bash
python -m pytest -q tests/test_graph.py
```

Some tests mutate `data/mock_doctors.json` (booking a slot) or `data/patients.db` (adding a note) as a real side effect of testing real write behavior. If test data looks off, reset it:
```bash
cat > data/mock_doctors.json << 'DOCEOF'
[
  {"doctor_id": 1, "name": "Dr. Rao", "specialty": "nephrology", "available_slots": ["2026-09-10 10:00", "2026-09-10 14:00", "2026-09-12 09:00"]},
  {"doctor_id": 2, "name": "Dr. Chen", "specialty": "cardiology", "available_slots": ["2026-09-11 09:00", "2026-09-11 15:00"]},
  {"doctor_id": 3, "name": "Dr. Patel", "specialty": "dermatology", "available_slots": ["2026-09-13 11:00"]}
]
DOCEOF
```

## Running the app

```bash
streamlit run app/streamlit_app.py
```

Opens a 5-tab dashboard:
- **Chat** — ask questions directly, or replay one of five pre-built test scenarios from the dropdown
- **Doctor view** — live doctor/specialty/slot data
- **Medical info** — the raw grounded answer from the last disease-search query
- **Metrics** — per-tool success rate and average latency, accumulated across all testing
- **Memory & logs** — the planner's last decomposition, retrieved memory context, and the full tool-call log

If you see `ModuleNotFoundError: No module named 'src'`, make sure you're running the command from the project root, not from inside `app/`.

## Screenshots

_(Add screenshots of the Chat, Doctor view, and Metrics tabs here before final submission.)_

## Known limitations

See **[docs/architecture.md](docs/architecture.md#known-limitations)** for the full list, including:
- Gemini free-tier rate limits (15 requests/minute)
- Doctor scheduling and disease information are mocked with static local files, not live APIs
- Specialty and read/write detection use simple text matching, not structured classification
