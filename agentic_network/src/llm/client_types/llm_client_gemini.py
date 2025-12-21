from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm_gemini(llm_key: str, model_name:str = "gemini-2.5-flash") -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model_name,
        api_key=llm_key,
        # convert_system_message_to_human=True
    )
