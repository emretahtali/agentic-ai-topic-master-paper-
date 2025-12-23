from agentic_network.utils import BaseAgent
from agentic_network.core import AgentState


class PreProcessingAgent(BaseAgent):
    async def _get_node(self, agent_state: AgentState) -> dict:
        return {}
