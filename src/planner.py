import json
import re
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

from src.prompts.templates import PLANNER_PROMPT

load_dotenv()


class SubTask(BaseModel):
    subtask: str
    tool: str  # one of: "appointment", "ehr", "disease_search"


class Plan(BaseModel):
    subtasks: list[SubTask]


_llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")


def _extract_text(content) -> str:
    """Handle both plain-string and structured content-block responses."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [block.get("text", "") for block in content if isinstance(block, dict)]
        return "".join(parts)
    return str(content)


def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def plan(query: str) -> Plan:
    prompt = PLANNER_PROMPT.format(query=query)
    response = _llm.invoke(prompt)
    raw_text = _extract_text(response.content)
    cleaned = _strip_markdown_fences(raw_text)
    data = json.loads(cleaned)
    return Plan(**data)
