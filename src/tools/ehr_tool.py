import sqlite3

DB_PATH = "data/patients.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            history_text TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_patient_record(patient_id: int, name: str, age: int, history_text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO patients (patient_id, name, age, history_text) VALUES (?, ?, ?, ?)",
        (patient_id, name, age, history_text),
    )
    conn.commit()
    conn.close()


def get_patient_history(patient_id: int) -> dict | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT patient_id, name, age, history_text FROM patients WHERE patient_id = ?",
        (patient_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return {
        "patient_id": row[0],
        "name": row[1],
        "age": row[2],
        "history_text": row[3],
    }

def append_patient_note(patient_id: int, note: str) -> bool:
    patient = get_patient_history(patient_id)
    if not patient:
        return False
    updated_history = f"{patient['history_text']} | Note: {note}"
    add_patient_record(patient_id, patient["name"], patient["age"], updated_history)

    return True
