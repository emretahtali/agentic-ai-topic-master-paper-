from __future__ import annotations
from abc import abstractmethod
from typing import TypedDict


class BaseAgent:
    def __call__(self, agent_state: TypedDict) -> dict:
        return self._get_node(agent_state)

    @abstractmethod
    def _get_node(self, agent_state: TypedDict) -> dict:
        raise NotImplementedError
