import json
import pytest
from src.tools.appointment_tool import find_slots, book_slot, DOCTORS_FILE
from src.tools.ehr_tool import init_db, add_patient_record, get_patient_history

ORIGINAL_DOCTORS = [
    {"doctor_id": 1, "name": "Dr. Rao", "specialty": "nephrology",
     "available_slots": ["2026-09-10 10:00", "2026-09-10 14:00", "2026-09-12 09:00"]},
    {"doctor_id": 2, "name": "Dr. Chen", "specialty": "cardiology",
     "available_slots": ["2026-09-11 09:00", "2026-09-11 15:00"]},
    {"doctor_id": 3, "name": "Dr. Patel", "specialty": "dermatology",
     "available_slots": ["2026-09-13 11:00"]},
]


@pytest.fixture(autouse=True)
def reset_doctors_file():
    """Runs before every test in this file, resetting mock_doctors.json
    to a known state so book_slot()'s side effects don't leak between tests."""
    with open(DOCTORS_FILE, "w") as f:
        json.dump(ORIGINAL_DOCTORS, f, indent=2)
    yield
    with open(DOCTORS_FILE, "w") as f:
        json.dump(ORIGINAL_DOCTORS, f, indent=2)


def test_find_slots_returns_matching_specialty():
    slots = find_slots("nephrology")
    assert slots == ["2026-09-10 10:00", "2026-09-10 14:00", "2026-09-12 09:00"]


def test_book_slot_success():
    result = book_slot(1, "2026-09-10 10:00")
    assert result is True
    assert "2026-09-10 10:00" not in find_slots("nephrology")


def test_book_slot_prevents_double_booking():
    book_slot(1, "2026-09-10 10:00")
    result = book_slot(1, "2026-09-10 10:00")
    assert result is False


def test_get_patient_history_known_patient():
    init_db()
    add_patient_record(1, "John Doe Sr.", 70, "CKD stage 3")
    result = get_patient_history(1)
    assert result["name"] == "John Doe Sr."
    assert result["age"] == 70


def test_get_patient_history_unknown_patient_returns_none():
    init_db()
    result = get_patient_history(999999)
    assert result is None


def test_add_patient_record_persists():
    init_db()
    add_patient_record(2, "Maria Gomez", 45, "Type 2 diabetes")
    result = get_patient_history(2)
    assert result is not None
    assert result["history_text"] == "Type 2 diabetes"
