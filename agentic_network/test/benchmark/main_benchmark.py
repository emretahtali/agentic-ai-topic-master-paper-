import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from benchmark.agent import system_prompt
from benchmark.core import ResultInfo

from benchmark.dataset import dataset
from benchmark.util import BenchmarkTemplate
from benchmark.util.topic_master_benchmark_template import TopicMasterBenchmarkTemplate


async def main():
    load_dotenv(find_dotenv())

    PROVIDER = os.getenv("BENCHMARK_LLM_PROVIDER").lower()
    MODEL = os.getenv("BENCHMARK_LLM_MODEL")
    API_KEY = os.getenv("BENCHMARK_LLM_API_KEY")
    ENDPOINT = os.getenv("BENCHMARK_LLM_ENDPOINT")
    STRATEGY = os.getenv("BENCHMARK_LLM_STRATEGY").lower()

    # tester = BenchmarkTemplate(
    #     llm_type=PROVIDER,
    #     model_name=MODEL,
    #     api_key=API_KEY,
    #     system_prompt=system_prompt,
    #     result_schema=ResultInfo,
    #     endpoint=ENDPOINT,
    #     concurrency=5,
    #     strategy_type=STRATEGY
    # )
    tester = TopicMasterBenchmarkTemplate(
        concurrency=5,
    )

    await tester.run(dataset)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest kullanıcı tarafından durduruldu.")