# Day 2 — Tool Setup: Appointment & EHR

## What I did
- Built mock_doctors.json with 3 doctors across different specialties
- Wrote find_slots() (read-only) and book_slot() (mutating, with double-booking
  prevention) in appointment_tool.py
- Designed and created the patients SQLite table, with add_patient_record()
  and get_patient_history() (returns None gracefully for unknown patients)
- Seeded 3 varied patients including the CKD sample-scenario patient (id=1)
- Wrote tests/test_tools.py with 6 passing tests

## What I learned
- book_slot() has a real side effect (rewrites mock_doctors.json on disk) —
  unlike find_slots(), running it twice doesn't give the same result the
  second time, since state has genuinely changed
- pytest fixtures (@pytest.fixture(autouse=True)) can reset state before/after
  every test automatically, so mutating operations can be tested repeatably
- SQLite's "INSERT OR REPLACE" makes seeding/reseeding a patient idempotent
  (safe to rerun without creating duplicates)

## Snags hit
- Manually tested book_slot() twice in a row without resetting first — the
  second run's results were confusing until I realized the first run had
  already permanently modified the JSON file. Fixed by adding a pytest
  fixture that resets to a known state before (and after) every test.

## Status
Phase 2 complete: src/tools/appointment_tool.py, src/tools/ehr_tool.py,
tests/test_tools.py all working, 6/6 tests passing repeatably.
Next: Phase 3 (FAISS vector store & memory modules).
