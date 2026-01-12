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
                response_format=ProviderStrategy(self.ResponseSchema)
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
    1. **AddAlarm:** "Wake me up at 7 AM tomorrow."
    2. **BuyBusTicket:** "I'd like to buy a seat on the 5:00 PM bus to Boston."
    3. **FindAttractions:** "What are some fun things to do in San Francisco this weekend?"
    4. **FindBus:** "When is the next bus arriving at North Station?"
    5. **FindProvider:** "I need to find a local internet service provider in Seattle."
    6. **GetAlarms:** "Show me a list of all my active alarms."
    7. **LookupMusic:** "Who sang the song that goes 'Ground Control to Major Tom'?"
    8. **PlayMedia:** "Shuffle my jazz playlist on Spotify."
    9. **ReserveHotel:** "Go ahead and book the King Suite at the Hilton for those dates."
    10. **ReserveRestaurant:** "Table for four at Mama Leone's at 8 PM, please."
    11. **SearchHotel:** "Find me hotels in Tokyo with a gym and free breakfast."
    12. **SearchHouse:** "Look for 3-bedroom houses for sale in the suburbs of Austin."
    13. **SearchRoundtripFlights:** "I need a roundtrip flight from London to New York for next month."
    14. **NONE:** "Asdfghjkl" or "What color is a mirror?"
    15. **AddAlarm**: "Wait, scratch that—make it 8 AM instead." (Correction to the latest topic)
    16. **BuyBusTicket**: "Does the ticket price include a carry-on bag?" (Specific inquiry within the current topic)
    17. **SearchHotel**: "Actually, what is the weather like in Tokyo first?" (Interruption/Switch to a new topic)
    18. **ReserveRestaurant**: "Can we increase the party size to six?" (Modification of an active topic)
    19. **FindAttractions**: "Are any of those places open after 10 PM?" (Refining the latest topic with a constraint)
    20. **SearchHouse**: "Show me more like the first one you found." (Contextual reference to a previous result)
    21. **NONE**: "I'm not sure yet, I'll have to check my schedule." (Stalling/Non-actionable input)
    22. **ReserveHotel**: "Is it too late to change my check-in date?" (Attempting to modify a previous topic)
    23. **FindProvider**: "Never mind about the internet, do they offer cable TV too?" (Pivoting from a current topic to a new related one)
    24. **LookupMusic**: "Who was the lead singer of that band again?" (Follow-up question on a previous topic)
    25. **NONE**: "Tell me a joke." (Out-of-scope request that doesn't trigger an expert)
    26. **NONE**: "No, I don't want to make the reservation now."
    """
