# test_tools.py
import asyncio
from mcp_client import get_tools


async def main():
    print("Connecting to MCP servers and discovering tools...")
    tools = await get_tools()
    print(f"\nSuccessfully loaded {len(tools)} tools:")
    for tool in tools:
        print(f" - {tool.name}: {tool.description}")


if __name__ == "__main__":
    asyncio.run(main())