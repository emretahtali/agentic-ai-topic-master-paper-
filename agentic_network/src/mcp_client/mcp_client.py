from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import find_dotenv, load_dotenv
from typing import Optional
import os


class MCPClient:
    mcp_tools: Optional[list]

    async def initialize(self):
        await self._initialize_client()

    def get_tools(self) -> list:
        if self.mcp_tools is None:
            print("MCP client is not initialized.")
            exit()

        return self.mcp_tools

    async def _initialize_client(self):
        load_dotenv(find_dotenv())
        mcp_server_endpoint = os.getenv("MCP_SERVER_ENDPOINT").strip()

        mcp_server_configs = {
            "mcp_tools_server": {
                "url": mcp_server_endpoint,
                "transport": "stdio"
            }
        }

        try:
            client = MultiServerMCPClient(connections=mcp_server_configs)

            self.mcp_tools = await client.get_tools()

            print(f"✅ Successfully fetched a total of {len(self.mcp_tools)} tools from all servers:")
            for tool in self.mcp_tools:
                print(f"  - {tool.name}: {tool.description}")

        except Exception as e:
            print(f"❌ MCP Client: Failed to connect or fetch tools.")
            exit()


# MCP Client Singleton
mcp_client = MCPClient()
