from langchain_core.messages import SystemMessage

from model import get_llm
from prompts import SYSTEM_PROMPT
from mcp_client import get_tools


_bound_model = None


async def get_agent():

    global _bound_model

    if _bound_model:

        return _bound_model

    llm = get_llm()

    tools = await get_tools()

    try:

        llm = llm.bind_tools(tools)

    except Exception:

        pass

    _bound_model = llm

    return _bound_model

async def agent_node(state):
    """
    Main AI Agent.

    Responsibilities:
    1. Read conversation history.
    2. Decide whether clarification is needed.
    3. Decide which MCP tool(s) to call.
    4. Produce the final answer after tool execution.
    """

    llm = await get_agent()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = await llm.ainvoke(messages)

    print("\n===== LLM Response =====")

    print(response)

    if hasattr(response, "tool_calls"):
        print("\nTool Calls:")
        for call in response.tool_calls:
            print(call)

    return {
        "messages": [response]
    }