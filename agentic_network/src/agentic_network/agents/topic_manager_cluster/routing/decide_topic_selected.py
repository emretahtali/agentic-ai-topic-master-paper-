from agentic_network.agents.topic_manager_cluster.core import TopicManagerState, TopicManagerRoutes


def is_topic_selected(state: TopicManagerState) -> TopicManagerRoutes:
    return TopicManagerRoutes.END if state.get("topic_selected") else TopicManagerRoutes.NEXT
