from langchain.agents import create_react_agent
from langchain_core.runnables import Runnable
from langchain.schema import OutputParserException


def create_custom_react_agent(llm, tools, prompt, parser, tools_renderer, retries=2) -> Runnable:
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
        output_parser=parser,
        tools_renderer=tools_renderer
    )
    # Retry only when the parser actually throws (malformed structure/tool call)
    agent = agent.with_retry(
        stop_after_attempt=retries,
        retry_if_exception_type=(OutputParserException,),
    )
    return agent
