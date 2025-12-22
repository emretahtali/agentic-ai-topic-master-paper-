from __future__ import annotations
import asyncio

from agentic_network.agents.appointment.system_prompt import system_msg
from agentic_network.core import AgentState
from agentic_network.agents.agent import Agent
from llm import appointment_llm
from mcp_client import appointment_mcp


class AppointmentAgent(Agent):
    def __init__(self):
        self.tools = appointment_mcp.get_tools()
        self.model = appointment_llm.bind_tools(self.tools)

    async def _get_node(self, state: AgentState) -> dict:
        messages = state["messages"]

        # call model
        response = self.model.invoke([system_msg] + messages)
        
        # return back the appointment data to llm
        return {
            "messages": [response],
            "active_agent": "appointment_agent"
        }



async def test():

    from loguru import logger
    from langchain_core.messages import HumanMessage

    try:
        logger.info(f"Initializing MCP Client for {appointment_mcp.label}...")
        await appointment_mcp.initialize()

        logger.info("Instantiating AppointmentAgent...")
        agent = AppointmentAgent()

        # Initialize the state
        state: AgentState = {"messages": [], "intermediate_steps": [], "agent_outcome": None}

        logger.success("Agent ready! Type 'exit' or 'quit' to stop.")
        print("-" * 50)

        # Start the Loop
        while True:
            # Get user input from console
            user_input = input("\n👤 User: ")

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input.strip():
                continue

            # Update state with the new human message
            state["messages"].append(HumanMessage(content=user_input))

            # Process with Agent
            result = await agent._get_node(state)

            # Extract the AI's response
            ai_msg = result["messages"][0]

            # Update local state with AI's message to maintain history
            state["messages"].append(ai_msg)

            # Handle Output
            if ai_msg.tool_calls:
                for tool_call in ai_msg.tool_calls:
                    logger.warning(f"🛠️  TOOL CALL: {tool_call['name']} -> {tool_call['args']}")

                # If tool calls exist, AI usually won't have text content
                if not ai_msg.content:
                    print(f"🤖 AI: [Requesting tool: {ai_msg.tool_calls[0]['name']}]")

            if ai_msg.content:
                print(f"🤖 AI: {ai_msg.content}")

    except KeyboardInterrupt:
        logger.info("\nLoop interrupted by user.")
    except Exception as e:
        logger.exception(f"Critical error in test loop: {e}")


if __name__ == "__main__":
    asyncio.run(test())