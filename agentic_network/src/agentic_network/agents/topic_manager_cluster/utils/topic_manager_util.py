from typing import Optional, Literal, Iterable
from uuid import uuid4

from agentic_network.agents import AgentData
from agentic_network.agents.topic_manager_cluster.core.topic_manager_state import TopicState
from agentic_network.core import AgentState
from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
)


# ----- Helpers -----
def _new_id() -> str:
    return str(uuid4())


# ----- API -----
def strip_quotes(s: str) -> str:
    while len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        s = s[1:-1]
    return s


def strip_braces(s: str) -> str:
    s = s.strip()

    if s.startswith("{"):
        if s.endswith("}"): s =  s[1:-1].strip()
        else: s = s[1:].strip()
    elif s.endswith("}"): s = s[:-1].strip()

    if s.startswith("["):
        if s.endswith("]"): s =  s[1:-1].strip()
        else: s = s[1:].strip()
    elif s.endswith("]"): s = s[:-1].strip()

    return s


def find_topic_index(topic_id: str, topic_stack: list[TopicState]) -> int:
    topic_id = strip_quotes(topic_id)
    for i, topic in enumerate(topic_stack):
        if topic["id"] == topic_id:
            return i
    return -1


def get_current_topic(agent_state: TopicManagerState) -> Optional[TopicState]:
    topic_stack = agent_state["topic_stack"]
    if not topic_stack: return None
    return topic_stack[-1]


# TODO: we should also populate the person data
def create_topic(state: TopicManagerState) -> TopicState:
    """
    Create a Topic and push it to the top of topic_stack.
    Returns a patch suitable for LangGraph (no in-place mutation).
    """
    # topic: Topic = {
    #     "id": _new_id(),
    #     "agent": agent,
    #     "person_data": {
    #         "name": "",
    #         "symptoms": [],
    #         "appointment_data": {
    #             "hospital_name": "",
    #             "doctor_name": "",
    #             "clinic": "",
    #             "date": "",
    #             "time": "",
    #         },
    #     },
    # }
    return {
        "id": _new_id(),
        "messages": [],
        "agent": None,
    }


def disclose_current_topic(state: AgentState) -> AgentState:
    """
    Move the top topic from topic_stack to disclosed_topics.
    If topic_id is None, pops the top of the stack.
    No-ops if not found.
    """
    stack = list(state.get("topic_stack") or [])
    disclosed = list(state.get("disclosed_topics") or [])

    if not stack: return {}

    idx = len(stack) - 1

    topic = stack[idx]
    new_stack = stack[:idx]
    new_disclosed = disclosed + [topic]

    return {
        "topic_stack": new_stack,
        "disclosed_topics": new_disclosed,
    }


def resurface_topic(state: TopicManagerState, topic_id: str) -> dict:
    """
    Find a topic by id in either topic_stack or disclosed_topics,
    and bring it to the top of topic_stack. Removes it from wherever it was.
    No-op if not found anywhere.
    """
    topic_stack = state.get("topic_stack") or []
    disclosed = list(state.get("disclosed_topics") or [])

    # 1) Try stack first: move to top if present
    idx = find_topic_index(topic_id, topic_stack)
    if idx != -1:
        topic = topic_stack[idx]
        new_stack = topic_stack[:idx] + topic_stack[idx + 1:] + [topic]

        return {
            "topic_stack": new_stack
        }

    # 2) Else try disclosed: remove from disclosed and push onto stack
    d_idx = find_topic_index(topic_id, disclosed)
    if d_idx != -1:
        topic = disclosed[d_idx]
        new_disclosed = disclosed[:d_idx] + disclosed[d_idx + 1:]
        new_stack = topic_stack + [topic]
        return {
            "topic_stack": new_stack,
            "disclosed_topics": new_disclosed,
        }

    # 3) Not found anywhere → no-op
    return {}


def embed_topic_id_to_message(msg: AnyMessage, topic_id: str | None) -> AnyMessage:
    """Return a copy of msg with metadata['topic_id']=topic_id."""
    meta = dict(getattr(msg, "metadata", {}) or {})
    meta["topic_id"] = topic_id

    try:
        # pydantic models support .copy(update=...)
        return msg.model_copy(update={"metadata": meta})

    except Exception:
        # fallback for dataclass-like messages
        return msg.__class__(content=msg.content, metadata=meta)


# def add_message_to_dialogue(state: AgentState, message: AnyMessage) -> dict:
#     stack = state.get("topic_stack") or []
#     topic_id = stack[-1]["id"] if stack else None
#
#     if topic_id is None:
#         raise RuntimeError("Topic Stack is somehow empty.")
#
#     msg = embed_topic_id_to_message(message, topic_id)
#     return {"all_dialog": [msg]}


def get_messages_for_topic(state: AgentState, topic_id: str) -> list[AnyMessage]:
    return [
        m for m in state.get("all_dialog", [])
        if (getattr(m, "metadata", {}) or {}).get("topic_id") == topic_id
    ]


def get_messages_for_current_topic(state: AgentState) -> list[AnyMessage]:
    stack = state.get("topic_stack") or []
    topic_id = stack[-1]["id"] if stack else None

    if topic_id is None:
        raise RuntimeError("Topic Stack is somehow empty.")

    return get_messages_for_topic(state, topic_id)


def _role_of(msg: AnyMessage) -> str:
    # "human" -> "user" for friendlier logs
    t = getattr(msg, "type", "") or msg.__class__.__name__.lower()
    return "user" if t == "human" else "assistant" if t == "ai" else t

def _content_str(msg: AnyMessage) -> str:
    c = getattr(msg, "content", "")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        # multimodal content: try to extract text parts
        parts = []
        for item in c:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(c)

def format_dialog_with_topics(messages: Iterable[AnyMessage]) -> str:
    """Format messages as lines that include [topic:<id>] when present."""
    lines = []
    for m in messages:
        topic_id = (getattr(m, "metadata", {}) or {}).get("topic_id")
        topic_tag = f"[topic:{topic_id}] " if topic_id else ""
        lines.append(f"{topic_tag}{_role_of(m)}: {_content_str(m)}")
    return "\n".join(lines)


def format_dialog_to_json(messages: Iterable[AnyMessage]) -> list:
    return [format_message_to_json(message) for message in messages]


def format_message_to_json(message: AnyMessage) -> dict:
    return {"role": _role_of(message), "content": [{"type": "text", "text": message.content}]}


def format_dialog(messages: Iterable[AnyMessage]) -> str:
    """Format messages as lines without topic IDs."""
    return "\n".join(f"{_role_of(m)}: {_content_str(m)}" for m in messages)


# def redirect_to_appointment_agent(agent_state: AgentState):
#     get_current_topic(agent_state)["agent"] = GraphRoutes.APPOINTMENT_AGENT

# tests:
# messages = [add_topic_id_to_message(HumanMessage("hello!"), "12341235245"), HumanMessage("lets go!")]
# print(format_dialog_with_topics(messages))
