import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from loguru import logger
from typing import Optional


class MCPClient:
    toolset: Optional[list]

    def __init__(self, port: str, label: str):
        self.port = port
        self.label = label

    async def initialize(self):
        await self._initialize_client()

    def get_tools(self) -> list:
        if self.toolset is None:
            logger.warning(f"[{self.label}] MCP client does not have toolset.")
            return []

        return self.toolset

    async def _initialize_client(self):
        # TODO: Fallback url
        mcp_server_endpoint = os.getenv(f"{self.label.upper()}_ENDPOINT", "")

        logger.info(f"[{self.label}] Connecting to MCP server on:", mcp_server_endpoint)

        mcp_server_configs = {
            "mcp_tools_server": {
                "url": mcp_server_endpoint,
                "transport": "stdio"
            }
        }

        try:
            client = MultiServerMCPClient(connections=mcp_server_configs)

            self.toolset = await client.get_tools()

            logger.info(f"[{self.label}] Successfully fetched a total of {len(self.toolset)} tools from server")

        except Exception as e:
            logger.error(f"[{self.label}]MCP Client: Failed to connect or fetch tools: {e}")
            exit(1)
