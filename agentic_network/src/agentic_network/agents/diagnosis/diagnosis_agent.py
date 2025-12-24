from __future__ import annotations
import asyncio

from agentic_network.agents.diagnosis.system_prompt import system_msg
from agentic_network.core import AgentState
from agentic_network.utils import BaseAgent
from llm import get_llm, LLMModel
from mcp_client import diagnosis_mcp


class DiagnosisAgent(BaseAgent):

    def __init__(self):
        self.tools = diagnosis_mcp.get_tools()
        self.model = get_llm(LLMModel.DIAGNOSIS).bind_tools(self.tools)

    async def _get_node(self, state: AgentState) -> dict:

        messages = state["messages"]

        # call model
        response = self.model.invoke([system_msg] + messages)

        # return back the appointment data to llm
        return {
            "messages": [response]
        }



async def test():

    from loguru import logger
    from langchain_core.messages import HumanMessage

    try:
        logger.info(f"Initializing MCP Client for {diagnosis_mcp.label}...")
        await diagnosis_mcp.initialize()

        logger.info("Instantiating DiagnosisAgent...")
        agent = DiagnosisAgent()

        # Define Initial State with the Example Message
        example_content = "My chest has been feeling very tight and I am having trouble breathing."

        state: AgentState = {"messages": [HumanMessage(content=example_content)], "intermediate_steps": [],
            "agent_outcome": None}

        logger.success("Diagnosis Agent ready. Starting with example message.")
        print("-" * 50)
        print(f"👤 User (Example): {example_content}")

        # Message Loop
        while True:

            result = await agent._get_node(state)

            # Extract AI response and update state to maintain history
            ai_msg = result["messages"][0]
            state["messages"].append(ai_msg)

            # Display AI Output
            if ai_msg.tool_calls:
                for tool_call in ai_msg.tool_calls:
                    logger.warning(f"🛠️  TOOL CALL REQUESTED: {tool_call['name']} -> {tool_call['args']}")
                if not ai_msg.content:
                    print(f"🤖 AI: [Attempting to call {ai_msg.tool_calls[0]['name']}...]")

            if ai_msg.content:
                print(f"🤖 AI: {ai_msg.content}")

            # --- USER TURN ---
            print("-" * 50)
            user_input = input("👤 User (Type 'exit' to stop): ")

            if user_input.lower() in ["exit", "quit", "q"]:
                logger.info("Exiting test loop.")
                break

            if not user_input.strip():
                continue

            # Add user input to state for the next iteration
            state["messages"].append(HumanMessage(content=user_input))

    except Exception as e:
        logger.error(f"Test loop failed: {e}")
    finally:
        logger.info("Test session closed.")


if __name__ == "__main__":
    asyncio.run(test())
