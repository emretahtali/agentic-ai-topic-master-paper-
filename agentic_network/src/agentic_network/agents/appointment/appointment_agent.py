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
        self.tool_map = {tool.name: tool for tool in self.tools}
        self.model = appointment_llm.bind_tools(self.tools)

#    async def _get_node(self, state: AgentState) -> dict:
#       messages = state["messages"]
#
#       # call model
#       response = self.model.invoke([system_msg] + messages)
#
#       # return back the appointment data to llm
#        return {
#           "messages": [response],
#            "active_agent": "appointment_agent"
#       }

    async def _get_node(self, state: AgentState) -> dict:
        messages = state["messages"]

        cleaned_messages = []
        for msg in messages:
            if msg.type == "tool" and isinstance(msg.content, list):
                msg_content = ""
                for item in msg.content:
                    if isinstance(item, dict) and "text" in item:
                        msg_content += item["text"]
                    else:
                        msg_content += str(item)
                msg.content = msg_content
            cleaned_messages.append(msg)

        response = self.model.invoke([system_msg] + cleaned_messages)

        return {
            "messages": [response],
            "active_agent": "appointment_agent"
        }


async def test():
    from loguru import logger
    from langchain_core.messages import HumanMessage, ToolMessage

    try:
        logger.info(f"Initializing MCP Client for {appointment_mcp.label}...")
        await appointment_mcp.initialize()

        logger.info("Instantiating AppointmentAgent...")
        agent = AppointmentAgent()

        state: AgentState = {"messages": [], "intermediate_steps": [], "agent_outcome": None}

        logger.success("Agent ready! Type 'exit' or 'quit' to stop.")
        print("-" * 50)

        while True:
            user_input = input("\n👤 User: ")

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input.strip():
                continue

            state["messages"].append(HumanMessage(content=user_input))

            # --- AGENT LOOP ---
            while True:
                result = await agent._get_node(state)
                ai_msg = result["messages"][0]
                state["messages"].append(ai_msg)

                if ai_msg.tool_calls:
                    for tool_call in ai_msg.tool_calls:
                        tool_name = tool_call["name"]
                        tool_args = tool_call["args"]
                        tool_id = tool_call["id"]

                        logger.warning(f"🛠️  TOOL CALL: {tool_name} -> {tool_args}")

                        selected_tool = agent.tool_map.get(tool_name)
                        tool_output = "Error: Tool not found"

                        if selected_tool:
                            try:
                                tool_output = await selected_tool.ainvoke(tool_args)

                                logger.info(f"   ✅ RESULT: {str(tool_output)[:100]}...")
                            except Exception as e:
                                tool_output = f"Tool Execution Error: {str(e)}"
                                logger.error(f"   ❌ ERROR: {tool_output}")
                        else:
                            logger.error(f"   ❌ ERROR: Tool '{tool_name}' not found.")

                        content_str = str(tool_output)

                        tool_msg = ToolMessage(
                            content=content_str,
                            tool_call_id=tool_id,
                            name=tool_name
                        )
                        state["messages"].append(tool_msg)

                    continue

                else:
                    print(f"🤖 AI: {ai_msg.content}")
                    break

    except KeyboardInterrupt:
        logger.info("\nLoop interrupted by user.")
    except Exception as e:
        logger.exception(f"Critical error in test loop: {e}")


if __name__ == "__main__":
    asyncio.run(test())