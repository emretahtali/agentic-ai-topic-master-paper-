from typing import Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from agentic_network.agents.appointment.appointment_agent import AppointmentAgent
from agentic_network.core import AgentState

class AgentGraph:
    graph: CompiledStateGraph
    checkpointer: Any

    def __init__(self, checkpointer):
        self.checkpointer = checkpointer
        self._initialize_agents()
        self._build_graph()

    def get_graph(self) -> CompiledStateGraph:
        return self.graph

    def _initialize_agents(self) -> None:
        self.appointment_agent = AppointmentAgent()

    def _build_graph(self) -> None:
        graph_builder = StateGraph(AgentState)

        graph_builder.add_node("appointment_agent", self.appointment_agent._get_node)

        graph_builder.add_edge(START, "appointment_agent")
        graph_builder.add_edge("appointment_agent", END)

        self.graph = graph_builder.compile(checkpointer=self.checkpointer)