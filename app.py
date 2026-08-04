import asyncio

from langchain_core.messages import HumanMessage

from graph import create_graph

from nodes.agent import get_agent


async def main():

    print("=" * 60)
    print(" Grocery AI Agent ")
    print("=" * 60)

    # Warm-up: initialize LLM and bind tools
    await get_agent()

    # Compile graph
    graph = await create_graph()

    # Conversation history
    messages = []

    while True:

        query = input("\nYou : ").strip()

        if query.lower() in ["exit", "quit"]:
            break

        messages.append(
            HumanMessage(content=query)
        )

        result = await graph.ainvoke(
            {
                "messages": messages
            }
        )

        messages = result["messages"]

        ai_message = messages[-1]

        print("\nAgent:\n")
        print(ai_message.content)


if __name__ == "__main__":

    asyncio.run(main())