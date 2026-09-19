"""Turn the model's free text into a Thought + Action, or a Final Answer."""

from __future__ import annotations

import re
from dataclasses import dataclass

_FINAL = re.compile(
    r"Thought:\s*(?P<thought>.*?)\s*Final Answer:\s*(?P<answer>.*)\s*\Z",
    re.IGNORECASE | re.DOTALL,
)
_ACTION = re.compile(
    r"Thought:\s*(?P<thought>.*?)\s*Action:\s*(?P<action>\S+)\s*"
    r"Action Input:\s*(?P<input>.*)\s*\Z",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class Decision:
    thought: str
    action: str | None = None
    action_input: str | None = None
    final_answer: str | None = None

    @property
    def done(self) -> bool:
        return self.final_answer is not None


def parse(text: str) -> Decision:
    """Read one model turn. Final Answer wins if both patterns are present."""
    blob = _prepare(text)
    final = _FINAL.search(blob)
    if final and "Action:" not in (final.group("thought") or ""):
        return Decision(
            thought=_clean(final.group("thought")),
            final_answer=_clean(final.group("answer")),
        )
    action = _ACTION.search(blob)
    if action:
        return Decision(
            thought=_clean(action.group("thought")),
            action=_clean(action.group("action")).strip("*`[]"),
            action_input=_clean(action.group("input")),
        )
    if final:
        return Decision(
            thought=_clean(final.group("thought")),
            final_answer=_clean(final.group("answer")),
        )
    raise ValueError(
        "could not parse a ReAct turn. Expected Thought + Action + Action Input, "
        f"or Thought + Final Answer. Got:\n{blob}"
    )


def _prepare(text: str) -> str:
    blob = text.strip()
    if blob.startswith("```"):
        blob = re.sub(r"^```(?:\w+)?\s*", "", blob)
        blob = re.sub(r"\s*```$", "", blob)
        blob = blob.strip()
    blob = re.split(r"^Observation\s*:", blob, maxsplit=1, flags=re.IGNORECASE | re.MULTILINE)[0]
    return blob.strip()


def _clean(text: str) -> str:
    return " ".join((text or "").strip().split())
