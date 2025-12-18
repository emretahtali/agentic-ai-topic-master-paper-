from enum import StrEnum, auto
from langgraph.graph import START, END


class Routes(StrEnum):
    START = START
    END = END

    PRE_PROCESSING = auto()
    ASSISTANT = auto()
    TOOLS = auto()
    POST_PROCESSING = auto()
