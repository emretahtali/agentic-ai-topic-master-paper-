from enum import StrEnum, auto
from langgraph.graph import START, END


class TopicManagerRoutes(StrEnum):
    START = START
    NEXT = auto()
    END = END

    PRE_PROCESSING_AGENT = auto()
    POST_PROCESSING_AGENT = auto()
    TOPIC_CHANGE_CHECKER_AGENT = auto()
    PRE_TOPICS_AGENT = auto()
    NEW_TOPIC_AGENT = auto()
