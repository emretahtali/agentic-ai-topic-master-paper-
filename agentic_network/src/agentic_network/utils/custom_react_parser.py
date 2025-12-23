from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain.schema import OutputParserException
from typing import Union


class CustomReActParser(ReActSingleInputOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            return super().parse(text)

        except OutputParserException:
            cleaned = (text or "").strip()

            # If it's just free text (no Action: / Final Answer: scaffolding), treat as final
            if cleaned and "Action:" not in cleaned:
                return AgentFinish(return_values={"output": cleaned}, log=cleaned)

            # It's genuinely malformed (e.g. Action but bad JSON) -> let caller retry
            raise OutputParserException
