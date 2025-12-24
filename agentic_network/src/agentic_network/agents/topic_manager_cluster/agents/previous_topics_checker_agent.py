from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from agentic_network.agents import AgentData
from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import (
    format_dialog_with_topics,
    strip_quotes,
    resurface_topic,
)
from agentic_network.utils import BaseAgent
from llm import get_llm
from llm.llm_client import LLMModel


class ResponseModel:
    class Choices:
        new_topic = "NEW_TOPIC".upper()

class PreTopicsCheckerAgent(BaseAgent):
    agent: Runnable

    class ResponseSchema(BaseModel):
        uuid: str

    def __init__(self):
        self.llm = get_llm(LLMModel.TOPIC_MASTER)
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------
    def _initialize_model(self):
        # print("[PreTopicsCheckerAgent] Initializing LLM connection…")
        try:
            self.agent = create_agent(
                model=self.llm,
                response_format=ToolStrategy(self.ResponseSchema),
            )

        except Exception as e:
            print(f"[PreTopicsCheckerAgent] ❌LLM connection failed.\nError Message:\n{e}")
            exit()

    def _get_node(self, agent_state: TopicManagerState) -> dict:
        # print("[PreTopicsCheckerAgent] Running agent...")

        topic_stack = agent_state["topic_stack"]
        disclosed_topics = agent_state["disclosed_topics"]
        if not topic_stack and not disclosed_topics:
            # print("[PreTopicsCheckerAgent] There was no topic in stack or disclosed topics, redirect to: NEW TOPIC AGENT")

            return {
                "topic_selected": False,
            }

        dialog = format_dialog_with_topics(agent_state["agentic_state"]["messages"])
        current_message = agent_state["current_message"]
        system_message = SystemMessage(self._get_system_prompt(dialog, current_message.content, AgentData.agent_list))

        response = self.agent.invoke(
            {
                "messages": [
                    system_message,
                    HumanMessage(content="Follow the instruction above and answer."),
                ]
            }
        )
        selected_topic_uuid = strip_quotes(response["structured_response"].uuid.upper())
        update_state = resurface_topic(agent_state, selected_topic_uuid)

        if not update_state:
            return {
                "topic_selected": False,
            }

        update_state.update({
            "topic_selected": True,
        })
        return update_state

    @staticmethod
    def _get_system_prompt(dialog: str, message: str, agents_list: list) -> str:
        formatted_agents = "\n".join([f"- {agent}" for agent in agents_list])

        return f"""\
    # ROLE
    You are a specialized routing component for an AI multi-agent system. Your task is **topic attribution**: decide which existing topic in the dialog the latest user input belongs to, or declare that it should start a new topic.

    ## TASK
    Choose the single best **topic ID** for the latest user input from the existing conversation, or output **NEW TOPIC** if the input introduces a shift in intent or domain.

    ## INPUTS
    ### Annotated Dialog (`dialog_with_topics`)
    ```text
    {dialog}
    ```
    
    ### Latest User Message (`user_input`)
    ```text
    {message}
    ```
    
    ### List of Specialized Agents
    ```text
    {formatted_agents}
    ```

    ---

    ## STRICT OUTPUT
    Only print the `uuid` parameter. Always select **EXACTLY** one of:
    - `uuid=[topic_id]`
    - `uuid='{ResponseModel.Choices.new_topic}'`

    ---

    ## DEFINITIONS
    * **Topic:** A coherent, ongoing task, inquiry, or workflow within a specific domain (e.g., technical troubleshooting, billing, or scheduling).
    * **Topic ID:** The UUID identifier appearing in `dialog_with_topics`. You must choose from IDs already present in the dialog. **Do NOT invent new IDs.**

    ---

    ## DECISION RULES

    ### Return `uuid=[topic_id]` if:
    1. **Follow-up:** The input provides answers, clarifications, or follows up on the **active domain/task** of that ID.
    2. **Entity Consistency:** It refers to the same entities, assets, or processes previously mentioned (via names or pronouns like "it", "that", "the previous one").
    3. **Logistics Update:** It modifies details for the **SAME** task (e.g., changing the time, quantity, or location for the same service request).
    4. **Continuity:** It is a brief acknowledgment or continuation cue (e.g., "okay," "go ahead") immediately following that topic.

    ### Return `uuid='{ResponseModel.Choices.new_topic}'` if:
    1. **Category/Agent Shift:** The user switches to a different domain, specialty, or service category handled by a different agent from the list provided.
    2. **Entity Swap:** The user starts discussing a completely different project, person, or product, even if the action (e.g., "ordering") is the same.
    3. **Discontinuity:** The user explicitly abandons the previous thread (e.g., "actually never mind," "let's do something else instead").
    4. **Meta-Talk:** General small talk, or meta-questions about the AI itself.
    5. **Ambiguity:** Empty or nonsensical content with no clear semantic link to previous topics.

    ---

    ## TIE-BREAKERS
    * Prefer the topic with the **strongest entity overlap** (same specific product name, project ID, or person).
    * For "mixed" messages, if the primary new request is a different domain → **NEW TOPIC**.
    * If still tied, prefer the **most recent topic**.
    * If linkage is "strained" or unclear → **NEW TOPIC**.

    ---

    ## LANGUAGE & STYLE
    * Apply rules universally across all languages.
    * Focus strictly on **intent and domain boundaries**.

    ---

    ## PROCESS
    1. **Analyze** the `user_input` for its primary intent and the domain/agent it requires.
    2. **Compare** this to the domains of the existing topics in the dialog.
    3. **Identify Shifts:** If the user has switched "targets" (e.g., switching from Department A to Department B), output **NEW TOPIC**.
    4. **Final Output:** Print exactly one final line as specified in **STRICT OUTPUT**.
    """
