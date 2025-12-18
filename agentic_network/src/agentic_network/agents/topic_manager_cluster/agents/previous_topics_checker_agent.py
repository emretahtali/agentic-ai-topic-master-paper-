from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from agentic_network.agents.topic_manager_cluster.agents import TopicAgent
from agentic_network.core import AgentState
from agentic_network.core.topic_manager_util import format_dialog_with_topics, format_dialog
from llm.core.llm_singletons import llmSingleton
from llm.core.gemma_based_model_adapter import GemmaBasedModelAdapter


class PreTopicsCheckerAgent(TopicAgent):
    def __init__(self):
        pass

    # ---- Internal Methods --------------------------------------------------------d
    def _get_node(self, agent_state: AgentState) -> dict:
        print("-PRE TOPICS CHECKER AGENT-")

        topic_stack = agent_state["topic_stack"]
        disclosed_topics = agent_state["disclosed_topics"]
        if not topic_stack and not disclosed_topics:
            return {
                "all_dialog": AIMessage("FINAL ANSWER: NEW TOPIC")
            }

        llm = llmSingleton.gemma_3_1b_it
        chat = GemmaBasedModelAdapter(llm)
        dialog = format_dialog_with_topics(agent_state["all_dialog"])
        thoughts = format_dialog(agent_state["thoughts"])
        current_message = agent_state["current_message"]
        system_message = self._build_system_message(dialog, current_message, thoughts)

        return {
            "thoughts": [chat.invoke([system_message, HumanMessage(content="Follow the instruction above and answer.")])]
        }

    def _build_system_message(self, dialog: str, message: str, thoughts: str) -> SystemMessage:
        system_message = SystemMessage(content=(
            f"""You are part of an AI assistant designed to help users with medical conditions get diagnosed and get hospital appointments. Your task here is **topic attribution**: decide which existing topic in the full dialog the latest user input belongs to, or declare that it should start a new topic.

    TASK
    Choose the single best topic for the latest user input, or output NEW TOPIC if no clear match exists.
    
    INPUTS
    - user_input — the latest user message (string)
    
    - dialog_with_topics — the entire dialog so far, ordered, each turn annotated with a topic id (string) beside it. Each item includes: role, content, topic_id.
    
    STRICT OUTPUT (ONLY ONE LINE)
    Always print EXACTLY one of:
    - FINAL ANSWER: [topic_id]
    - FINAL ANSWER: NEW TOPIC
    - THOUGHT: [your latest thoughts]
    (Do not output anything else.)
    
    DEFINITIONS
    - Topic: a coherent, ongoing task/subject within the medical-help context (e.g., symptom triage, a specific appointment, a lab/test, a prescription refill, insurance/billing for THIS visit).
    - Topic id: the uuid identifier appearing in dialog_with_topics for each message (e.g., "cde7f754-448d-4fc1-af48-37771e4a38a2"). You must choose from topic ids already present in the dialog. Do NOT invent new IDs.
    
    DECISION RULES — WHEN TO OUTPUT FOUND TOPIC
    Return FINAL ANSWER: [topic_id] if the user_input most likely continues one existing topic by any of these signals:
    1) Adds details, answers a question, clarifies, corrects, or follows up on the same problem/task.
    2) Refers to the same condition, symptoms, appointment (date/time/location/clinician), test, prescription/medic ation, or admin flow — including via pronouns/synonyms (“that”, “it”, “the MRI”, “Dr. Chen”, “tomorrow at 3”).
    3) Adjusts logistics for the same task (reschedulings changing location/doctor, confirming/canceling, insurance for that visit).
    
    DON'T attach brief acknowledgments/continuers (e.g., “okay,” “yes,” “got it,” “continue”) to a previous topic once the current topic has changed. Such replies cannot be credited to earlier topics; treat them as belonging to the current topic (or NEW TOPIC if no active topic applies).
    
    DECISION RULES — WHEN TO OUTPUT NEW TOPIC
    Return NEW TOPIC if any apply:
    1) Introduces a new medical issue, a different appointment/test/medication, or switches to a different patient/person.
    2) Shifts to a different administrative task for a different visit (e.g., from cardiology scheduling to insurance about physical therapy).
    3) General/unrelated chat, small talk, or a request unrelated to existing topics.
    4) Explicit change signals (“new topic”, “separately”, “on another note”).
    5) Ambiguous content with no clear linkage to any existing topic after applying tie-breakers.
    
    TIE-BREAKERS (if multiple topics match)
    - Prefer the topic with the strongest entity overlap (exact match on condition/appointment/test/clinician/date/time beats vague similarity).
    - If still tied, prefer the most recent topic in the dialog.
    - If still unclear, choose NEW TOPIC.
    
    LANGUAGE & STYLE
    - Apply the same rules for any language.
    - Ignore superficial formatting/casing; focus on meaning.
    - You are not giving medical advice — only attributing the new message to a topic.
    
    PROCESS
    Optionally reflect first using:
    THOUGHT: [brief reasoning about candidate topics and why]
    Then output exactly one final line as specified in STRICT OUTPUT.
    
    INPUTS:
    user_input:
    {message}
    
    dialog_with_topics:
    {dialog}
    
    THOUGHTS:
    These are your lates thoughts on this task if you've had any:
    {thoughts}
    """
        ))
        return system_message


# Test the AI
# agent = TopicChangeCheckerAgent()
# while True:
#     prompt = input("Prompt (or 'quit' to exit): ")
#     if prompt.lower() == 'quit': break
#
#     messages = [HumanMessage(content=prompt)]
#     response = agent({"all_dialog": messages})
#
#     print("\n" + "=" * 34 + " FINAL RESPONSE " + "=" * 34)
#     final_message = response['messages'][-1]
#     final_message.pretty_print()
#     print("=" * 58 + "\n")
