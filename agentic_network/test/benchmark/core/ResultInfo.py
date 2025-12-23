from openai import BaseModel
from benchmark.data.intent_literal import intent_literal


class ResultInfo(BaseModel):
    extracted_intent: intent_literal