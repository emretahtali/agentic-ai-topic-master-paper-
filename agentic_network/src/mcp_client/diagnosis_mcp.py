import asyncio
from dotenv import load_dotenv,find_dotenv
from os import getenv

from mcp_client.util import MCPClient

load_dotenv(find_dotenv())
mcp_port = getenv("DIAGNOSIS_SERVER_PORT", 8080)

diagnosis_mcp = MCPClient(mcp_port, "diagnosis_server")


async def test():

    await diagnosis_mcp.initialize()

    print(diagnosis_mcp.get_tools())

if __name__ == "__main__":
    asyncio.run(test())