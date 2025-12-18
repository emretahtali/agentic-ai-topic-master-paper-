from typing import Any
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from agentic_network.agents import AssistantAgent, ToolsAgent
from agentic_network.core import AgentState
from agentic_network.core import Routes
from agentic_network.routing import decide_tools
from .agents.pre_processing_agent import PreProcessingAgent
from .agents.post_processing_agent import PostProcessingAgent


class AgentGraph:
    """Orchestrates the agent network as a LangGraph state machine."""
    graph: CompiledStateGraph
    checkpointer: Any

    def __init__(self, checkpointer):
        """Create agents and build the graph once."""
        self.checkpointer = checkpointer
        self._initialize_agents()
        self._build_graph()

    # ---- Public API --------------------------------------------------------------
    def get_graph(self) -> CompiledStateGraph:
        return self.graph

    # ---- Internal Methods --------------------------------------------------------
    def _initialize_agents(self) -> None:
        """Instantiate concrete agent nodes."""
        self.pre_processing_agent = PreProcessingAgent()
        self.assistant_agent = AssistantAgent()
        self.tools_agent = ToolsAgent()
        self.post_processing_agent = PostProcessingAgent()

    def _build_graph(self) -> None:
        """Declare nodes, edges, and routing, then compile the graph."""
        graph_builder = StateGraph(AgentState)

        # ---------------------- Nodes -----------------------------------------------
        graph_builder.add_node(Routes.PRE_PROCESSING, self.pre_processing_agent)
        graph_builder.add_node(Routes.ASSISTANT, self.assistant_agent)
        graph_builder.add_node(Routes.TOOLS, self.tools_agent)
        graph_builder.add_node(Routes.POST_PROCESSING, self.post_processing_agent)

        # ---------------------- Lineer Edges ----------------------------------------
        graph_builder.add_edge(Routes.START, Routes.PRE_PROCESSING)
        graph_builder.add_edge(Routes.PRE_PROCESSING, Routes.ASSISTANT)
        graph_builder.add_edge(Routes.TOOLS, Routes.ASSISTANT)
        graph_builder.add_edge(Routes.POST_PROCESSING, Routes.END)

        # ---------------------- Conditional Edges -----------------------------------
        graph_builder.add_conditional_edges(Routes.ASSISTANT, decide_tools, path_map={
            "tools": Routes.TOOLS,
            "end": Routes.POST_PROCESSING
        })

        # ---------------------- Compile ---------------------------------------------
        # self.graph = graph_builder.compile(checkpointer=self.checkpointer)
        self.graph = graph_builder.compile()
