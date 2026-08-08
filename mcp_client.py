import os
import sys
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

_client = None
_tools = None


async def get_mcp_client():
    """Creates the MCP client singleton."""
    global _client

    if _client is not None:
        return _client

    # Retrieve token at instantiation time
    swiggy_token = os.getenv("SWIGGY_ACCESS_TOKEN")
    if not swiggy_token:
        raise ValueError(
            "SWIGGY_ACCESS_TOKEN is missing in your .env file. "
            "Please run your token generation script first."
        )

    _client = MultiServerMCPClient(
        {
            # 1. Local Zepto Scraper Server
            "zepto": {
                "transport": "stdio",
                "command": sys.executable,  # Uses venv python interpreter
                "args": [
                    r"E:\my_project_work\zepto_swiggy_mcp\price_tracker_advance\server.py"
                ],
            },
            # 2. Official Swiggy Instamart SSE Server
            "swiggy_instamart": {
                "transport": "http",
                "url": "https://mcp.swiggy.com/im",
                "headers": {"Authorization": f"Bearer {swiggy_token}"},
            },
        }
    )

    return _client


async def get_tools():
    """Fetches and caches combined tools from all MCP servers."""
    global _tools

    if _tools is not None:
        return _tools

    try:
        client = await get_mcp_client()
        _tools = await client.get_tools()
        return _tools
    except Exception as ex:
        raise RuntimeError(f"Unable to connect to MCP Servers: {ex}")