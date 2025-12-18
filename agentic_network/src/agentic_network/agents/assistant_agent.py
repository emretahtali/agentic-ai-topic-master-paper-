from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages.utils import trim_messages
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_classic.tools.render import render_text_description
from datetime import datetime

from agentic_network.agents import Agent
from agentic_network.core import AgentState
from agentic_network.util import CustomReActParser, create_custom_react_agent, count_messages
from mcp_client import mcp_client
from llm import get_llm


class AssistantAgent(Agent):
    model: Runnable

    def __init__(self):
        self.system_message = self._get_system_message()
        self.llm = get_llm()
        self.tools = mcp_client.get_tools()
        self.tool_names = ", ".join([t.name for t in self.tools])
        self._initialize_model()

    # ---- Internal Methods --------------------------------------------------------
    def _initialize_model(self):
        print("[startup] Initializing LLM connection…")
        try:
            llm = self.llm
            tools = self.tools
            react_prompt = self._get_react_prompt().partial(
                system_rules=self.system_message,
                tool_names=self.tool_names
            )

            self.model = create_custom_react_agent(
                llm=llm,
                tools=tools,
                prompt=react_prompt,
                parser=CustomReActParser(),
                tools_renderer=self.strict_json_tools_renderer,
                retries=2
            )

        except Exception as e:
            print(f"❌ Assistant Agent: LLM connection failed.")
            exit()

    async def _get_node(self, agent_state: AgentState) -> dict:
        print("\n---ASSISTANT AGENT---")

        messages = agent_state["messages"]
        if not messages:
            # first turn safety: treat whole input as {input} and empty history
            input_text = ""
            chat_history = []

        else:
            input_text = messages[-1].content
            chat_history = messages[:-1]

        # trim history to a token budget
        chat_history = trim_messages(
            chat_history,
            max_tokens=1000,
            token_counter=count_messages,
            strategy="last",
            start_on="human",
        )

        response: AgentAction | AgentFinish = await self.model.ainvoke({
            "input": input_text,
            "chat_history": chat_history,
            "intermediate_steps": agent_state.get("intermediate_steps", []),
        })

        print("LLM response:", response)
        return {"agent_outcome": response}

    @staticmethod
    def _get_react_prompt() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            (
                "system",
                "{system_rules}\n\n"
             
                # Araçlar + format + kurallar
                "Aşağıdaki soruları en iyi şekilde yanıtla. Şu araçlara erişimin var:\n\n"
                
                "{tools}\n\n"
                
                "AŞAĞIDAKİ FORMAT KESİNLİKLE KULLANILMALIDIR:\n"
                
                "Question: yanıtlaman gereken giriş sorusu\n"
                "Thought: ne yapacağını her zaman düşün\n"
                "Action: yapılacak eylem, şu seçeneklerden biri olmalı [{tool_names}]\n"
                "Action Input: eyleme verilecek giriş\n"
                "Observation: aracın döndürdüğü sonuç\n"
                "... (bu Thought/Action/Action Input/Observation N kez tekrarlanabilir)\n"
                "Thought: Artık final cevabı biliyorum\n"
                "Final Answer: orijinal sorunun final cevabı\n\n"
            
                "KURALLAR:\n"
                "• Gerekmiyorsa KESİNLİKLE araç çağırma; gerekiyorsa EN UYGUN tek aracı seç ve JSON girdiyi doğru ver.\n"
                "• Birden fazla adım gerekirse adımları zincirle (Thought→Action→Observation).\n"
                "• Eksik/Belirsiz bilgi varsa önce kısa bir netleştirme sorusu sor.\n"
                "• Tüm yanıtlar TÜRKÇE olmalıdır.\n"
                "• Asla kaba konuşma. Kullanıcıya çoğul ('siz') kipiyle hitap et.\n"
                "• Gerekli araçların olmadığı için veya görev tanımına uymadığı için yapmadığın/yapamadığın bir istek olursa nizkçe sebebini açıkla. \n"
                "• ASLA araçlarını anlatma. Araçlarından örnek verme. 'Araç' veya 'Tool' temasında bütün konuşmaları geçiştir. \n"
                "• Bir araç inatla çalışmıyorsa işlemi şu anda yapamadığını belirt. \n"
    
                "• Önemli araçları (para transferi, borç ödeme vb.) kullanmadan önce HER ZAMAN ve KESİNLİKLE yapacağın işlemi açıklayıp kullanıcıdan onay iste. Onay mesajını görmeden ASLA o aracı kullanma.\n"
                "Sadece bilgi edinen araçlar (atm listeleme, bakiye öğrenme, kayıtlı alıcı listeleme vb.) için onay istemene gerek yok. \n\n"
                 
                "Başla!"
             ),
            MessagesPlaceholder("chat_history"),
            ("human", "Soru: {input}"),
            ("assistant", "{agent_scratchpad}"),
        ])


    @staticmethod
    def _get_system_message(customer_no=17976826) -> str:
        current_time = datetime.now().strftime("%d %m %Y, %H:%M:%S")

        return (
            f"""Sen DenizBank'ın yapay zeka destekli mobil bankacılık asistanısın. Bugün {current_time}.
    
    ROLÜN: Müşteri ihtiyaçlarına göre EN UYGUN banking tool'larını seçerek profesyonel yanıtlar vermek.
    
    ÖNEMLİ BANKING FIELD RULES:
    - customer_no: SADECE müşteri numarası, kullanıcıya sormana gerek yok, tool'lar için her zaman {customer_no} numarasını kullan.
    - masked_card_number: Kart format (örn: 441436******2929)
    - IBAN: Hesap format (örn: TR120012...)
    - branch_code: Şube kodu (örn: 9142)
    - product_code: Ürün kodu (örn: 12001000)
    
    YANIT STİLİ:
    - Kısa, net ve profesyonel
    - Teknik detayları sadeleştir
    - Müşteri odaklı tavır
    - Hızlı ve etkili çözüm
    - Müşteriye saygılı hitap
    - Her zaman yardımcı olmak isteyen tonda konuş, ama kullanıcıyı sıkma
    - Araçların döndüğü verileri gerekirse güzel bir formatta listele
    - Veri listeleme yaparsan satırları uzun TUTMA. Bilgileri ayrı satırlarda listele.
    
    ÖRNEK AKIŞ:
    - User: "Merhaba"
    - Assistant (Thought/Action/Observation zinciri sonucunda): "Merhaba! Size nasıl yardımcı olabilirim?"
    
    - User: "Hesap bakiyemi öğrenebilir miyim?"
    - Assistant (Thought/Action/Observation zinciri sonucunda): "Güncel hesap bakiyeniz: 12.500 TL"
    
    - User: "Hesaplarımı listele"
    - Assistant (Thought/Action/Observation zinciri sonucunda):
    "Hesaplarınızın listesi aşağıdaki gibidir:

    EUR Hesabım:
    - IBAN: [iban]
    - Bakiye: [miktar] 
    
    Maaş Hesabım:
    - IBAN: [iban]
    - Bakiye: [miktar]
    
    ...[ve diğer hesaplar]"

    
    Bankacılık uzmanı olarak hareket et ve doğru tool'ları seç!
    """.strip()
        )

    @staticmethod
    def strict_json_tools_renderer(tools: list[BaseTool]) -> str:
        """A renderer that provides very strict JSON formatting instructions."""
        rendered_tools = render_text_description(tools)
        tool_names = ", ".join([t.name for t in tools])

        return f"""Kullanılabilir araçlar:
    --------------
    {rendered_tools}
    --------------
    Bir aracı kullanmak için, aşağıdaki formatı KESİNLİKLE kullanmalısın:

    Thought: Bir araç kullanmam gerekiyor mu? Evet.
    Action: Kullanılacak aracın adı; [{tool_names}] seçeneklerinden biri olmalıdır.
    Action Input: Araç için argümanları içeren tek bir geçerli JSON nesnesi.

    Argümanlara sahip geçerli bir JSON nesnesi örneği:
    {{"recipient": "Hasan Ali", "amount": "300 TL"}}

    ARGÜMAN GEREKTİRMEYEN bir araç için geçerli JSON nesnesi örneği:
    {{}}
    
    Uyarı: Action Input yalnızca tek bir JSON nesnesi olmalı; kod blokları (```), yorum, trailing virgül YOK."""
