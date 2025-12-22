"""
A class-based FastAPI server for a LangGraph-powered agent network.

Features:
- Checkpointing (server-owned dialog state) via SqliteSaver by default.
- thread_id (configurable -> thread-bound state).
- client_turn_id (idempotency per turn).
- HTTP /invoke (one-shot) and WS /stream (streaming) endpoints.
- MCP client initialization on startup.
- No module-level global state (everything encapsulated in classes + app.state).
"""

from dotenv import load_dotenv, find_dotenv
import os, uvicorn

from fastapi_server import AssistantService, APIServer


def main() -> None:
    """
    Server runner main method.
    Run with:  poetry run python server_main.py
    """
    load_dotenv(find_dotenv())
    api_key = os.getenv("AGENTIC_SERVER_API_KEY", "dev-key").strip()
    checkpointer_mode = os.getenv("CHECKPOINTER", "memory").strip()  # "sqlite" or "memory"
    # sqlite_path = os.getenv("SQLITE_PATH", "checkpoints.db")
    sqlite_path = "checkpoints.db"

    service = AssistantService(
        checkpointer_mode=checkpointer_mode,
        sqlite_path=sqlite_path,
    )
    server = APIServer(service=service, api_key=api_key)

    server_host = os.getenv("AGENTIC_SERVER_HOST", "0.0.0.0").strip()
    server_port = int(os.getenv("AGENTIC_SERVER_PORT", "8082").strip())
    uvicorn.run(server.app, host=server_host, port=server_port)


if __name__ == "__main__":
    main()
