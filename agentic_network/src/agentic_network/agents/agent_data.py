from typing import Literal

from agentic_network.utils import get_class_variable_field_values


class AgentData:
    class Agents:
        diagnosis_agent = "DIAGNOSIS_AGENT"

    agent_list = get_class_variable_field_values(Agents)
    agent_literals = Literal[*agent_list]
