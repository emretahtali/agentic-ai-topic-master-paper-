from typing import Literal

from langchain_core.tools import tool

from agentic_network.agents import DiagnosisAgent

class NewTopicTools:
    agents = Literal["DIAGNOSIS_AGENT"]
    agent_names = {
        "DIAGNOSIS_AGENT": DiagnosisAgent,
    }

    @staticmethod
    @tool
    def select_agent(agent: agents):
        """Select a new agent."""
        pass

    def get_tools(self):
        return [
            self.select_agent,
        ]
