from __future__ import annotations

from llm import appointment_llm
from mcp_client import appointment_mcp

from langchain_core.messages.system import SystemMessage

from agentic_network.core import AgentState
from src.agentic_network.agents.agent import Agent
from src.agentic_network.helper.initialize_slots import create_initial_appointment_state


class AppointmentAgent(Agent):
    def __init__(self):
        # self.tools = mcp_client.get_tools()
        self.tools = appointment_mcp.get_tools()
        # self.model = llm_client.bind_tools(self.tools)
        self.model = appointment_llm.bind_tools(self.tools)

    async def _get_node(self, state: AgentState) -> dict:
        messages = state["messages"]
        
        app_data = state.get("appointment_data") or create_initial_appointment_state()
        
        # Slot summary
        slots_summary = "\n".join([
            f"- {k}: {v['value'] if v['value'] else 'EKSİK'} (Durum: {v['status']})"
            for k, v in app_data["slots"].items()
        ])

        system_msg = SystemMessage(
            content=f"""
# ROL
Sen uzman bir Hastane Randevu Asistanısın. Kullanıcıdan randevu bilgilerini toplamakla görevlisin.

# MEVCUT RANDEVU DURUMU
{slots_summary}

# KRİTİK HEDEF
Şu an odaklanman gereken adım: **{app_data['flow']['current_step']}**

# İŞLEYİŞ KURALLARI
1. **Veri Girişi:** Kullanıcıdan randevu ile ilgili herhangi bir bilgi (TC, şehir, doktor vb.) aldığında VEYA kullanıcı bir bilgiyi düzelttiğinde, VAKİT KAYBETMEDEN `update_appointment_slots` aracını çağır.
2. **Hata Yakalama (INVALID):**
   - Eğer bir slotun durumu `invalid` ise (Örn: TC hatalı), kullanıcıya "TC kimlik numaranız 11 haneli olmalıdır, lütfen kontrol edip tekrar iletebilir misiniz?" gibi bilgilendirici bir geri bildirim ver.
3. **Zeki Hafıza (Pending):**
   - Kullanıcı henüz sırası gelmeyen bir bilgi paylaşırsa endişelenme, tool bunu `pending_slots` içine alacaktır. Sen sadece akışı bozmadan bir sonraki adımı sormaya devam et.
4. **Onay Mekanizması:**
   - `current_step` "onay" olduğunda, tüm bilgileri (Şehir, Hastane, Doktor, Tarih/Saat) bir liste halinde özetle ve kullanıcıdan "Onaylıyor musunuz?" diye sor.
5. **Kısıtlamalar:**
   - TC Kimlik 11 hane ve sadece rakam olmalı.
   - Randevu dışı konularda nazikçe sürece geri dön.

# ÜSLUP
Robotik olma. "TC kimlik numaranızı alabilir miyim?" gibi nazik ve yardımsever bir ton kullan.
"""
        )

        # call model
        response = self.model.invoke([system_msg] + messages)
        
        # return back the appointment data to llm
        return {
            "messages": [response],
            "appointment_data": app_data,
            "active_agent": "appointment_agent"
        }