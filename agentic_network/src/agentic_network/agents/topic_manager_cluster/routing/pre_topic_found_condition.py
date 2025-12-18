import uuid

from agentic_network.core import AgentState
from agentic_network.agents.topic_manager_cluster.core import TopicManagerRoutes
from agentic_network.agents.topic_manager_cluster.routing.condition_util import strip_braces, clean_thoughts
from agentic_network.core.topic_manager_util import find_topic_index, resurface_topic


def _is_valid_uuid(value, version=4):
    try:
        uuid_obj = uuid.UUID(value, version=version)

    except ValueError:
        return False

    return str(uuid_obj) == value.lower()


def decide_pre_topic_found(agent_state: AgentState) -> TopicManagerRoutes:
    """Parses:
       - FINAL ANSWER: [topic_id]
       - FINAL ANSWER: NEW TOPIC
       - THOUGHT: anything...
   """
    print("-decide: PRE TOPIC FOUND CONDITION-")

    ai_message = agent_state["all_dialog"][-1].content.upper()  # TODO: this should change to thought dialog

    if "FINAL ANSWER" in ai_message:
        if "NEW" in ai_message:
            print("-this is a new topic, redirect to: NEW_TOPIC_AGENT")
            clean_thoughts(agent_state)
            return TopicManagerRoutes.NEW_TOPIC_AGENT

        else:
            topic_id = ai_message.split("FINAL ANSWER:")[1].strip()
            topic_id = strip_braces(topic_id)
            topic_id = topic_id.lower()

            if not _is_valid_uuid(topic_id):
                print("-the topic id is not a valid uuid, redirect to: PRE_TOPICS_AGENT")
                return TopicManagerRoutes.PRE_TOPICS_AGENT  # TODO: add the thought that the topic_id is not a valid uuid

            if find_topic_index(agent_state, topic_id):
                print("-the topic id could not be found in the topic stack, redirect to: PRE_TOPICS_AGENT")
                return TopicManagerRoutes.PRE_TOPICS_AGENT  # TODO: add the thought that the topic_id cannot be found

            print("-this is an older topic, redirect to: END")
            resurface_topic(agent_state, topic_id)
            clean_thoughts(agent_state)
            return TopicManagerRoutes.END

    print("-final answer is malformed, redirect to: PRE_TOPICS_AGENT")
    return TopicManagerRoutes.PRE_TOPICS_AGENT
