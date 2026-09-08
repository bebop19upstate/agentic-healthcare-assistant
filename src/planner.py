def plan(query: str) -> list[dict]:
    return [
        {"subtask": "identify patient context", "tool": "ehr"},
        {"subtask": "retrieve medical history", "tool": "ehr"},
        {"subtask": "book nephrologist appointment", "tool": "appointment"},
        {"subtask": "summarize treatment options", "tool": "disease_search"},
    ]
