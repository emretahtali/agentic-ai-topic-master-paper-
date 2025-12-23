from langchain_core.agents import AgentFinish
from langchain_core.messages import AIMessage

from agentic_network.utils import BaseAgent
from agentic_network.core import AgentState


class PostProcessingAgent(BaseAgent):
    async def _get_node(self, agent_state: AgentState) -> dict:
        agent_finish: AgentFinish = agent_state.get("agent_outcome", {})
        final_text = agent_finish.return_values.get("output", {})

        return {"messages": AIMessage(content=final_text)}
