from dotenv import load_dotenv, find_dotenv
from agentic_network.agents.topic_manager_cluster.agents.new_topic_agent import NewTopicAgent
from langchain_core.messages import HumanMessage, AIMessage
from agentic_network.agents.topic_manager_cluster.core.topic_manager_state import TopicManagerState
from agentic_network.core import AgentState

GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

load_dotenv(find_dotenv())
def main():
    agent = NewTopicAgent()
    state = TopicManagerState(
        agentic_state=AgentState(),
        current_message = HumanMessage("I have a strong headache. What should i do?"),
        topic_stack = [],
        disclosed_topics = [],
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
