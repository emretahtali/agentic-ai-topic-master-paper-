from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from agentic_network.agents import AgentData
from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from agentic_network.agents.topic_manager_cluster.utils.topic_manager_util import create_topic
from agentic_network.utils import BaseAgent
from llm.llm_client import get_llm, LLMModel


class NewTopicAgent(BaseAgent):
    agent: Runnable

    class ResponseSchema(BaseModel):
        agent: AgentData.agent_literals

    def __init__(self):
        self.llm = get_llm(LLMModel.TOPIC_MASTER)
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------
    def _initialize_model(self):
        print("[NewTopicAgent] Initializing LLM connection…")
        try:
            self.agent = create_agent(
                model=self.llm,
                response_format=ProviderStrategy(self.ResponseSchema)
            )

        except Exception as e:
            print(f"[NewTopicAgent] ❌LLM connection failed.\nError Message:\n{e}")
            exit()

    def _get_node(self, agent_state: TopicManagerState) -> dict:
        print("[NewTopicAgent] Running agent...")

        current_message = agent_state.get("current_message")
        system_message = SystemMessage(self._get_system_prompt(current_message.content))

        response = self.agent.invoke(
            {
                "messages": [
                    system_message,
                    HumanMessage(content="Follow the instruction above and answer."),
                ]
            }
        )
        selected_agent = response["structured_response"].agent.upper()
        messages = response["messages"]

        print("[NewTopicAgent] New topic is created with agent:", selected_agent)
        new_topic = create_topic(agent_state, selected_agent)

        return {
            "topic_stack": new_topic,
            "topic_selected": True
        }

    @staticmethod
    def _get_system_prompt(message: str) -> str:
        return f"""You are part of a medical assistant. Your sole task is **agent routing for a new topic**: based ONLY on the latest user message, choose which specialized agent should handle it.

    AGENTS & THEIR SCOPES
    - DIAGNOSIS_AGENT
      Purpose: Clinical questions and symptom triage.
      Route here when the message:
      • Describes symptoms, concerns, or a medical problem (“fever and cough”, “rash on my arm”).
      • Asks about causes, severity, risks, next clinical steps, labs/imaging interpretation, or treatment options.
      • Asks about medications in a clinical sense (side effects, interactions, dosing, safety, effectiveness).
      • Mentions urgent/emergency-sounding issues (chest pain, shortness of breath, suicide/self-harm) — still classify here.
      Examples: “My throat hurts and I have a fever.” / “Is 101°F dangerous?” / “What does a high WBC mean?” / “Is it safe to take ibuprofen with amoxicillin?”

    - APPOINTMENT_AGENT
      Purpose: Care logistics, scheduling, and visit-related admin.
      Route here when the message:
      • Requests to book, reschedule, confirm, or cancel appointments, tests, or procedures.
      • Specifies dates/times/locations/clinicians, preferences, or availability.
      • Handles visit logistics: telehealth vs. in-person, directions, preparation instructions, paperwork.
      • Handles visit-specific admin: insurance eligibility for this visit, referrals, prescription refills as an administrative request (“send to Walgreens”), change pharmacy for this prescription, provider/hospital choice for this booking.
      Examples: “Can you book me with Dr. Chen tomorrow at 3?” / “Move my MRI to next week.” / “Cancel my appointment.” / “Send the refill to CVS on 5th.”

    - SMALL_TALK_AGENT
      Purpose: Polite chatter and meta-assistant talk.
      Route here when the message:
      • Is greetings, thanks, acknowledgments, chit-chat, jokes, or short non-medical pleasantries.
      • Asks about the assistant itself (“what’s your name?”, “who made you?”) or generic “ok/thanks”.
      Examples: “Thanks!” / “hi there” / “lol that’s helpful” / “what are you?”

    - OUT_OF_TOPIC_AGENT
      Purpose: Everything irrelevant to healthcare tasks.
      Route here when the message:
      • Is clearly non-medical (shopping, travel, programming help, sports, etc.).
      • Is spam, empty, emoji-only, or not actionable.
      • Is administrative/billing not tied to a specific visit and cannot be addressed by scheduling logistics (e.g., “explain my insurance plan in general”).
      Examples: “Write me a Python script.” / “Plan my vacation.” / “What’s the stock price of XYZ?”

    INPUT
    - user_input — the latest user message (string):
    {message}

    DECISION RULES
    - Classify the **single best agent** for this new topic. Do not assume continuity with prior topics.
    - If the message contains both clinical details and an explicit scheduling action (e.g., “I have ear pain; book me with ENT tomorrow”), prefer **APPOINTMENT_AGENT** (the actionable request).
    - If there’s clinical content but no explicit scheduling/admin action, choose **DIAGNOSIS_AGENT**.
    - If the content is only greetings/thanks/acknowledgments or meta-chat, choose **SMALL_TALK_AGENT**.
    - If none of the above clearly applies or it’s unrelated to healthcare tasks, choose **OUT_OF_TOPIC_AGENT**.
    - Ambiguous? Prefer DIAGNOSIS_AGENT over OUT_OF_TOPIC_AGENT **only if** there is some medical substance (symptom/condition/med/drug/test term). Otherwise use OUT_OF_TOPIC_AGENT.

    STRICT OUTPUT
    Only print the agent parameter. Always select EXACTLY one of:
    {'\n'.join(AgentData.agent_mapping.keys())}
    (Do not output anything else.)

    LANGUAGE & STYLE
    - Apply the same rules for any language.
    - Ignore superficial formatting/casing; focus on meaning.
    - You are not giving medical advice — only attributing the new message to a topic.

    PROCESS
    Decide which agent must be called to answer the user's message
    Then output exactly one final line as specified in STRICT OUTPUT.

    EXAMPLES
    1) “I’ve had a cough for a week and green phlegm.” → select_agent("DIAGNOSIS_AGENT")
    2) “Book me with Dr. Patel next Tuesday afternoon.” → select_agent("APPOINTMENT_AGENT")
    3) “Thanks!” → select_agent("SMALL_TALK_AGENT")
    4) “Can you explain my BluePlus plan in general?” → select_agent("OUT_OF_TOPIC_AGENT")
    5) “Refill my amoxicillin to Walgreens on 5th.” → select_agent("APPOINTMENT_AGENT")
    6) “Is it safe to take ibuprofen with amoxicillin?” → select_agent("DIAGNOSIS_AGENT")
    """
