from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Optional
from langchain_core.messages import AnyMessage

from agentic_network.agents.agent_data import AgentData


class AgentState(TypedDict):
    topic_master_state: Optional[TypedDict]
    messages: Annotated[list[AnyMessage], add_messages]
    active_agent: Optional[AgentData.agent_literals]
