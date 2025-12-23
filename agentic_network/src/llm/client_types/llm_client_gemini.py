import os

from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm_gemini(llm_key: str = "") -> ChatGoogleGenerativeAI:
    load_dotenv(find_dotenv())

    llm_endpoint = os.getenv("GEMINI_API_ENDPOINT").strip()
    llm_key = os.getenv("GEMINI_API_KEY").strip()
    llm_model_name = os.getenv("GEMINI_API_MODEL").strip()

    return ChatGoogleGenerativeAI(
        model=llm_model_name,
        api_key=llm_key,
    )
