import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.graph import app

load_dotenv()

_judge_llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

EVAL_SET_PATH = "data/eval_set.json"

GRADING_PROMPT = """You are grading an AI assistant's answer against a set of criteria. Respond with GRADE: CORRECT or GRADE: INCORRECT on the first line, followed by a one-sentence explanation.

Criteria the answer should meet:
{criteria}

The AI assistant answered:
{answer}

Grade:"""


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return str(content)


def _load_eval_set() -> list[dict]:
    with open(EVAL_SET_PATH) as f:
        return json.load(f)


def _grade_answer(answer: str, criteria: str) -> dict:
    prompt = GRADING_PROMPT.format(criteria=criteria, answer=answer)
    response = _judge_llm.invoke(prompt)
    graded_text = _extract_text(response.content)
    is_correct = graded_text.strip().upper().startswith("GRADE: CORRECT")
    return {"is_correct": is_correct, "explanation": graded_text}


def evaluate_all() -> list[dict]:
    eval_set = _load_eval_set()
    results = []
    for entry in eval_set:
        graph_result = app.invoke({
            "query": entry["query"],
            "patient_id": entry["patient_id"],
            "plan": [],
            "tool_results": {},
            "final_answer": "",
        })
        answer = graph_result["final_answer"]
        grade = _grade_answer(answer, entry["expected_criteria"])
        results.append({
            "id": entry["id"],
            "query": entry["query"],
            "answer": answer,
            "is_correct": grade["is_correct"],
            "explanation": grade["explanation"],
        })
    return results
