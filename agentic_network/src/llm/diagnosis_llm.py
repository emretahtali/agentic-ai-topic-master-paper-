import os
from dotenv import load_dotenv, find_dotenv

from llm import get_llm
from llm.llm_client import LLMModel

load_dotenv(find_dotenv())

llm_endpoint = os.getenv("DIAGNOSIS_LLM_API_ENDPOINT").strip()
llm_key = os.getenv("DIAGNOSIS_LLM_API_KEY").strip()
llm_type = LLMModel(os.getenv("DIAGNOSIS_LLM_TYPE", LLMModel.GEMINI))
model_name = os.getenv("DIAGNOSIS_LLM_MODEL_NAME", "gemini-2.5-flash").strip()

diagnosis_llm = get_llm(llm_type=llm_type, llm_endpoint=llm_endpoint, llm_key=llm_key, model_name=model_name)
