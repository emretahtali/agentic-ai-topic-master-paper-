from enum import StrEnum, auto
from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv, find_dotenv
import os

from llm.client_types import get_llm_openai, get_llm_gemini


class LLMModel(StrEnum):
    GEMINI = auto()
    OPENAI = auto()


def get_llm(llm_type: LLMModel = LLMModel.GEMINI) -> BaseChatModel:
    load_dotenv(find_dotenv())
    llm_endpoint = os.getenv("LLM_API_ENDPOINT").strip()
    llm_key = os.getenv("LLM_API_KEY").strip()

    if llm_type is None:
        llm_type = os.getenv("LLM_API_TYPE").strip()

    if llm_type == "GEMINI":
        return get_llm_gemini(llm_key)

    return get_llm_openai(llm_endpoint, llm_key)
