from __future__ import annotations
from abc import abstractmethod

from agentic_network.core import AgentState
from agentic_network.utils import BaseAgent


class DiagnosisAgent(BaseAgent):
    async def _get_node(self, agent_state: AgentState) -> dict:
        raise NotImplementedError
