"""Plain-text formatting for the four programs (no tables library)."""

from __future__ import annotations

from react.data import World
from react.loop import Trace
from react.tools import Tool


def format_world(world: World) -> str:
    lines = [f"Mundo: {world.name}  (máx. {world.max_steps} pasos)"]
    if world.source:
        lines.append(f"Archivo: {world.source}")
    lines.append("")
    lines.append("Hechos (Lookup):")
    if not world.facts:
        lines.append("  (ninguno)")
    for fact in world.facts:
        aliases = f"  aliases={list(fact.aliases)}" if fact.aliases else ""
        lines.append(f"  [{fact.key}]{aliases} {fact.text}")
    lines.append("")
    lines.append("Clima (Weather):")
    if not world.weather:
        lines.append("  (ninguno)")
    for item in world.weather:
        lines.append(f"  {item.city}: {item.temp} °C, {item.summary}")
    return "\n".join(lines)


def format_tools(tools: tuple[Tool, ...]) -> str:
    lines = ["Herramientas:"]
    for tool in tools:
        lines.append(f"  {tool.name}: {tool.description}")
    return "\n".join(lines)


def format_prompt(prompt: str) -> str:
    lines = ["Prompt ReAct:"]
    for line in prompt.splitlines():
        lines.append(f"  | {line}")
    return "\n".join(lines)


def format_trace(trace: Trace, *, title: str | None = None) -> str:
    lines = []
    if title:
        lines.append(title)
    lines.append(f"Pregunta: {trace.question}")
    if not trace.steps:
        lines.append("  (sin pasos)")
        return "\n".join(lines)
    for i, step in enumerate(trace.steps, start=1):
        lines.append(f"\nPaso {i}")
        lines.append(f"  Thought: {step.thought}")
        if step.final_answer is not None:
            lines.append(f"  Final Answer: {step.final_answer}")
            continue
        lines.append(f"  Action: {step.action}")
        lines.append(f"  Action Input: {step.action_input}")
        lines.append(f"  Observation: {step.observation}")
    lines.append("")
    if trace.stopped == "final":
        lines.append(f"Respuesta: {trace.answer}")
    else:
        lines.append(f"Paró en el máximo de pasos sin Final Answer.")
    return "\n".join(lines)


def format_step_cycle(trace: Trace) -> str:
    """One Thought → Action → Observation (program 02)."""
    if not trace.steps:
        return "No hubo ningún paso."
    step = trace.steps[0]
    lines = [
        f"Pregunta: {trace.question}",
        "",
        "Thought → Action → Observation",
        f"  Thought: {step.thought}",
    ]
    if step.final_answer is not None:
        lines.append("  (el modelo terminó sin herramienta)")
        lines.append(f"  Final Answer: {step.final_answer}")
        return "\n".join(lines)
    lines.append(f"  Action: {step.action}")
    lines.append(f"  Action Input: {step.action_input}")
    lines.append(f"  Observation: {step.observation}")
    return "\n".join(lines)
