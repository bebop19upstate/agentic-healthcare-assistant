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
