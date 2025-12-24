from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.utils import BaseAgent


class TopicManagerPreProcessingAgent(BaseAgent):
    def _get_node(self, agent_state: TopicManagerState) -> dict:
        return {
            "topic_selected": False,
        }
