from agentic_network.core import AgentState
from agentic_network.agents.topic_manager_cluster.core import TopicManagerRoutes
from agentic_network.agents.topic_manager_cluster.routing.condition_util import clean_thoughts


def decide_topic_has_changed(agent_state: AgentState) -> TopicManagerRoutes:
    """Parses:
       - FINAL ANSWER: SAME TOPIC
       - FINAL ANSWER: DIFFERENT TOPIC
       - THOUGHT: anything...
   """

    print("-decide: TOPIC CHANGED CONDITION-")

    if len(agent_state["thoughts"]) == 0:
        print("-there are no prior thoughts, redirect to: TOPIC_CHANGE_CHECKER_AGENT")
        return TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT  # TODO: we can make this a bit better later

    ai_message = agent_state["thoughts"][-1].content.upper()

    if "FINAL ANSWER" in ai_message:
        if "SAME" in ai_message:
            print("-same topic, redirect to: END")
            clean_thoughts(agent_state)
            return TopicManagerRoutes.END

        elif "DIFFERENT" in ai_message:
            print("-different topic, redirect to: PRE_TOPICS_AGENT")
            clean_thoughts(agent_state)
            return TopicManagerRoutes.PRE_TOPICS_AGENT

    print("-final message malformed, redirect to: TOPIC_CHANGE_CHECKER_AGENT")
    return TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT
