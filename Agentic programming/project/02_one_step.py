#!/usr/bin/env python3
"""Program 2: one Thought → Action → Observation cycle.

Stage 2 of ReAct. The agent thinks, calls one tool, and we print the
observation. It does not loop yet — that is program 03. The packing
question's first action is Weather; a math question's first action is
Calculator.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from react.cli import build_parser, load, queries_from, run_one  # noqa: E402
from react.format import format_step_cycle  # noqa: E402


def main() -> None:
    args = build_parser("Run a single Thought → Action → Observation step.").parse_args()
    world = load(args)

    for question in queries_from(args, world):
        print("=" * 72)
        trace = run_one(question, world, args, max_steps=1)
        print(format_step_cycle(trace))
        print()

    print("=" * 72)
    print("Tras la observación, el agente decide: ¿otro ciclo o la respuesta final?")
    print("Eso es el bucle de 03_react_loop.py.")


if __name__ == "__main__":
    main()
