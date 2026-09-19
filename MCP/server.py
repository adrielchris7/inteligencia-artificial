"""Minimal FastMCP server: tools, a resource, and a prompt."""

from fastmcp import FastMCP

mcp = FastMCP("Demo")


@mcp.tool
def greet(name: str) -> str:
    """Saluda a una persona por su nombre."""
    return f"Hola, {name}!"


@mcp.tool
def add(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b


@mcp.resource("info://server")
def server_info() -> str:
    """Datos de solo lectura sobre este servidor."""
    return "Servidor MCP de demostración (FastMCP). Tools: greet, add."


@mcp.prompt
def explain(topic: str) -> str:
    """Plantilla de mensaje para pedir una explicación breve."""
    return f"Explica en una frase qué es {topic}."


if __name__ == "__main__":
    mcp.run()
