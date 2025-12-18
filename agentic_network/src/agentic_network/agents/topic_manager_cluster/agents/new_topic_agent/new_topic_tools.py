from typing import Literal

from langchain_core.tools import tool

from agentic_network.agents import DiagnosisAgent, PreProcessingAgent, PostProcessingAgent

agents = Literal["DiagnosisAgent"]
agent_names = {
    "DiagnosisAgent": DiagnosisAgent,
}

class NewTopicTools:
    @staticmethod
    @tool
    def select_agent(agent: agents):
        pass

    def get_tools(self):
        return [
            self.select_agent,
        ]
