from __future__ import annotations

from agentic_network.agents.diagnosis import system_msg
from agentic_network.core import AgentState
from agentic_network.agents.agent import Agent
from llm import diagnosis_llm
from mcp_client import diagnosis_mcp


class DiagnosisAgent(Agent):

    def __init__(self):
        self.tools = diagnosis_mcp.get_tools()
        self.model = diagnosis_llm.bind_tools(self.tools)

    async def _get_node(self, state: AgentState) -> dict:

        messages = state["messages"]

        # call model
        response = self.model.invoke([system_msg] + messages)

        # return back the appointment data to llm
        return {"messages": [response], "active_agent": "diagnosis_agent"}

