from langgraph.graph.state import CompiledStateGraph, StateGraph

from agentic_network.agents.cluster_agent import ClusterAgent
from agentic_network.agents.topic_manager_cluster.core import TopicManagerRoutes
from agentic_network.agents.topic_manager_cluster.routing import decide_topic_has_changed, decide_pre_topic_found, decide_new_topic_found
from agentic_network.agents.topic_manager_cluster.agents import TopicAgent, TopicChangeCheckerAgent
from agentic_network.agents.topic_manager_cluster.agents import PreTopicsCheckerAgent, NewTopicAgent
from agentic_network.core import AgentState


class TopicManagerCluster(ClusterAgent):
    # The compiled, runnable graph (set in _build_graph)
    graph: CompiledStateGraph = None

    # Concrete agent instances (all share a common base: TopicAgent)
    topic_change_checker_agent: TopicAgent = None
    pre_topics_checker_agent: TopicAgent = None
    new_topic_agent: TopicAgent = None

    def __init__(self):
        """Create agents and build the graph once."""
        self._initialize_agents()
        self._build_graph()

    # ---- Internal Methods --------------------------------------------------------
    def _get_node(self, agent_state: AgentState) -> dict:
        self.graph.invoke(state=agent_state)
        return {}

    def _initialize_agents(self) -> None:
        """Instantiate concrete agent nodes.

        Each agent should implement the callable interface expected by LangGraph
        (i.e., accept and return the `AgentState` mapping or compatible object).
        """
        self.topic_change_checker_agent = TopicChangeCheckerAgent()
        self.pre_topics_checker_agent = PreTopicsCheckerAgent()
        self.new_topic_agent = NewTopicAgent()

    def _build_graph(self) -> None:
        """Declare nodes, edges, and routing, then compile the graph.

        Structure:
            - Nodes: one per agent.
            - Start edge: START → TopicChangeCheckerAgent.
            - Conditional edges:
        #     todo: add these

        Notes:
            - `TopicManagerRoutes` values are used as node identifiers to keep routing
              consistent and type-safe across the codebase.
            - `AgentState` is the shared mutable state carried across nodes.
        """
        # Initialize a typed state graph; all node callables must accept&return AgentState
        graph_builder = StateGraph(AgentState)

        # ---------------------- Nodes -------------------------------------------------
        # Register each agent under a stable route key from GraphRoutes.
        graph_builder.add_node(TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT, self.topic_change_checker_agent)
        graph_builder.add_node(TopicManagerRoutes.PRE_TOPICS_AGENT, self.pre_topics_checker_agent)
        graph_builder.add_node(TopicManagerRoutes.NEW_TOPIC_AGENT, self.new_topic_agent)

        # ---------------------- Linear Edge(s) ----------------------------------------
        # Entry point: start the graph at TopicChangeCheckerAgent.
        graph_builder.add_edge(TopicManagerRoutes.START, TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT)

        # ---------------------- Conditional Routing -----------------------------------
        graph_builder.add_conditional_edges(
            TopicManagerRoutes.TOPIC_CHANGE_CHECKER_AGENT,
            decide_topic_has_changed
        )
        graph_builder.add_conditional_edges(
            TopicManagerRoutes.PRE_TOPICS_AGENT,
            decide_pre_topic_found
        )
        graph_builder.add_conditional_edges(
            TopicManagerRoutes.NEW_TOPIC_AGENT,
            decide_new_topic_found
        )

        # ---------------------- Compile -----------------------------------------------
        # Finalize the graph into a runnable pipeline.
        self.graph = graph_builder.compile()
