from operator import add

from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Optional
from langchain_core.messages import AnyMessage

from agentic_network.agents import AgentData


class TopicState(TypedDict):
    id: str
    messages: Annotated[list[AnyMessage], add_messages]
    agent: AgentData.agent_literals

class TopicManagerState(TypedDict):
    agentic_state: TypedDict
    current_message: Optional[AnyMessage]
    topic_stack: Annotated[list[TopicState], add]
    disclosed_topics: list[TopicState]
    topic_selected: bool
