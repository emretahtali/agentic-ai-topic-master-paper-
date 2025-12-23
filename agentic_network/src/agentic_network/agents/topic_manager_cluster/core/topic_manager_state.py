from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Optional, Union
from langchain_core.messages import AnyMessage

from agentic_network.agents import AgentData
from agentic_network.core import AgentState


class TopicState(TypedDict):
    id: str
    messages: Annotated[list[AnyMessage], add_messages]
    agent: AgentData.agent_literals

class TopicManagerState(TypedDict):
    agentic_state: AgentState
    current_message: Optional[AnyMessage]
    topic_stack: list[TopicState]
    disclosed_topics: list[TopicState]
    topic_selected: bool
