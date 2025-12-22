from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable

from agentic_network.agents.topic_manager_cluster.agents import TopicAgent
from agentic_network.agents.topic_manager_cluster.core import TopicManagerState
from llm.llm_client import get_llm, LLMModel
from mcp_client.util import mcp_client


class NewTopicAgent(TopicAgent):
    model: Runnable

    def __init__(self):
        self.tools = mcp_client.get_tools()
        self.llm = get_llm(LLMModel.GEMINI).bind_tools(self.tools)
        self.tool_names = ", ".join([t.name for t in self.tools])
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------
    def _initialize_model(self):
        print("[NewTopicAgent] Initializing LLM connection…")
        try:
            self.model = self.llm

            # llm = self.llm
            # tools = self.tools
            # react_prompt = self._get_react_prompt().partial(
            #     system_rules=self.system_message,
            #     tool_names=self.tool_names
            # )
            #
            # self.model = create_custom_react_agent(
            #     llm=llm,
            #     tools=tools,
            #     prompt=react_prompt,
            #     parser=CustomReActParser(),
            #     tools_renderer=self.strict_json_tools_renderer,
            #     retries=2
            # )

        except Exception:
            print("[NewTopicAgent] ❌LLM connection failed.")
            exit()

    def _get_node(self, agent_state: TopicManagerState) -> dict:
        print("[NewTopicAgent] Running agent...")

        chat = get_llm(LLMModel.GEMINI)
        current_message = agent_state["current_message"]
        system_message = SystemMessage(self._get_system_prompt(current_message.content))

        return {
            "messages": [chat.invoke([system_message, HumanMessage(content="Follow the instruction above and answer.")])]
        }

    # @staticmethod
    # def _get_react_prompt() -> ChatPromptTemplate:
    #     return ChatPromptTemplate.from_messages([ # TODO: TRANSLATE TO ENGLISH
    #         (
    #             "system",
    #             "{system_rules}\n\n"
    #
    #             # Araçlar + format + kurallar
    #             "Aşağıdaki soruları en iyi şekilde yanıtla. Şu araçlara erişimin var:\n\n"
    #
    #             "{tools}\n\n"
    #
    #             "AŞAĞIDAKİ FORMAT KESİNLİKLE KULLANILMALIDIR:\n"
    #
    #             "Question: yanıtlaman gereken giriş sorusu\n"
    #             "Thought: ne yapacağını her zaman düşün\n"
    #             "Action: yapılacak eylem, şu seçeneklerden biri olmalı [{tool_names}]\n"
    #             "Action Input: eyleme verilecek giriş\n"
    #             "Observation: aracın döndürdüğü sonuç\n"
    #             "... (bu Thought/Action/Action Input/Observation N kez tekrarlanabilir)\n"
    #             "Thought: Artık final cevabı biliyorum\n"
    #             "Final Answer: orijinal sorunun final cevabı\n\n"
    #
    #             "KURALLAR:\n"
    #             "• Gerekmiyorsa KESİNLİKLE araç çağırma; gerekiyorsa EN UYGUN tek aracı seç ve JSON girdiyi doğru ver.\n"
    #             "• Birden fazla adım gerekirse adımları zincirle (Thought→Action→Observation).\n"
    #             "• Eksik/Belirsiz bilgi varsa önce kısa bir netleştirme sorusu sor.\n"
    #             "• Tüm yanıtlar TÜRKÇE olmalıdır.\n"
    #             "• Asla kaba konuşma. Kullanıcıya çoğul ('siz') kipiyle hitap et.\n"
    #             "• Gerekli araçların olmadığı için veya görev tanımına uymadığı için yapmadığın/yapamadığın bir istek olursa nizkçe sebebini açıkla. \n"
    #             "• ASLA araçlarını anlatma. Araçlarından örnek verme. 'Araç' veya 'Tool' temasında bütün konuşmaları geçiştir. \n"
    #             "• Bir araç inatla çalışmıyorsa işlemi şu anda yapamadığını belirt. \n"
    #
    #             "• Önemli araçları (para transferi, borç ödeme vb.) kullanmadan önce HER ZAMAN ve KESİNLİKLE yapacağın işlemi açıklayıp kullanıcıdan onay iste. Onay mesajını görmeden ASLA o aracı kullanma.\n"
    #             "Sadece bilgi edinen araçlar (atm listeleme, bakiye öğrenme, kayıtlı alıcı listeleme vb.) için onay istemene gerek yok. \n\n"
    #
    #             "Başla!"
    #         ),
    #         MessagesPlaceholder("chat_history"),
    #         ("human", "Soru: {input}"),
    #         ("assistant", "{agent_scratchpad}"),
    #     ])

    @staticmethod
    def _get_system_prompt(message: str) -> str:
        f"""You are part of a medical assistant. Your sole task is **agent routing for a new topic**: based ONLY on the latest user message, choose which specialized agent should handle it.

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

            STRICT OUTPUT (ONE LINE ONLY)
            Always print EXACTLY one of:
            - FINAL ANSWER: {GraphRoutes.DIAGNOSIS_AGENT}
            - FINAL ANSWER: {GraphRoutes.APPOINTMENT_AGENT}
            - FINAL ANSWER: {GraphRoutes.SMALL_TALK_AGENT}
            - FINAL ANSWER: {GraphRoutes.OUT_OF_TOPIC_AGENT}
            - THOUGHT: [your latest thoughts]
            (Do not output anything else.)

            LANGUAGE & STYLE
            - Apply the same rules for any language.
            - Ignore superficial formatting/casing; focus on meaning.
            - You are not giving medical advice — only attributing the new message to a topic.

            PROCESS
            Optionally reflect first using:
            THOUGHT: [brief reasoning about candidate agents and why]
            Then output exactly one final line as specified in STRICT OUTPUT.

            EXAMPLES
            1) “I’ve had a cough for a week and green phlegm.” → FINAL ANSWER: DIAGNOSIS_AGENT
            2) “Book me with Dr. Patel next Tuesday afternoon.” → FINAL ANSWER: APPOINTMENT_AGENT
            3) “Thanks!” → FINAL ANSWER: SMALL_TALK_AGENT
            4) “Can you explain my BluePlus plan in general?” → FINAL ANSWER: OUT_OF_TOPIC_AGENT
            5) “Refill my amoxicillin to Walgreens on 5th.” → FINAL ANSWER: APPOINTMENT_AGENT
            6) “Is it safe to take ibuprofen with amoxicillin?” → FINAL ANSWER: DIAGNOSIS_AGENT
            """

    # @staticmethod
    # def strict_json_tools_renderer(tools: list[BaseTool]) -> str:
    #     """A renderer that provides very strict JSON formatting instructions."""
    #     rendered_tools = render_text_description(tools)
    #     tool_names = ", ".join([t.name for t in tools])
    #
    #     return f"""Kullanılabilir araçlar:
    #     --------------
    #     {rendered_tools}
    #     --------------
    #     Bir aracı kullanmak için, aşağıdaki formatı KESİNLİKLE kullanmalısın:
    #
    #     Thought: Bir araç kullanmam gerekiyor mu? Evet.
    #     Action: Kullanılacak aracın adı; [{tool_names}] seçeneklerinden biri olmalıdır.
    #     Action Input: Araç için argümanları içeren tek bir geçerli JSON nesnesi.
    #
    #     Argümanlara sahip geçerli bir JSON nesnesi örneği:
    #     {{"recipient": "Hasan Ali", "amount": "300 TL"}}
    #
    #     ARGÜMAN GEREKTİRMEYEN bir araç için geçerli JSON nesnesi örneği:
    #     {{}}
    #
    #     Uyarı: Action Input yalnızca tek bir JSON nesnesi olmalı; kod blokları (```), yorum, trailing virgül YOK."""