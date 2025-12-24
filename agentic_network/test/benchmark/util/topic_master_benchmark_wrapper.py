from langchain_core.messages import HumanMessage, AIMessage

from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.topic_manager_cluster import TopicManagerCluster
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import get_current_topic, \
    embed_topic_id_to_message
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
        print(f"selected_intent: {current_agent}")
        return {
            "structured_response": ResultInfo(extracted_intent=current_agent)
        }

    def add_ai_message(self, message: str):
        # print("add_ai_message")
        current_topic = get_current_topic(self.topic_master_state)
        current_topic_id = current_topic["id"]
        ai_message = embed_topic_id_to_message(AIMessage(message), current_topic_id)
        # print(f"{self.graph_state["messages"]=}")
        self.graph_state["messages"].append(ai_message)
        # print(f"{current_topic["messages"]=}")
        current_topic["messages"].append(ai_message)

        self.graph_state["topic_master_state"] = self.topic_master_state
        self.topic_master_state["agentic_state"] = self.graph_state
        self.graph_state["topic_master_state"] = self.topic_master_state
        self.topic_master_state["agentic_state"] = self.graph_state
