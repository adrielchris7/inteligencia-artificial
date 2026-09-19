"""Gemini writes the next ReAct step.

Same client as LLMs/Notebooks/04 LLM Gemini API.ipynb: google-genai and
gemini-3.6-flash. The loop does not change; only this brain does.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

from react.loop import Step

DEFAULT_MODEL = "gemini-3.6-flash"
_KEY_URL = "https://aistudio.google.com/apikey"
_PROJECT_ENV = Path(__file__).resolve().parent.parent / ".env"


class GeminiBrain:
    """Call Gemini once per ReAct turn. Stop before it invents an Observation."""

    def __init__(self, model: str | None = None) -> None:
        load_dotenv(_PROJECT_ENV)
        load_dotenv(find_dotenv())
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise SystemExit(
                "Missing GEMINI_API_KEY. Copy .env.example to .env and paste a key from "
                f"{_KEY_URL}"
            )
        self.model = model or os.getenv("GEMINI_MODEL") or DEFAULT_MODEL
        self._client = genai.Client(api_key=api_key)

    def next_action(self, question: str, steps: list[Step], prompt: str) -> str:
        del question  # already inside the ReAct prompt
        response = self._client.models.generate_content(
            model=self.model,
            contents=_contents(prompt, steps),
            config=types.GenerateContentConfig(
                temperature=0.0,
                stop_sequences=["\nObservation:", "\nObservation"],
            ),
        )
        return _normalize(_text(response))


def _contents(prompt: str, steps: list[Step]) -> str:
    lines = [prompt.rstrip(), ""]
    for step in steps:
        lines.append(f"Thought: {step.thought}")
        if step.final_answer is not None:
            lines.append(f"Final Answer: {step.final_answer}")
            continue
        lines.append(f"Action: {step.action}")
        lines.append(f"Action Input: {step.action_input}")
        lines.append(f"Observation: {step.observation}")
    lines.append("Thought:")
    return "\n".join(lines)


def _text(response: object) -> str:
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        parts = getattr(getattr(candidate, "content", None), "parts", None) or []
        chunks = [part.text for part in parts if getattr(part, "text", None)]
        if chunks:
            return "".join(chunks)
    return getattr(response, "text", None) or ""


def _normalize(text: str) -> str:
    blob = text.strip()
    if blob.startswith("```"):
        blob = re.sub(r"^```(?:\w+)?\s*", "", blob)
        blob = re.sub(r"\s*```$", "", blob)
        blob = blob.strip()
    if blob.casefold().startswith("final answer:"):
        blob = "Thought: Ya sé la respuesta final\n" + blob
    elif not blob.casefold().startswith("thought:"):
        blob = "Thought: " + blob
    return blob
