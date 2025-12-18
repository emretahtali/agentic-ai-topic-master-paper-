from __future__ import annotations
from abc import ABC, abstractmethod
from agentic_network.core import AgentState


class TopicAgent:
    def __call__(self, agent_state: AgentState) -> dict:
        return self._get_node(agent_state)

    @abstractmethod
    def _get_node(self, agent_state: AgentState) -> dict:
        raise NotImplementedError
