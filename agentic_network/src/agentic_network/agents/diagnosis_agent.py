from __future__ import annotations
from abc import abstractmethod

from agentic_network.core import AgentState


class DiagnosisAgent:
    async def __call__(self, agent_state: AgentState) -> dict:
        return await self._get_node(agent_state)

    async def _get_node(self, agent_state: AgentState) -> dict:
        raise NotImplementedError
