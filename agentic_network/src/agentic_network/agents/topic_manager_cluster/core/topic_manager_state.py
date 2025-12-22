from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Optional, Union
from langchain_core.messages import AnyMessage

from agentic_network.agents import AgentData

class TopicState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    agent: AgentData.agent_literals

class TopicManagerState(TypedDict):
    current_message: Optional[AnyMessage]
    topic_stack: list[TopicState]
    topic_selected: bool
