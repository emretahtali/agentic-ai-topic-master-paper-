from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.utils import BaseAgent


class TopicManagerPostProcessingAgent(BaseAgent):
    async def _get_node(self, agent_state: TopicManagerState) -> dict:
        return {}