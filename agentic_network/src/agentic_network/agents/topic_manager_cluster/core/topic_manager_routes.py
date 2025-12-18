from enum import StrEnum, auto
from langgraph.graph import START, END


class TopicManagerRoutes(StrEnum):
    START = START
    END = END

    TOPIC_CHANGE_CHECKER_AGENT = auto()
    PRE_TOPICS_AGENT = auto()
    NEW_TOPIC_AGENT = auto()
