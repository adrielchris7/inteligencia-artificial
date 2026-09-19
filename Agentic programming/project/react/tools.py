"""External tools the agent may call. Each one is a function with a name."""

from __future__ import annotations

import ast
import operator
from dataclasses import dataclass

from react.data import World

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    run: object  # Callable[[str], str] — kept untyped so the file stays import-light


def calculator(expression: str) -> str:
    """Evaluate a tiny arithmetic expression. No eval(), only + - * / ** % and ()."""
    text = expression.strip().rstrip("=").strip()
    if not text:
        return "Calculator error: empty expression."
    try:
        tree = ast.parse(text, mode="eval")
        value = _eval_ast(tree.body)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        return f"Calculator error: {exc}"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value)


def _eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_eval_ast(node.left), _eval_ast(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval_ast(node.operand))
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    raise ValueError("only numbers and + - * / ** % ( ) are allowed")


def lookup(query: str, world: World) -> str:
    fact = world.lookup(query)
    if fact is None:
        keys = ", ".join(f.key for f in world.facts) or "(none)"
        return f"No fact matched {query!r}. Known keys: {keys}."
    return fact.text


def weather(city: str, world: World) -> str:
    forecast = world.forecast(city)
    if forecast is None:
        cities = ", ".join(item.city for item in world.weather) or "(none)"
        return f"No forecast for {city!r}. Known cities: {cities}."
    return f"{forecast.city}: {forecast.temp} °C, {forecast.summary}."


def build_tools(world: World) -> tuple[Tool, ...]:
    return (
        Tool(
            name="Calculator",
            description="Aritmética. Action Input es una expresión como 17 * 24 + 5.",
            run=calculator,
        ),
        Tool(
            name="Lookup",
            description="Hechos locales (qué hay en el closet, el artículo ReAct, etc.). Action Input es una clave como closet o react. No inventes esos hechos.",
            run=lambda q, _world=world: lookup(q, _world),
        ),
        Tool(
            name="Weather",
            description="Pronóstico de una ciudad del mundo. Action Input es el nombre de la ciudad.",
            run=lambda city, _world=world: weather(city, _world),
        ),
    )


def run_tool(tools: tuple[Tool, ...], name: str, tool_input: str) -> str:
    wanted = name.strip().casefold()
    for tool in tools:
        if tool.name.casefold() == wanted:
            return str(tool.run(tool_input))
    available = ", ".join(t.name for t in tools)
    return f"Unknown tool {name!r}. Available: [{available}]."
