from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm_gemini(llm_key: str = "") -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=llm_key,
        # convert_system_message_to_human=True
    )
