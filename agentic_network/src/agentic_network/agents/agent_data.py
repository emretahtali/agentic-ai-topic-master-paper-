from typing import Literal

from agentic_network.agents import DiagnosisAgent


class AgentData:
    class Agents:
        diagnosis_agent = "DIAGNOSIS_AGENT"

    agent_mapping = {
        Agents.diagnosis_agent: DiagnosisAgent,
    }
    agent_literals = Literal[agent_mapping]
