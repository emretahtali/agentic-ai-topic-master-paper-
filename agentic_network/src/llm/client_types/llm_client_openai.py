import os

from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


def get_llm_openai() -> ChatOpenAI:
    load_dotenv(find_dotenv())

    llm_endpoint = os.getenv("OPENAI_API_ENDPOINT").strip()
    llm_key = os.getenv("OPENAI_API_KEY").strip()
    llm_model_name = os.getenv("OPENAI_API_MODEL").strip()

    return ChatOpenAI(
        model=llm_model_name,
        base_url=llm_endpoint,
        api_key=llm_key,
    )
