from mcp.server.fastmcp.prompts.base import UserMessage

from fastapi_server import server_main
from dotenv import load_dotenv, find_dotenv

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    # server_main.main()

