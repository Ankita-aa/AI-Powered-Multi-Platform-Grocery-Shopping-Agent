# get_my_address.py
import asyncio
from mcp_client import get_mcp_client


async def main():
    client = await get_mcp_client()

    # Call get_addresses tool directly from Swiggy
    tools = await client.get_tools()
    address_tool = next(t for t in tools if t.name == "get_addresses")

    result = await address_tool.ainvoke({})
    print("Your Swiggy Addresses:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())