from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from agentic_network.agents import AgentData
from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import (
    create_topic,
    get_current_topic,
    format_dialog,
)
from agentic_network.utils import BaseAgent
from llm.llm_client import get_llm, LLMModel


class RouterAgent(BaseAgent):
    agent: Runnable

    class ResponseSchema(BaseModel):
        agent: AgentData.agent_literals

    def __init__(self):
        self.llm = get_llm(LLMModel.TOPIC_MASTER)
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------
    def _initialize_model(self):
        # print("[RouterAgent] Initializing LLM connection…")
        try:
            self.agent = create_agent(
                model=self.llm,
                response_format=ToolStrategy(self.ResponseSchema)
            )

        except Exception as e:
            print(f"[RouterAgent] ❌LLM connection failed.\nError Message:\n{e}")
            exit()

    def _get_node(self, agent_state: TopicManagerState) -> dict:
        # print("[RouterAgent] Running agent...")

        current_message = agent_state.get("current_message")
        messages = get_current_topic(agent_state)["messages"][:]
        messages.append(current_message)
        topic_messages = format_dialog(messages)
        system_message = SystemMessage(self._get_system_prompt(current_message.content, topic_messages, AgentData.agent_list))

        response = self.agent.invoke(
            {
                "messages": [
                    system_message,
                    HumanMessage(content="Follow the instruction above and answer."),
                ]
            }
        )
        selected_agent = response["structured_response"].agent

        # print("[RouterAgent] Routing to agent:", selected_agent)
        current_topic = get_current_topic(agent_state)
        current_topic["agent"] = selected_agent

        return {}

    @staticmethod
    def _get_system_prompt(message: str, topic_messages: str, agents_list: list) -> str:
        formatted_agents = "\n".join([f"- {agent}" for agent in agents_list])

        return f"""\
    # ROLE
    You are a specialized routing component for an AI multi-agent system. Your sole task is **agent routing**: based ONLY on the latest user message and the provided context, choose which specialized agent should handle it.

    ## INPUTS
    ### Prior Context (`topic_messages`)
    ```text
    {topic_messages}
    ```
    
    ### Latest User Input (`user_input`)
    ```text
    {message}
    ```
    
    ### List of Specialized Agents
    ```text
    {formatted_agents}
    ```

    ---

    ## DECISION RULES
    1. **Single Best Agent:** Classify the single best agent based on the specialized scopes provided.
    2. **Action Priority:** If a message contains both information and an explicit request for action (e.g., "The site is slow, please open a ticket"), route to the agent responsible for the **action** (the "task-doer").
    3. **Information Priority:** If seeking information or describing a situation without a specific task, route to the agent responsible for that **subject matter**.
    4. **Brief Responses:** For brief acknowledgments (e.g., "okay," "got it"), route to the agent that was **previously active** in the `topic_messages` unless the user explicitly changes the subject.
    5. **Ambiguity:** If a message is on the border, select the agent whose scope description most specifically matches the user's keywords.

    ## STRICT OUTPUT
    Only print the agent parameter. Always select **EXACTLY** one agent name from the provided list.
    **(Do not output anything else.)**
    ""Only and only respond with PascalCase: PascalCase, FindHotels, ReserveRestaurant etc.""

    ---

    ## LANGUAGE & STYLE
    * Apply these rules universally across all languages.
    * Focus strictly on **intent and functional scope**.
    ""Only and only respond with PascalCase: PascalCase, FindHotels, ReserveRestaurant etc.""

    ## PROCESS
    1. **Analyze** the user's core intent (What do they want to *know* or *do*?).
    2. **Match** that intent against the 'Purpose' and 'Scope' of the available agents.
    3. **Output** exactly one final line with the agent name.

    ---

    ## EXAMPLES
    *(Assuming a Business/Tech system)*
    1. **Input:** "How do I reset my password?" → `TechSupport`
    2. **Input:** "My last invoice looks wrong, I was overcharged $50." → `BillingOperator`
    3. **Input:** "What are the best things to see in Rome besides the Colosseum" → `FindAttractions`
    4. **Input:** "I'm looking for a pet-friendly hotel in downtown Seattle for under $200 a night." → `SearchHotels`
    """
