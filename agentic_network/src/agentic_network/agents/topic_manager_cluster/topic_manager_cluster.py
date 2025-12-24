from langgraph.graph.state import CompiledStateGraph, StateGraph

from agentic_network.agents.topic_manager_cluster.agents.post_processing_agent import TopicManagerPostProcessingAgent
from agentic_network.agents.topic_manager_cluster.agents.pre_processing_agent import TopicManagerPreProcessingAgent
from agentic_network.agents.topic_manager_cluster.agents.previous_topics_checker_agent import PreTopicsCheckerAgent
from agentic_network.agents.topic_manager_cluster.agents.router_agent import RouterAgent
from agentic_network.agents.topic_manager_cluster.agents.topic_change_checker_agent import TopicChangeCheckerAgent
from agentic_network.utils.base_agent import BaseAgent
from agentic_network.agents.topic_manager_cluster.core import (
    TopicManagerRoutes,
    TopicManagerState,
)
from agentic_network.agents.topic_manager_cluster.routing import is_topic_selected
from agentic_network.agents.topic_manager_cluster.agents import (
    NewTopicAgent,
    )
from agentic_network.core import AgentState


class TopicManagerCluster(BaseAgent):
    # The compiled, runnable graph (set in _build_graph)
    graph: CompiledStateGraph = None

    # Concrete agent instances (all share a common base: BaseAgent)
    pre_processing_agent: BaseAgent = None
    topic_change_checker_agent: BaseAgent = None
    pre_topics_checker_agent: BaseAgent = None
    new_topic_agent: BaseAgent = None
    router_agent: BaseAgent = None
    post_processing_agent: BaseAgent = None

    def __init__(self):
        """Create agents and build the graph once."""
        self._initialize_agents()
        self._build_graph()

    # ---- Internal Methods --------------------------------------------------------
    def _get_node(self, agent_state: AgentState) -> dict:
        topic_master_state = agent_state.get("topic_master_state")
        current_message = topic_master_state["current_message"]
        # print(f"[TopicMaster] {current_message=}")

        # TODO: add this to agentstate
        # TopicManagerState(
        #     agentic_state=agent_state,
        #     current_message=agent_state.get("current_message"),
        #     topic_stack=[],
        #     disclosed_topics=[],
        #     topic_selected=False

        final_state = self.graph.invoke(topic_master_state)
        topic_stack = final_state.get("topic_stack")
        # print(f"[TopicMaster] {topic_stack=}")

        return {
            "topic_master_state": final_state,
            "messages": final_state["current_message"],
        }

    def _initialize_agents(self) -> None:
        """Instantiate concrete agent nodes.

        Each agent should implement the callable interface expected by LangGraph
        (i.e., accept and return the `AgentState` mapping or compatible object).
        """
        self.pre_processing_agent = TopicManagerPreProcessingAgent()
        self.topic_change_checker_agent = TopicChangeCheckerAgent()
        self.pre_topics_checker_agent = PreTopicsCheckerAgent()
        self.new_topic_agent = NewTopicAgent()
        self.router_agent = RouterAgent()
        self.post_processing_agent = TopicManagerPostProcessingAgent()

    def _build_graph(self) -> None:
        """Declare nodes, edges, and routing, then compile the graph.

        Notes:
            - `TopicManagerRoutes` values are used as node identifiers to keep routing
              consistent and type-safe across the codebase.
            - `TopicManagerState` is the shared mutable state carried across nodes.
        """

        # Initialize a typed state graph; all node callables must accept&return AgentState
        graph_builder = StateGraph(TopicManagerState)

        # ---------------------- Nodes -------------------------------------------------
        # Register each agent under a stable route key from GraphRoutes.
        graph_builder.add_node(TopicManagerRoutes.PRE_PROCESSING_AGENT, self.pre_processing_agent)
        graph_builder.add_node(TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT, self.topic_change_checker_agent)
        graph_builder.add_node(TopicManagerRoutes.PRE_TOPICS_AGENT, self.pre_topics_checker_agent)
        graph_builder.add_node(TopicManagerRoutes.NEW_TOPIC_AGENT, self.new_topic_agent)
        graph_builder.add_node(TopicManagerRoutes.ROUTER_AGENT, self.router_agent)
        graph_builder.add_node(TopicManagerRoutes.POST_PROCESSING_AGENT, self.post_processing_agent)

        # ---------------------- Linear Edge(s) ----------------------------------------
        graph_builder.add_edge(TopicManagerRoutes.START, TopicManagerRoutes.PRE_PROCESSING_AGENT)
        graph_builder.add_edge(TopicManagerRoutes.PRE_PROCESSING_AGENT, TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT)
        graph_builder.add_edge(TopicManagerRoutes.NEW_TOPIC_AGENT, TopicManagerRoutes.ROUTER_AGENT)
        graph_builder.add_edge(TopicManagerRoutes.ROUTER_AGENT, TopicManagerRoutes.POST_PROCESSING_AGENT)
        graph_builder.add_edge(TopicManagerRoutes.POST_PROCESSING_AGENT, TopicManagerRoutes.END)

        # ---------------------- Conditional Routing -----------------------------------
        graph_builder.add_conditional_edges(
            TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT,
            is_topic_selected,
            path_map={
                TopicManagerRoutes.NEXT: TopicManagerRoutes.PRE_TOPICS_AGENT,
                TopicManagerRoutes.END: TopicManagerRoutes.ROUTER_AGENT
            },
        )
        graph_builder.add_conditional_edges(
            TopicManagerRoutes.PRE_TOPICS_AGENT,
            is_topic_selected,
            path_map={
                TopicManagerRoutes.NEXT: TopicManagerRoutes.NEW_TOPIC_AGENT,
                TopicManagerRoutes.END: TopicManagerRoutes.ROUTER_AGENT,
            },
        )

        # ---------------------- Compile -----------------------------------------------
        # Finalize the graph into a runnable pipeline.
        self.graph = graph_builder.compile()
