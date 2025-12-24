import asyncio
import os
import re
from datetime import datetime
from typing import Optional, Literal, List, Dict, Any

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


class TopicMasterBenchmarkTemplate:
    GREEN, RED, CYAN, YELLOW, RESET = "\033[92m", "\033[91m", "\033[96m", "\033[93m", "\033[0m"

    def __init__(
            self,
            result_schema: Any,
            concurrency: int = 5,
    ):
        self.result_schema = result_schema
        self.concurrency = concurrency

        self.logs = []
        self.print_lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(self.concurrency)

    @staticmethod
    def _parse_intent(resp: Dict) -> str:
        structured = resp.get("structured_response")
        return structured.extracted_intent.strip() if structured else "UNKNOWN"

    async def _process_dialogue(self, dialog: Dict):
        async with self.semaphore:
            chat_history, correct_count, user_msg_count = [], 0, 0
            terminal_output = []
            dialog_id = dialog['dialogue_id']

            terminal_output.append(f"{self.CYAN}\n{'=' * 20} DIALOGUE {dialog_id} {'=' * 20}{self.RESET}")

            try:
                agent = None # TODO: TODO

                for msg in dialog["messages"]:
                    role = "user" if msg["role"] == "user" else "assistant"
                    current_msg = {"role": role, "content": msg["message"]}

                    if msg["role"] == "user":
                        user_msg_count += 1

                        result = agent.invoke(message=current_msg["content"])

                        pred = self._parse_intent(result)
                        truth = msg["intent"].strip()
                        is_correct = pred.lower() == truth.lower()

                        if is_correct: correct_count += 1

                        color = self.GREEN if is_correct else self.RED
                        terminal_output.append(f"{self.YELLOW}User:{self.RESET} {msg['message']}")
                        terminal_output.append(f"{color}└─ Pred: {pred} | True: {truth} {self.RESET}")
                    else:
                        terminal_output.append(f"{self.CYAN}AI:{self.RESET} {msg['message']}")

                    chat_history.append(current_msg)

            except Exception as e:
                terminal_output.append(f"{self.RED}Error in Dialogue {dialog_id}: {e}{self.RESET}")

            async with self.print_lock:
                for line in terminal_output: print(line)
                self.logs.extend(terminal_output)

            return correct_count, user_msg_count

    async def run(self, dataset: List[Dict]):
        print(f"{self.CYAN}--- Test Started | Model: {self.model_name} | Tip: {self.llm_type} ---{self.RESET}")

        tasks = [self._process_dialogue(d) for d in dataset]
        results = await asyncio.gather(*tasks)

        total_correct = sum(r[0] for r in results)
        total_msgs = sum(r[1] for r in results)
        accuracy = total_correct / total_msgs if total_msgs else 0

        self._save_to_file(accuracy)

        print(f"\n{self.CYAN}{'=' * 50}{self.RESET}")
        print(f"{self.GREEN if accuracy > 0.8 else self.RED}FINAL ACCURACY: {accuracy:.4f}{self.RESET}")
        return accuracy

    def _save_to_file(self, accuracy: float):
        safe_name = self.model_name.replace(":", "_").replace("/", "_")
        os.makedirs("io/output_files", exist_ok=True)
        path = f"io/output_files/{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Model: {self.model_name}\nType: {self.llm_type}\nAccuracy: {accuracy:.4f}\n\n")
            for entry in self.logs:
                f.write(ansi_escape.sub('', entry) + "\n")
        print(f"{self.CYAN}Saved at:{self.RESET} {path}")