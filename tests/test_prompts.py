from src.prompts.templates import (
    PLANNER_PROMPT,
    DISEASE_ANSWER_PROMPT,
    EHR_SUMMARY_PROMPT,
    COMPOSER_PROMPT,
)


def test_planner_prompt_renders_with_query():
    rendered = PLANNER_PROMPT.format(query="Book me a cardiologist")
    assert "Book me a cardiologist" in rendered
    assert "{query}" not in rendered


def test_disease_answer_prompt_renders_with_excerpts_and_question():
    rendered = DISEASE_ANSWER_PROMPT.format(
        excerpts="- Some excerpt about CKD treatment.",
        question="What treats CKD?",
    )
    assert "Some excerpt about CKD treatment." in rendered
    assert "What treats CKD?" in rendered


def test_ehr_summary_prompt_renders_with_history():
    rendered = EHR_SUMMARY_PROMPT.format(
        name="John Doe Sr.", age=70, history_text="CKD stage 3"
    )
    assert "John Doe Sr." in rendered
    assert "CKD stage 3" in rendered


def test_composer_prompt_renders_with_partial_results():
    rendered = COMPOSER_PROMPT.format(
        results="Appointment: Booked with Dr. Rao for 2026-09-10 10:00."
    )
    assert "Booked with Dr. Rao" in rendered
    assert "{results}" not in rendered
