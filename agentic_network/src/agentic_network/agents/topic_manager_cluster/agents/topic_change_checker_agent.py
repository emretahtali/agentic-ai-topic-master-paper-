from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

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
        print("[TopicChangeCheckerAgent] Initializing LLM connection…")
        try:
            self.agent = create_agent(
                model=self.llm,
                response_format=ProviderStrategy(self.ResponseSchema),
            )

        except Exception as e:
            print(f"[NewTopicAgent] ❌LLM connection failed.\nError Message:\n{e}")
            exit()

    def _get_node(self, agent_state: TopicManagerState) -> dict:
        print("[TopicChangeCheckerAgent] Running agent...")

        topic_stack = agent_state["topic_stack"]
        if not topic_stack:
            print("[TopicChangeCheckerAgent] There was no topic in stack, redirect to: PRE TOPIC CHECKER AGENT")

            return {
                "topic_selected": False,
            }

        cur_topic: TopicState = get_current_topic(agent_state)
        cur_topic_messages = cur_topic.get("messages", [])

        current_message = agent_state["current_message"]
        system_message = SystemMessage(self._get_system_prompt(format_dialog(cur_topic_messages), current_message.content))

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
    def _get_system_prompt(cur_topic_messages: str, current_message: str) -> str:
        return f"""You are part of an AI assistant designed to help users with medical conditions get diagnosed and get hospital appointments. Your primary goal is to provide helpful, precise, and clear responses.

    TASK
    Decide if the latest user input continues the current topic in the ongoing medical-assistant dialog.

    INPUTS
    - user_input - the latest user message (string):
    {current_message}

    - messages - prior turns for the current topic (array of [role, content], ordered):
    {cur_topic_messages}

    STRICT OUTPUT
    Only print the final_decision parameter. Always select EXACTLY one of:
    {'\n'.join(ResponseModel.response_strings)}

    DEFINITIONS
    - Topic: a coherent, ongoing task/subject within the medical-help context (e.g., symptom triage, a specific appointment, a prescription refill, insurance/billing for THIS visit).
    - Current topic: what the messages have been discussing most recently.

    DECISION RULES — RETURN SAME_TOPIC IF ANY APPLY
    1) The input adds details, answers a question, clarifies, corrects, or follows up on the same problem/task in messages.
    2) It refers to the same condition, appointment, test, medication, clinician, or admin flow (even via pronouns/synonyms).
    3) It changes logistics of the same task (e.g., “Can we do Tuesday instead?” for the same appointment).
    4) It’s a brief acknowledgment/continuation cue (e.g., “okay,” “got it,” “continue”).

    DECISION RULES — RETURN DIFFERENT_TOPIC IF ANY APPLY
    1) Introduces a new medical issue, a different appointment/test/medication, or switches to a different patient/person.
    2) Shifts from clinical to unrelated admin (or vice versa) for a DIFFERENT task (e.g., from scheduling cardiology to asking about insurance for physical therapy).
    3) Starts general/unrelated chat (small talk, jokes, “what’s your name”), or a new request unrelated to messages.
    4) Explicit change signals like “new topic,” “on another note,” “separately,” “unrelated.”
    5) Empty/emoji-only/spam-like content with no clear link to the current topic.

    TIE-BREAKERS & AMBIGUITY
    - If there is clear linkage to the current topic → SAME_TOPIC.
    - If linkage is unclear or absent → DIFFERENT_TOPIC.
    - Mixed messages: if most of the substance continues the current topic → SAME_TOPIC; otherwise DIFFERENT_TOPIC.

    LANGUAGE & STYLE
    - Apply the same rules for any language.
    - Ignore superficial formatting/casing; focus on meaning.

    NOTE
    - You are ONLY classifying topic continuity, not giving medical advice.

    EXAMPLES
    A) messages: Booking an MRI for knee pain.
       user_input: “Morning works. Do they have anything before 10am?”
       final_answer: SAME_TOPIC

    B) messages: Guidance on managing migraines.
       user_input: “Also, I need to schedule a flu shot for my daughter.”
       final_answer: DIFFERENT_TOPIC

    PROCESS
    Reflect on the current situation based on the user's message.
    Then output exactly one final line as specified in STRICT OUTPUT.
    """
