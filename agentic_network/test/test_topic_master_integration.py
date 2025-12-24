from langchain_core.messages import HumanMessage

from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.topic_manager_cluster import TopicManagerCluster
from agentic_network.core import AgentState


def main():
    agent_state = AgentState(
        topic_master_state=None,
        messages=[],
        active_agent=None
    )
    topic_master_state = TopicManagerState(
        agentic_state=agent_state,
        current_message=None,
        topic_stack=[],
        disclosed_topics=[],
        topic_selected=False,
    )
    agent_state["topic_master_state"] = topic_master_state

    while True:
        message = input("Enter message: ")
        topic_master_cluster = TopicManagerCluster()
        topic_master_state["current_message"] = HumanMessage(message)

        agent_state = topic_master_cluster(agent_state)


if __name__ == "__main__":
    main()
