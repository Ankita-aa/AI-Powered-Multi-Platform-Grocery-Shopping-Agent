# from langchain_mcp_adapters.client import MultiServerMCPClient

# _client = None
# _tools = None


# async def get_tools():

#     global _client
#     global _tools

#     if _tools is not None:
#         return _tools

#     _client = MultiServerMCPClient(
#         {
#             "zepto": {
#                 "transport": "stdio",
#                 "command": "npx",
#                 "args": [
#                     "tsx",
#                     r"E:\AgenticAI\grocery-mcp\src\server.ts"
#                 ]
#             }
#         }
#     )

#     _tools = await _client.get_tools()

#     return _tools


from langchain_mcp_adapters.client import MultiServerMCPClient

_client = None
_tools = None


async def get_mcp_client():
    """
    Creates the MCP client only once.
    """

    global _client

    if _client is not None:
        return _client

    _client = MultiServerMCPClient(
        {
            "zepto": {
                "transport": "stdio",
                "command": "npx",
                "args": [
                    "tsx",
                    r"E:\AgenticAI\grocery-mcp\src\server.ts"
                ]
            }
        }
    )

    return _client


async def get_tools():

    global _tools

    if _tools is not None:
        return _tools

    try:

        client = await get_mcp_client()

        _tools = await client.get_tools()

        return _tools

    except Exception as ex:

        raise RuntimeError(
            f"Unable to connect to MCP Server: {ex}"
        )