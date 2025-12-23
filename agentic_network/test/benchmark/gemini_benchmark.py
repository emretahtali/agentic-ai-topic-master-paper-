from datetime import datetime

from dotenv import load_dotenv, find_dotenv
import os

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy

import llm.client_types
from benchmark.agent import system_prompt
from benchmark.core import ResultInfo
from benchmark.dataset import dataset

load_dotenv(find_dotenv())
API_KEY = os.getenv("APPOINTMENT_LLM_API_KEY")

model = llm.client_types.get_llm_gemini(llm_key= API_KEY, model_name= "gemini-2.5-flash")

agent = create_agent(
    model=model,
    response_format=ProviderStrategy(ResultInfo),
    system_prompt=system_prompt
)



def parse_intent(resp) -> str:
    structured = resp.get("structured_response")
    if structured:
        return structured.extracted_intent
    return ""


def evaluate_intent_accuracy(agent, dataset, logs):
    correct = 0
    total = 0

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    for dialog in dataset:
        header = f"\n--- Dialogue ID: {dialog['dialogue_id']} ---"
        print(header)
        logs.append(header)
        chat_history = []

        for msg in dialog["messages"]:
            role = "user" if msg["role"] == "user" else "assistant"
            current_message = {"role": role, "content": msg["message"]}

            if msg["role"] == "user":
                total += 1
                user_text = msg["message"]
                ground_truth = msg["intent"]

                result = agent.invoke({
                    "messages": chat_history + [current_message]
                })

                pred_intent = parse_intent(result).strip()
                gt_intent = ground_truth.strip()

                is_correct = pred_intent.lower() == gt_intent.lower()
                if is_correct:
                    correct += 1

                accuracy_now = correct / total if total else 0
                color = GREEN if is_correct else RED

                log_entry = (
                    f"User: {user_text}\n"
                    f"Pred: {pred_intent} | True: {gt_intent}\n"
                    f"[{total} messages] Current Accuracy: {accuracy_now:.4f}\n"
                )

                print(f"User: {user_text}")
                print(f"{color}Pred: {pred_intent} | True: {gt_intent}{RESET}")
                print(f"[{total} messages] Current Accuracy: {accuracy_now:.4f}\n")

                logs.append(log_entry)

            chat_history.append(current_message)

    final_accuracy = correct / total if total else 0
    return {"total": total, "correct": correct, "accuracy": final_accuracy}


def test_intent_pipeline():
    logs = []
    results = evaluate_intent_accuracy(agent, dataset, logs)

    model_name = "gemini-2.5-flash"
    safe_model_name = model_name.replace(":", "_").replace("/", "_")

    out_dir = "io/output_files"
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"{safe_model_name}_results_{timestamp}.txt"
    path = os.path.join(out_dir, out_file)

    with open(path, "w", encoding="utf-8") as f:
        f.write("--- Intent Pipeline Test Results ---\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Total user messages: {results['total']}\n")
        f.write(f"Correct predictions: {results['correct']}\n")
        f.write(f"Accuracy: {results['accuracy']:.4f}\n")
        f.write("\n" + "=" * 30 + "\n")
        f.write("DETAILED DIALOGUE LOGS\n")
        f.write("=" * 30 + "\n")

        for entry in logs:
            f.write(entry + "\n")

    print(f"Results saved to: {path}")

test_intent_pipeline()