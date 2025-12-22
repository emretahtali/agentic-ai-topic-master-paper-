from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp.prompts.base import UserMessage

from agentic_network.agents import DiagnosisAgent, AgentData
from agentic_network.agents.topic_manager_cluster.agents.new_topic_agent import NewTopicAgent
from langchain_core.messages import HumanMessage, AIMessage

from agentic_network.agents.topic_manager_cluster.agents.topic_change_checker_agent import TopicChangeCheckerAgent
from agentic_network.agents.topic_manager_cluster.core.topic_manager_state import (
    TopicManagerState,
    TopicState,
)

GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

load_dotenv(find_dotenv())
def main():
    agent = TopicChangeCheckerAgent()
    state = TopicManagerState(
        # current_message = HumanMessage("Yes please."),
        current_message = HumanMessage("Actually never mind, I want to make an appointment for orthopedics."),
        topic_stack = [
            TopicState(
                messages = [
                    UserMessage("Hello, can you help?"),
                    AIMessage("Of course, what is your problem?"),
                    UserMessage("I have a strong headache. What should i do?"),
                    AIMessage("Then you should get an appointment from neurology clinic. Can i help you make the appointment?"),
                ],
                agent=AgentData.Agents.diagnosis_agent
            )
        ],
        topic_selected = False
    )
    state.update(agent(state))
    # ai_message: AIMessage = state.get("messages")[-1]

    for key, value in state.items():
        print(f"{GREEN}{BOLD}{key}: {YELLOW}{value}{RESET}")

    # print(f"{GREEN}{BOLD}ai message: {YELLOW}{ai_message}{RESET}")
    # print(f"{GREEN}{BOLD}ai message content: {YELLOW}{ai_message.content}{RESET}")
    #
    # print(f"{GREEN}{BOLD}selected agent: {YELLOW}{final_state.get('selected_agent')}{RESET}")

if __name__ == "__main__":
    main()
