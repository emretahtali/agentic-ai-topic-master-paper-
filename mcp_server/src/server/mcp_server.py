from fastmcp import FastMCP
from dotenv import find_dotenv, load_dotenv
import inspect
from typing import Literal
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from tools import ToolBase


class MCPServer:

    def __init__(self, server_name: str):

        self.server_name = server_name
        self.mcp = FastMCP(name=server_name)

        @self.mcp.custom_route("/health", methods=["GET"])
        async def health_check(request: Request) -> PlainTextResponse:
            return PlainTextResponse("OK")

    def register_tools(self, tool_instances: list[ToolBase]):
        for tool_class in tool_instances:
            for name, method in inspect.getmembers(tool_class, inspect.ismethod):
                if not name.startswith('_'):
                    self.mcp.tool()(method)

    def run(self, transport: Literal["stdio", "http", "sse", "streamable-http"] = "stdio", **kwargs):
        self.mcp.run(transport=transport, **kwargs)


if __name__ == "__main__":
    try:

        SERVER_NAME = "main"
        mcp_server = MCPServer(SERVER_NAME)

        mcp_server.register_tools(tool_instances=[])

        load_dotenv(find_dotenv())
        env_key = f"{SERVER_NAME.upper()}_PORT"
        port = 8080

        print(f"Starting MCP Server '{SERVER_NAME}'")
        mcp_server.run(transport="stdio", host="0.0.0.0", port=port)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)