from openai import BaseModel
from benchmark.dataset.intent_data import intent_literal


class ResultInfo(BaseModel):
    extracted_intent: intent_literal