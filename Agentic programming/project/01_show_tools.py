#!/usr/bin/env python3
"""Program 1: tools, the toy world, and the ReAct prompt.

Stage 1 of ReAct. Before the loop runs, show what the agent may call
(Calculator, Lookup, Weather), the facts and forecasts those tools read,
and the canonical Thought / Action / Observation prompt from the lecture.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from react.cli import build_parser, load, tools_for  # noqa: E402
from react.format import format_prompt, format_tools, format_world  # noqa: E402
from react.prompt import build_prompt  # noqa: E402


def main() -> None:
    args = build_parser("Show the tools, the YAML world, and the ReAct prompt.").parse_args()
    world = load(args)
    tools = tools_for(world)
    question = args.query or (world.queries[0] if world.queries else "¿cuál es la pregunta?")

    print(format_world(world))
    print()
    print(format_tools(tools))
    print()
    print(format_prompt(build_prompt(question, tools)))
    print()
    print("El LLM es el cerebro: elige Thought y Action. Las tools son el entorno.")
    print("Edita data/viaje.yaml (o usa --data) y vuelve a ejecutar.")


if __name__ == "__main__":
    main()
