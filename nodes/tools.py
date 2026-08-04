from langgraph.prebuilt import ToolNode

from mcp_client import get_tools


async def create_tool_node():

    tools = await get_tools()

    print("\n====== Loaded MCP Tools ======")

    for tool in tools:

        print(tool.name)

    print("==============================")

    return ToolNode(tools)