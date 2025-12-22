from dotenv import load_dotenv,find_dotenv
from os import getenv
import asyncio

from mcp_client.util import MCPClient

load_dotenv(find_dotenv())
mcp_port = getenv("APPOINTMENT_SERVER_PORT", 8081)

appointment_mcp = MCPClient(mcp_port, "appointment_server")


async def test():
    await appointment_mcp.initialize()

    print(appointment_mcp.get_tools())

if __name__ == "__main__":
    asyncio.run(test())