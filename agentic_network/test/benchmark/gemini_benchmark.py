import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from benchmark.agent import system_prompt
from benchmark.core import ResultInfo

from benchmark.dataset import dataset
from benchmark.util import BenchmarkTemplate


async def main():
    load_dotenv(find_dotenv())

    PROVIDER = "google"
    MODEL = "gemini-2.5-flash"
    API_KEY = os.getenv("APPOINTMENT_LLM_API_KEY")
    ENDPOINT = None

    tester = BenchmarkTemplate(
        llm_type=PROVIDER,
        model_name=MODEL,
        api_key=API_KEY,
        system_prompt=system_prompt,
        result_schema=ResultInfo,
        endpoint=ENDPOINT,
        concurrency=5
    )

    await tester.run(dataset)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest kullanıcı tarafından durduruldu.")