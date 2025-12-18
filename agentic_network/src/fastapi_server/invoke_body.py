from typing import Any, Dict, Optional
from pydantic import BaseModel


class InvokeBody(BaseModel):
    """
    Payload for /invoke:
      - thread_id: stable per conversation (server loads/saves state here)
      - input: either {"message": "..."} or {"messages":[{"role":"user","content":"..."}]}
      - client_turn_id: unique per new client message to dedupe retries
    """
    input: Dict[str, Any]
    thread_id: str
    client_turn_id: str
