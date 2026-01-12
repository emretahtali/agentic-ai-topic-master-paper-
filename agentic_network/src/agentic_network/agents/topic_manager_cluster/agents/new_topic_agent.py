from langchain_core.runnables import Runnable

from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import create_topic
from agentic_network.utils import BaseAgent


class NewTopicAgent(BaseAgent):
    agent: Runnable

    # ---- Internal Methods --------------------------------------------------------
    def _get_node(self, agent_state: TopicManagerState) -> dict:
        # print("[NewTopicAgent] Running agent...")
        # print("[NewTopicAgent] New topic is created.")
        new_topic = create_topic(agent_state)

        return {
            "topic_stack": [new_topic],
            "topic_selected": True
        }
