import json

DOCTORS_FILE = "data/mock_doctors.json"


def _load_doctors() -> list[dict]:
    with open(DOCTORS_FILE) as f:
        return json.load(f)


def find_slots(specialty: str) -> list[str]:
    doctors = _load_doctors()
    slots = []
    for doctor in doctors:
        if doctor["specialty"].lower() == specialty.lower():
            slots.extend(doctor["available_slots"])
    return slots
