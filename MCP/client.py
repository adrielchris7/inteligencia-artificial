"""Call the local FastMCP server in-process (no extra process, no HTTP)."""

import asyncio

from fastmcp import Client

from server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("tools:", [tool.name for tool in tools])

        greeting = await client.call_tool("greet", {"name": "Ada"})
        print("greet:", greeting.data)

        total = await client.call_tool("add", {"a": 17, "b": 25})
        print("add:", total.data)

        info = await client.read_resource("info://server")
        print("resource:", info[0].text)

        prompt = await client.get_prompt("explain", {"topic": "MCP"})
        print("prompt:", prompt.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())
