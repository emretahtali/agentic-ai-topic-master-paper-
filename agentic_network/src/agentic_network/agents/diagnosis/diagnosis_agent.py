from __future__ import annotations
import asyncio

from agentic_network.agents.diagnosis.system_prompt import system_msg
from agentic_network.core import AgentState
from agentic_network.agents.agent import Agent
from llm import diagnosis_llm
from mcp_client import diagnosis_mcp


class DiagnosisAgent(Agent):

    def __init__(self):
        self.tools = diagnosis_mcp.get_tools()
        self.model = diagnosis_llm.bind_tools(self.tools)

    async def _get_node(self, state: AgentState) -> dict:

        messages = state["messages"]

        # call model
        response = self.model.invoke([system_msg] + messages)

        # return back the appointment data to llm
        return {"messages": [response], "active_agent": "diagnosis_agent"}


async def test():

    from loguru import logger
    from langchain_core.messages import HumanMessage

    try:
        logger.info(f"Initializing MCP Client for {diagnosis_mcp.label}")
        await diagnosis_mcp.initialize()

        logger.info("Instantiating DiagnosisAgent")
        agent = DiagnosisAgent()


        initial_state: AgentState = {"messages": [
            HumanMessage(content="My chest has been feeling very tight and I am having trouble breathing.")],
            "intermediate_steps": [], "agent_outcome": None}
        logger.info("Input Message: {}", initial_state["messages"][0].content)

        logger.info("Invoking _get_node")
        result = await agent._get_node(initial_state)

        ai_msg = result["messages"][0]

        if ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                logger.info(f"AI requested tool call: {tool_call['name']} with args: {tool_call['args']}")
        else:
            logger.info(f"AI RESPONSE: {ai_msg.content}")

        logger.success("Integration test completed successfully.")

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    asyncio.run(test())
