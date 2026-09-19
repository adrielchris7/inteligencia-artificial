"""CLI helpers shared by the four programs."""

from __future__ import annotations

import argparse
from pathlib import Path

from react.brain import GeminiBrain
from react.data import World, load_world
from react.loop import Trace, run_react
from react.tools import Tool, build_tools

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = ROOT / "data" / "viaje.yaml"


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="YAML world")
    parser.add_argument("--query", type=str, default=None, help="Ask your own question")
    parser.add_argument("--all", action="store_true", help="Run every example query in the YAML")
    parser.add_argument("--max-steps", type=int, default=None, dest="max_steps", help="Loop cap")
    return parser


def load(args: argparse.Namespace) -> World:
    return load_world(args.data)


def tools_for(world: World) -> tuple[Tool, ...]:
    return build_tools(world)


def brain_for(world: World, *, use_tools: bool = True) -> GeminiBrain:
    del world, use_tools  # tools vs CoT is decided by which tools we pass
    return GeminiBrain()


def max_steps_from(args: argparse.Namespace, world: World) -> int:
    return args.max_steps if args.max_steps is not None else world.max_steps


def queries_from(args: argparse.Namespace, world: World) -> list[str]:
    if args.query:
        return [args.query]
    if args.all:
        return list(world.queries)
    if world.queries:
        return [world.queries[0]]
    raise SystemExit("No query: pass --query or add queries: in the YAML.")


def run_one(
    question: str,
    world: World,
    args: argparse.Namespace,
    *,
    use_tools: bool = True,
    max_steps: int | None = None,
) -> Trace:
    steps = max_steps if max_steps is not None else max_steps_from(args, world)
    tools = tools_for(world) if use_tools else ()
    return run_react(question, tools, brain_for(world, use_tools=use_tools), steps)
