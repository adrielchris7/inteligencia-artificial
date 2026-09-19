"""The ReAct loop: Thought → Action → Observation, until a Final Answer."""

from __future__ import annotations

from dataclasses import dataclass, field

from react.parse import Decision, parse
from react.prompt import build_prompt
from react.tools import Tool, run_tool


@dataclass
class Step:
    thought: str
    action: str | None = None
    action_input: str | None = None
    observation: str | None = None
    final_answer: str | None = None


@dataclass
class Trace:
    question: str
    prompt: str
    steps: list[Step] = field(default_factory=list)
    stopped: str = "max_steps"  # "final" | "max_steps"

    @property
    def answer(self) -> str | None:
        if not self.steps:
            return None
        return self.steps[-1].final_answer


class Brain:
    """Anything that, given the prompt and the trace so far, writes one ReAct turn."""

    def next_action(self, question: str, steps: list[Step], prompt: str) -> str:  # pragma: no cover
        raise NotImplementedError


def run_react(
    question: str,
    tools: tuple[Tool, ...],
    brain: Brain,
    max_steps: int,
) -> Trace:
    """Repeat think → (optional) act → observe until Final Answer or max_steps."""
    prompt = build_prompt(question, tools)
    trace = Trace(question=question, prompt=prompt)
    for _ in range(max_steps):
        raw = brain.next_action(question, trace.steps, prompt)
        decision = parse(raw)
        step = _step_from(decision)
        if decision.done:
            trace.steps.append(step)
            trace.stopped = "final"
            return trace
        step.observation = run_tool(tools, decision.action or "", decision.action_input or "")
        trace.steps.append(step)
    return trace


def _step_from(decision: Decision) -> Step:
    return Step(
        thought=decision.thought,
        action=decision.action,
        action_input=decision.action_input,
        final_answer=decision.final_answer,
    )
