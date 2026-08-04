from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from state import AgentState
from nodes.agent import agent_node
from nodes.tools import create_tool_node


async def create_graph():

    # Create ToolNode from MCP tools
    tool_node = await create_tool_node()

    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)

    # Entry
    builder.add_edge(START, "agent")

    # If LLM generated tool_calls -> tools
    # Otherwise -> END
    builder.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )

    # After tool execution go back to agent
    builder.add_edge("tools", "agent")

    return builder.compile()