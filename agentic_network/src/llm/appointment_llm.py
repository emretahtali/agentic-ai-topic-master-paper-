import os
from dotenv import load_dotenv, find_dotenv

from llm import get_llm
from llm.llm_client import LLMModel

load_dotenv(find_dotenv())
# .env den APPOINTMENT_LLM_TYPE den GEMINI veya OPENAI seçilebilir.
llm_type_str = os.getenv("APPOINTMENT_LLM_TYPE", "GEMINI").upper().strip()
llm_type = LLMModel[llm_type_str]

# buraya .env değiştirilip asıl open ai gelebilir.
if llm_type == LLMModel.OPENAI:
    llm_key = os.getenv("DIAGNOSIS_LLM_API_KEY").strip()
    llm_endpoint = os.getenv("DIAGNOSIS_LLM_API_ENDPOINT").strip()
    model_name = os.getenv("DIAGNOSIS_LLM_MODEL_NAME", "gpt-4o").strip()
else:
    llm_key = os.getenv("GEMINI_APPOINTMENT_KEY").strip()
    llm_endpoint = os.getenv("GEMINI_APPOINTMENT_ENDPOINT").strip()
    model_name = os.getenv("GEMINI_APPOINTMENT_MODEL", "gemini-2.5-flash").strip()

appointment_llm = get_llm(llm_type=llm_type, llm_endpoint=llm_endpoint, llm_key=llm_key, model_name=model_name)

if __name__ == "__main__":
    print(appointment_llm.dict())