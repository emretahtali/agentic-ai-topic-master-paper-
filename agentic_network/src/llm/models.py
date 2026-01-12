from enum import auto, StrEnum


class LLMModel(StrEnum):
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
    DEEPINFRA = "DEEPINFRA"

    TOPIC_MASTER = "TOPIC_MASTER"
    DIAGNOSIS = "DIAGNOSIS"
    APPOINTMENT = "APPOINTMENT"
