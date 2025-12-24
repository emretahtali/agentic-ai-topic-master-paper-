from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from agentic_network.agents import AgentData
from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.core.topic_manager_state import TopicState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import (
    get_current_topic,
    format_dialog,
)
from agentic_network.utils import BaseAgent, get_class_field_values
from llm.llm_client import get_llm, LLMModel

class ResponseModel:
    class Choices:
        same_topic = "SAME_TOPIC"
        different_topic = "DIFFERENT_TOPIC"

    response_strings = get_class_field_values(Choices)
    response_literals = Literal[*response_strings]

class TopicChangeCheckerAgent(BaseAgent):
    agent: Runnable

    class ResponseSchema(BaseModel):
        final_answer: ResponseModel.response_literals

    def __init__(self):
        self.llm = get_llm(LLMModel.TOPIC_MASTER)
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------d
    def _initialize_model(self):
        # print("[TopicChangeCheckerAgent] Initializing LLM connection…")
        try:
            self.agent = create_agent(
                model=self.llm,
                response_format=ToolStrategy(self.ResponseSchema),
            )

        except Exception as e:
            print(f"[NewTopicAgent] ❌LLM connection failed.\nError Message:\n{e}")
            exit()

    def _get_node(self, agent_state: TopicManagerState) -> dict:
        # print("[TopicChangeCheckerAgent] Running agent...")

        topic_stack = agent_state["topic_stack"]
        if not topic_stack:
            # print("[TopicChangeCheckerAgent] There was no topic in stack, redirect to: PRE TOPIC CHECKER AGENT")

            return {
                "topic_selected": False,
            }

        current_message = agent_state["current_message"]
        cur_topic: TopicState = get_current_topic(agent_state)
        cur_topic_messages = cur_topic.get("messages", []) + [current_message]

        system_message = SystemMessage(self._get_system_prompt(format_dialog(cur_topic_messages), current_message.content, AgentData.agent_list))

        response = self.agent.invoke(
            {
                "messages": [
                    system_message,
                    HumanMessage(content="Follow the instruction above and answer."),
                ]
            }
        )
        final_answer = response["structured_response"].final_answer.upper()

        return {
            "topic_selected": final_answer == ResponseModel.Choices.same_topic,
        }

    @staticmethod
    def _get_system_prompt(
        cur_topic_messages: str, current_message: str, agents_list: list
    ) -> str:
        formatted_agents = "\n".join([f"- {agent}" for agent in agents_list])
        response_options = "\n".join(ResponseModel.response_strings)

        return f"""# ROLE
    You are a specialized routing component for an AI multi-agent system. Your primary goal is to maintain topical consistency across a network of specialized agents.

    ## TASK
    Decide if the latest user input continues the **current topic/task** within the scope of the current agent, or if it shifts to a **different intent** that might require a different agent or a new session.

    ## INPUTS
    ### Prior Messages (Current Topic)
    ```text
    {cur_topic_messages}
    ```

    ### Latest User Input
    ```text
    {current_message}
    ```
    
    ### List of Specialized Agents
    ```text
    {formatted_agents}
    ```
    
    ## STRICT OUTPUT
    Only print the `final_decision` parameter. Always select **EXACTLY** one of the following:
    {response_options}
    
    ---
    
    ## DEFINITIONS
    * **Topic:** The specific subject matter, domain, or entity being discussed (e.g., a specific department, product, or technical issue). 
    * **Current Topic:** The specific domain and objective established in the recent 'Prior Messages'.
    
    ---
    
    ## DECISION RULES
    
    ### RETURN `SAME_TOPIC` IF:
    1. The input provides additional data, answers a prompt, clarifies, or follows up on the **active domain**.
    2. It refers to the **same entities, objects, or processes** previously mentioned.
    3. It modifies **logistics** for the existing subject (e.g., changing the time for the same service).
    4. It is a **brief acknowledgment** (e.g., "okay," "yes," "thanks").
    
    ### RETURN `DIFFERENT_TOPIC` IF:
    1. **Category Shift:** The user switches to a different department or service category, even if the verb (e.g., "book," "cancel") remains the same.
    2. **Agent Handoff:** The request introduces an intent that clearly belongs to a **different specialized agent** from the list provided.
    3. **Entity Swap:** Focus shifts to a completely different project, person, or asset not previously discussed.
    4. **Explicit Transitions:** Clear signals like "actually never mind," "on another note," or "let’s do something else."
    5. **Meta-Talk:** Starts unrelated talk about the AI itself or contains nonsensical/empty content.
    
    ---
    
    ## TIE-BREAKERS & AMBIGUITY
    * If the user explicitly abandons the previous thought → **DIFFERENT_TOPIC**.
    * If the action is the same but the "target" or "department" has changed → **DIFFERENT_TOPIC**.
    * If there is a plausible link to the current context → **SAME_TOPIC**.
    
    ## LANGUAGE & STYLE
    * Apply these rules **universally across all languages**.
    * Focus strictly on **intent and meaning**.
    * You are **ONLY** classifying topic continuity for routing purposes.
    
    ---
    
    ## EXAMPLES
    * **Context:** Processing a refund for a damaged item.
        **User Input:** "Wait, can you send it to my PayPal instead of my bank?"
        **Final Answer:** `SAME_TOPIC`
    
    * **Context:** Troubleshooting a software bug in a mobile app.
        **User Input:** "Thanks. Separately, I want to upgrade my subscription to Pro."
        **Final Answer:** `DIFFERENT_TOPIC`
    
    * **Context:** Inquiring about a savings account.
        **User Input:** "Actually, forget the savings account. I want to apply for a credit card."
        **Final Answer:** `DIFFERENT_TOPIC`
    
    * **Context:** Booking a flight to Paris.
        **User Input:** "Can we change the flight to 10 AM?"
        **Final Answer:** `SAME_TOPIC`
    
    ## FINAL PROCESS
    1. Analyze the user's intent relative to the prior messages and the available agent list.
    2. If the user is requesting a service from a different specialized agent or category, treat it as a new topic.
    3. Output exactly one final line as specified in **STRICT OUTPUT**.
    """
