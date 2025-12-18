from agentic_network.agents import Agent
from agentic_network.core import AgentState


class PreProcessingAgent(Agent):
    async def _get_node(self, agent_state: AgentState) -> dict:
        return {}
