#!/usr/bin/env python3
"""Program 4: chain-of-thought alone vs ReAct with tools.

Stage 4 of ReAct. The same questions, twice: Gemini with no tools (CoT
from its own knowledge — often wrong about this toy world), then ReAct,
which looks things up. The gap is the lecture point: CoT + external
evidence beats CoT alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from react.cli import build_parser, load, queries_from, run_one  # noqa: E402
from react.format import format_trace  # noqa: E402


def main() -> None:
    args = build_parser("Compare CoT (no tools) with ReAct (tools).").parse_args()
    world = load(args)

    for question in queries_from(args, world):
        print("=" * 72)
        print(f"Pregunta: {question}\n")

        cot = run_one(question, world, args, use_tools=False, max_steps=1)
        react = run_one(question, world, args)

        print(format_trace(cot, title="1) Solo chain-of-thought (sin tools)"))
        print()
        print(format_trace(react, title="2) ReAct (tools + observaciones)"))
        print()

    print("=" * 72)
    print("El razonamiento verbalizado es el mismo formato; la diferencia es consultar el entorno.")


if __name__ == "__main__":
    main()
