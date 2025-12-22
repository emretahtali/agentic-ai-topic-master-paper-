from enum import StrEnum, auto
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel


from llm.client_types import get_llm_openai, get_llm_gemini


class LLMModel(StrEnum):
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"


def get_llm(model_name:str, llm_key: str, llm_endpoint: Optional[str]="", llm_type: LLMModel = LLMModel.GEMINI) -> BaseChatModel:

    if llm_type == "GEMINI":
        return get_llm_gemini(llm_key, model_name=model_name)

    elif llm_type == "OPENAI":
        return get_llm_openai(llm_key=llm_key, llm_endpoint=llm_endpoint, model_name=model_name)

    return get_llm_openai(llm_key=llm_key, llm_endpoint=llm_endpoint, model_name=model_name)