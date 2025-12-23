from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Optional, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import AnyMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    agent_outcome: Optional[Union[AgentAction, AgentFinish, None]]