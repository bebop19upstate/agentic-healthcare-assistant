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


def book_slot(doctor_id: int, slot: str) -> bool:
    """Books a slot by removing it from the doctor's available_slots.
    Returns True if booked successfully, False if the slot wasn't available
    (already booked, or doesn't exist)."""
    doctors = _load_doctors()
    booked = False
    for doctor in doctors:
        if doctor["doctor_id"] == doctor_id and slot in doctor["available_slots"]:
            doctor["available_slots"].remove(slot)
            booked = True
            break

    if booked:
        with open(DOCTORS_FILE, "w") as f:
            json.dump(doctors, f, indent=2)

    return booked
