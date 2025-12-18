from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from agentic_network.agents.topic_manager_cluster.agents import TopicAgent
from agentic_network.core import AgentState
from agentic_network.core.topic_manager_util import get_messages_for_current_topic, format_dialog
from llm.core.gemma_based_model_adapter import GemmaBasedModelAdapter
from llm.core.llm_singletons import llmSingleton


class TopicChangeCheckerAgent(TopicAgent):
    def __init__(self):
        pass

    # ---- Internal Methods --------------------------------------------------------d
    def _get_node(self, agent_state: AgentState) -> dict:
        print("-TOPIC CHANGE CHECKER AGENT-")

        topic_stack = agent_state["topic_stack"]
        if not topic_stack:
            print("--there was no topic in stack, redirect to: PRE TOPIC CHECKER AGENT")

            return {
                "thoughts": AIMessage("FINAL ANSWER: DIFFERENT TOPIC")
            }

        llm = llmSingleton.gemma_3_1b_it
        chat = GemmaBasedModelAdapter(llm)
        dialog = format_dialog(get_messages_for_current_topic(agent_state))
        thoughts = format_dialog(agent_state["thoughts"])
        current_message = agent_state["current_message"]
        system_message = self._build_system_message(dialog, current_message, thoughts)

        return {
            "thoughts": [chat.invoke([system_message, HumanMessage(content="Follow the instruction above and answer.")])]
        }

    def _build_system_message(self, dialog: str, message: str, thoughts: str) -> SystemMessage:
        system_message = SystemMessage(content=(
            f"""You are part of an AI assistant designed to help users with medical conditions get diagnosed and get hospital appointments. Your primary goal is to provide helpful, precise, and clear responses.

    TASK
    Decide if the latest user input continues the current topic in the ongoing medical-assistant dialog.

    INPUTS
    - user_input - the latest user message (string):
    {message}

    - messages - prior turns for the current topic (array of [role, content], ordered):
    {dialog}

    STRICT OUTPUT (ONLY ONE LINE)
    Always print EXACTLY one of:
    - FINAL ANSWER: SAME TOPIC
    - FINAL ANSWER: DIFFERENT TOPIC
    Or your latest thought in this STRICT format:
    - THOUGHT: [your latest thoughts]

    DEFINITIONS
    - Topic: a coherent, ongoing task/subject within the medical-help context (e.g., symptom triage, a specific appointment, a prescription refill, insurance/billing for THIS visit).
    - Current topic: what the messages have been discussing most recently.

    DECISION RULES — RETURN SAME TOPIC IF ANY APPLY
    1) The input adds details, answers a question, clarifies, corrects, or follows up on the same problem/task in messages.
    2) It refers to the same condition, appointment, test, medication, clinician, or admin flow (even via pronouns/synonyms).
    3) It changes logistics of the same task (e.g., “Can we do Tuesday instead?” for the same appointment).
    4) It’s a brief acknowledgment/continuation cue (e.g., “okay,” “got it,” “continue”).

    DECISION RULES — RETURN DIFFERENT TOPIC IF ANY APPLY
    1) Introduces a new medical issue, a different appointment/test/medication, or switches to a different patient/person.
    2) Shifts from clinical to unrelated admin (or vice versa) for a DIFFERENT task (e.g., from scheduling cardiology to asking about insurance for physical therapy).
    3) Starts general/unrelated chat (small talk, jokes, “what’s your name”), or a new request unrelated to messages.
    4) Explicit change signals like “new topic,” “on another note,” “separately,” “unrelated.”
    5) Empty/emoji-only/spam-like content with no clear link to the current topic.

    TIE-BREAKERS & AMBIGUITY
    - If there is clear linkage to the current topic → SAME TOPIC.
    - If linkage is unclear or absent → DIFFERENT TOPIC.
    - Mixed messages: if most of the substance continues the current topic → SAME TOPIC; otherwise DIFFERENT TOPIC.

    LANGUAGE & STYLE
    - Apply the same rules for any language.
    - Ignore superficial formatting/casing; focus on meaning.

    NOTE
    - You are ONLY classifying topic continuity, not giving medical advice.

    EXAMPLES
    A) messages: Booking an MRI for knee pain.
       user_input: “Morning works. Do they have anything before 10am?”
       OUTPUT (trace=none): FINAL ANSWER: SAME TOPIC
       OUTPUT (trace=brief): REASON: The message adjusts timing for the same MRI task. \nFINAL ANSWER: SAME TOPIC
       OUTPUT (trace=structured): SIGNALS: {"entities":["MRI","knee pain"],"continuity":["timing adjustment"],"shift":[]} \nFINAL ANSWER: SAME TOPIC

    B) messages: Guidance on managing migraines.
       user_input: “Also, I need to schedule a flu shot for my daughter.”
       OUTPUT (trace=brief): REASON: Introduces a new request for a different person. \nFINAL ANSWER: DIFFERENT TOPIC

    PROCESS
    You should first reflect on the current situation using 'THOUGHT: [your_thoughts]'.
    When you decide on an answer, print exactly one of these two answers:
    'FINAL ANSWER: SAME TOPIC' or 'FINAL ANSWER: DIFFERENT TOPIC'
    
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
