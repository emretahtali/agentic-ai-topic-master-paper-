from typing import Any, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

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
        self.tool_node = ToolNode(self.appointment_agent.tools)

    def _router(self, state: AgentState) -> Literal["tools", "__end__"]:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "__end__"

    def _build_graph(self) -> None:
        graph_builder = StateGraph(AgentState)

        graph_builder.add_node("appointment_agent", self.appointment_agent._get_node)
        graph_builder.add_node("tools", self.tool_node)

        graph_builder.add_edge(START, "appointment_agent")

        graph_builder.add_conditional_edges(
            "appointment_agent",
            self._router,
            {
                "tools": "tools",
                "__end__": END
            }
        )

        graph_builder.add_edge("tools", "appointment_agent")

        self.graph = graph_builder.compile(checkpointer=self.checkpointer)