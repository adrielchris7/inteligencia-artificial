#!/usr/bin/env python3
"""Program 3: the full ReAct loop until Final Answer.

Stage 3 of ReAct. Repeat Thought → Action → Observation. After each
observation the agent either calls another tool or stops with a Final
Answer. `max_steps` (YAML or --max-steps) is the safety cap from the lecture.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from react.cli import build_parser, load, queries_from, run_one  # noqa: E402
from react.format import format_trace  # noqa: E402


def main() -> None:
    args = build_parser("Run the ReAct loop until Final Answer or max_steps.").parse_args()
    world = load(args)

    for question in queries_from(args, world):
        print("=" * 72)
        trace = run_one(question, world, args)
        print(format_trace(trace))
        print()

    print("=" * 72)
    print("ReAct = razonar + actuar + observar, y parar cuando ya se puede responder.")
    print("Sin --query corre la primera pregunta; --all corre todas las del YAML.")


if __name__ == "__main__":
    main()
