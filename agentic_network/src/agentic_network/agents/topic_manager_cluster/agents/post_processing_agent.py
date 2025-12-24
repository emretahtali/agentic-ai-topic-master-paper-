from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import embed_topic_id_to_message, \
    get_current_topic
from agentic_network.utils import BaseAgent


class TopicManagerPostProcessingAgent(BaseAgent):
    def _get_node(self, agent_state: TopicManagerState) -> dict:
        current_topic = get_current_topic(agent_state)
        current_topic_id = current_topic["id"]

        id_embedded_message = embed_topic_id_to_message(agent_state["current_message"], current_topic_id)
        get_current_topic(agent_state)["messages"].append(id_embedded_message)
        # print(f"[PostProcessing] current_message={id_embedded_message}")

        return {
            "current_message": id_embedded_message,
        }
