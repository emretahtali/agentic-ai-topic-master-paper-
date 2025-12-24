from langchain_core.messages import HumanMessage

from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.topic_manager_cluster import TopicManagerCluster
from agentic_network.core import AgentState
from benchmark.core import ResultInfo


class TopicMasterBenchmarkWrapper:
    graph_state: AgentState
    topic_master_state: TopicManagerState

    def __init__(self):
        self.graph_state = AgentState(
            topic_master_state=None,
            messages=[],
            active_agent=None
        )
        self.topic_master_state = TopicManagerState(
            agentic_state=self.graph_state,
            current_message=None,
            topic_stack=[],
            disclosed_topics=[],
            topic_selected=False,
        )
        self.graph_state["topic_master_state"] = self.topic_master_state

    def invoke(self, message: str):
        topic_master_cluster = TopicManagerCluster()
        self.topic_master_state["current_message"] = HumanMessage(message)

        self.graph_state = topic_master_cluster(self.graph_state)
        self.topic_master_state = self.graph_state.get("topic_master_state")
        self.topic_master_state["agentic_state"] = self.graph_state

        current_agent = self.graph_state.get("active_agent")
        return {
            "structured_output": ResultInfo(extracted_intent=current_agent)
        }
