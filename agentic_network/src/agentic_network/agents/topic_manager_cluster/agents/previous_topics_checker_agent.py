from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import (
    format_dialog_with_topics,
    strip_quotes,
    find_topic_index,
    resurface_topic,
)
from agentic_network.utils import BaseAgent
from agentic_network.core import AgentState
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
        self.llm = get_llm(LLMModel.GEMINI)
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------
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
        print("[PreTopicsCheckerAgent] Running agent...")

        topic_stack = agent_state["topic_stack"]
        disclosed_topics = agent_state["disclosed_topics"]
        if not topic_stack and not disclosed_topics:
            print("[PreTopicsCheckerAgent] There was no topic in stack or disclosed topics, redirect to: NEW TOPIC AGENT")

            return {
                "topic_selected": False,
            }

        dialog = format_dialog_with_topics(agent_state["agentic_state"]["messages"])
        current_message = agent_state["current_message"]
        system_message = SystemMessage(self._get_system_prompt(dialog, current_message))

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
    def _get_system_prompt(self, dialog: str, message: str) -> str:
        return f"""You are part of an AI assistant designed to help users with medical conditions get diagnosed and get hospital appointments. Your task here is **topic attribution**: decide which existing topic in the full dialog the latest user input belongs to, or declare that it should start a new topic.

    TASK
    Choose the single best topic for the latest user input, or output NEW TOPIC if no clear match exists.
    
    INPUTS
    - user_input — the latest user message (string)
    
    - dialog_with_topics — the entire dialog so far, ordered, each turn annotated with a topic id (string) beside it. Each item includes: role, content, topic_id.
    
    STRICT OUTPUT
    Only print the uuid parameter. Always select EXACTLY one of:
    - uuid=[topic_id]
    - uuid='{ResponseModel.Choices.new_topic}'
    (Do not output anything else.)
    
    DEFINITIONS
    - Topic: a coherent, ongoing task/subject within the medical-help context (e.g., symptom triage, a specific appointment, a lab/test, a prescription refill, insurance/billing for THIS visit).
    - Topic id: the uuid identifier appearing in dialog_with_topics for each message (e.g., "cde7f754-448d-4fc1-af48-37771e4a38a2"). You must choose from topic ids already present in the dialog. Do NOT invent new IDs.
    
    DECISION RULES — WHEN TO OUTPUT FOUND TOPIC
    Return uuid=[topic_id] if the user_input most likely continues one existing topic by any of these signals:
    1) Adds details, answers a question, clarifies, corrects, or follows up on the same problem/task.
    2) Refers to the same condition, symptoms, appointment (date/time/location/clinician), test, prescription/medic ation, or admin flow — including via pronouns/synonyms (“that”, “it”, “the MRI”, “Dr. Chen”, “tomorrow at 3”).
    3) Adjusts logistics for the same task (reschedulings changing location/doctor, confirming/canceling, insurance for that visit).
    
    DON'T attach brief acknowledgments/continuers (e.g., “okay,” “yes,” “got it,” “continue”) to a previous topic once the current topic has changed. Such replies cannot be credited to earlier topics; treat them as belonging to the current topic (or NEW TOPIC if no active topic applies).
    
    DECISION RULES — WHEN TO OUTPUT uuid='{ResponseModel.Choices.new_topic}'
    Return uuid='{ResponseModel.Choices.new_topic}' if any apply:
    1) Introduces a new medical issue, a different appointment/test/medication, or switches to a different patient/person.
    2) Shifts to a different administrative task for a different visit (e.g., from cardiology scheduling to insurance about physical therapy).
    3) General/unrelated chat, small talk, or a request unrelated to existing topics.
    4) Explicit change signals (“new topic”, “separately”, “on another note”).
    5) Ambiguous content with no clear linkage to any existing topic after applying tie-breakers.
    
    TIE-BREAKERS (if multiple topics match)
    - Prefer the topic with the strongest entity overlap (exact match on condition/appointment/test/clinician/date/time beats vague similarity).
    - If still tied, prefer the most recent topic in the dialog.
    - If still unclear, choose uuid='{ResponseModel.Choices.new_topic}'.
    
    LANGUAGE & STYLE
    - Apply the same rules for any language.
    - Ignore superficial formatting/casing; focus on meaning.
    - You are not giving medical advice — only attributing the new message to a topic.
    
    PROCESS
    Reflect on the current situation based on the user's message.
    Then output exactly one final line as specified in STRICT OUTPUT.
    
    INPUTS:
    user_input:
    {message}
    
    dialog_with_topics:
    {dialog}
    """
