import os

from dotenv import load_dotenv, find_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from llm.models import LLMModel


def get_llm_diagnosis() -> BaseChatModel:
    load_dotenv(find_dotenv())

    llm_endpoint = os.getenv("DIAGNOSIS_LLM_API_ENDPOINT").strip()
    llm_key = os.getenv("DIAGNOSIS_LLM_API_KEY").strip()
    llm_model_name = os.getenv("DIAGNOSIS_LLM_MODEL_NAME", "gemini-2.5-flash").strip()
    llm_type_str = os.getenv("DIAGNOSIS_LLM_TYPE", LLMModel.GEMINI).upper().strip()
    llm_type = LLMModel[llm_type_str]

    if llm_type == LLMModel.GEMINI:
        return ChatGoogleGenerativeAI(
            model=llm_model_name,
            api_key=llm_key,
        )

    return ChatOpenAI(
        model=llm_model_name,
        base_url=llm_endpoint,
        api_key=llm_key,
    )


def test():
    llm = get_llm_diagnosis()
    response = llm.invoke("Hello pal!")
    print(f"{response.content=}")

if __name__ == "__main__":
    test()
