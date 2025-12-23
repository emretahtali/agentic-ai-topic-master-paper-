from langchain_core.language_models.chat_models import BaseChatModel

from llm.client_types import (
    get_llm_openai,
    get_llm_gemini,
    get_llm_topic_master,
    get_llm_diagnosis,
    get_llm_appointment,
)
from llm.models import LLMModel


def get_llm(llm_type: LLMModel = LLMModel.GEMINI) -> BaseChatModel:
    if llm_type == LLMModel.TOPIC_MASTER:
        return get_llm_topic_master()

    if llm_type == LLMModel.DIAGNOSIS:
        return get_llm_diagnosis()

    if llm_type == LLMModel.APPOINTMENT:
        return get_llm_appointment()

    if llm_type == LLMModel.GEMINI:
        return get_llm_gemini()

    return get_llm_openai()
