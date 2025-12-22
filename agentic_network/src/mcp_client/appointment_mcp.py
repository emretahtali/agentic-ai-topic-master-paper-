from dotenv import load_dotenv,find_dotenv
from os import getenv

from .util import MCPClient

load_dotenv(find_dotenv())
mcp_port = getenv("APPOINTMENT_SERVER_PORT", 8081)

appointment_mcp = MCPClient(mcp_port, "appointment tools mcp client")
