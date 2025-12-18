from langchain_core.agents import AgentFinish
from typing import Literal

from agentic_network.core import AgentState


def decide_tools(state: AgentState) -> Literal["end", "tools"]:
    if isinstance(state["agent_outcome"], AgentFinish):
        return "end"

    # If it's not AgentFinish, it must be an AgentAction,
    # which by definition contains a tool call.
    return "tools"
