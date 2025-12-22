from dotenv import load_dotenv,find_dotenv
from os import getenv

from .util import MCPClient

load_dotenv(find_dotenv())
mcp_port = getenv("DIAGNOSIS_SERVER_PORT", 8080)

diagnosis_mcp = MCPClient(mcp_port, "diagnosis_server")
