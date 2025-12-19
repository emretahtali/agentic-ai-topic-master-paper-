from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm_gemini(llm_key: str = "") -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=llm_key,
    )
