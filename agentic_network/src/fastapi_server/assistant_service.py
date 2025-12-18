from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.agents import AgentFinish
from fastapi import HTTPException
from typing import Any, Dict, Optional, Literal
import uuid, asyncio

from agentic_network.agent_graph import AgentGraph
from agentic_network.core import AgentState
from mcp_client import mcp_client


class AssistantService:
    """
    Encapsulates:
      - MCP initialization
      - Graph building/compilation (with checkpointer)
      - Idempotency cache (dev)
      - Invoke + Stream operations
    """

    def __init__(
        self,
        checkpointer_mode: str = "memory",  # "sqlite", "memory"
        sqlite_path: str = "checkpoints.db",
    ):
        self.checkpointer_mode = checkpointer_mode
        self.sqlite_path = sqlite_path

        self.graph = None
        self.dialogs: Dict[str, Dict[str, Dict[str, Any]]] = {}  # cache: {thread_id: {client_turn_id: response}}
        self.state_cache: Dict[str, AgentState] = {}  # cache: {thread_id: AgentState}
        self.dialog_lock = asyncio.Lock()
        self.state_cache_lock = asyncio.Lock()

    # ---------- lifecycle ----------

    async def startup(self) -> None:
        """Initialize backends and build the graph once per process."""

        print("[startup] Initializing MCP client…")
        await mcp_client.initialize()

        print("[startup] Building/compiling LangGraph…")
        checkpointer = self._make_checkpointer()
        self.graph = AgentGraph(checkpointer=checkpointer).get_graph()

    def _make_checkpointer(self):
        """Chooses a checkpointer for state durability."""
        # if self.checkpointer_mode == "sqlite":
        #     # Default: SQLite file (no external DB; survives restarts; single writer is safest)
        #     return SqliteSaver.from_conn_string(self.sqlite_path)

        # Ephemeral (single-worker dev only)
        return MemorySaver()

    # ---------- helpers ----------

    @staticmethod
    def _extract_user_text(payload: Dict[str, Any]) -> Optional[str]:
        """
        Accept only:
          {"message": "..."}
        """
        if not payload: return None

        if "message" in payload and isinstance(payload["message"], str):
            return payload["message"]

        return None

    @staticmethod
    def _last_ai_text(messages: Any) -> Optional[str]:
        """Convenience: return last AI message content if present."""
        if not isinstance(messages, list):
            return None

        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                return str(msg.content)

            if isinstance(msg, BaseMessage) and getattr(msg, "type", "") == "ai":
                return str(getattr(msg, "content", ""))

            if isinstance(msg, dict) and msg.get("role") == "assistant":
                return str(msg.get("content") or "")

        return None

    # ---------- API operations ----------

    async def invoke(
        self,
        thread_id: str,
        input_payload: Dict[str, Any],
        client_turn_id: Optional[str],
    ) -> Dict[str, Any]:

        """Run a single turn (non-streaming); return full state (and a convenience final_text)."""
        if self.graph is None:
            raise RuntimeError("Graph not initialized")

        # Caching
        agent_state: AgentState
        turn_id = client_turn_id or str(uuid.uuid4())

        async with self.dialog_lock:
            self.dialogs.setdefault(thread_id, {})
            if turn_id in self.dialogs[thread_id]:
                return self.dialogs[thread_id][turn_id]

        async with self.state_cache_lock:
            self.state_cache.setdefault(thread_id, AgentState(messages=[], intermediate_steps=[], agent_outcome=None))
            agent_state = self.state_cache[thread_id]

        user_text = self._extract_user_text(input_payload)
        if not user_text:
            raise HTTPException(400, "input.message is not provided")

        config = {"configurable": {"thread_id": thread_id}}
        agent_state["messages"].append(HumanMessage(content=user_text))
        agent_state["intermediate_steps"].clear()
        agent_state["agent_outcome"] = None

        print("\n---USER MESSAGE---")
        print(user_text)

        # Pass only the new user message.
        result_state = await self.graph.ainvoke(
            agent_state,
            config=config,
        )

        # Try to surface the final assistant text
        agent_finish: AgentFinish = result_state.get("agent_outcome", {})
        final_text = agent_finish.return_values.get("output", {})
        resp = {"response": final_text}

        # Caching back
        async with self.state_cache_lock:
            self.state_cache[thread_id] = result_state
        async with self.dialog_lock:
            self.dialogs[thread_id][turn_id] = resp

        return resp

    async def stream(self, *, thread_id: str, user_text: str):
        """
        Async generator of LangGraph events for streaming.
        Yields dict events (LangGraph v2 schema), then ends.
        """
        if self.graph is None:
            raise RuntimeError("Graph not initialized")

        config = {"configurable": {"thread_id": thread_id}}

        async for event in self.graph.astream_events(
            {"messages": [HumanMessage(content=user_text)]},
            config=config,
            version="v2",
        ):
            yield event
