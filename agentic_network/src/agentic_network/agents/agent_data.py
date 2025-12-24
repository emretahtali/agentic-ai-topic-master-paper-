from typing import Literal

from agentic_network.utils import get_class_field_values


class AgentData:
    class Agents:
        diagnosis_agent = "DIAGNOSIS_AGENT"
        appointment_agent = "APPOINTMENT_AGENT"
        small_talk_agent = "SMALL_TALK_AGENT"
        out_of_topic_agent = "OUT_OF_TOPIC_AGENT"

    agent_list = get_class_field_values(Agents)
    agent_literals = Literal[*agent_list]
