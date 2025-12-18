from langchain_openai import ChatOpenAI


def get_llm_openai(llm_endpoint, llm_key) -> ChatOpenAI:
    return ChatOpenAI(
        model="default",
        base_url=llm_endpoint,
        api_key=llm_key,
        # default_headers={"Content-Type": "application/json", "X-Custom": "value"}
    )
