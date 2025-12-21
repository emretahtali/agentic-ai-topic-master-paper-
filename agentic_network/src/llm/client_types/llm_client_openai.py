from langchain_openai import ChatOpenAI


def get_llm_openai(llm_endpoint, llm_key, model_name="default") -> ChatOpenAI:
    return ChatOpenAI(
        model=model_name,
        base_url=llm_endpoint,
        api_key=llm_key,
        # default_headers={"Content-Type": "application/json", "X-Custom": "value"}
    )
