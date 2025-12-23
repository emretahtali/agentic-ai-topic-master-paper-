from datetime import datetime

from dotenv import load_dotenv, find_dotenv
import os

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from langchain.agents.structured_output import ProviderStrategy

import llm.client_types
from benchmark.core import ResultInfo
from benchmark.dataset import intent_list, dataset

from benchmark.dataset import read_dataset

#intent_tuple = tuple(intent_list)
#IntentLiteral = Literal[*intent_tuple]

load_dotenv(find_dotenv())
API_KEY = os.getenv("APPOINTMENT_LLM_API_KEY")

model = llm.client_types.get_llm_gemini(llm_key= API_KEY, model_name= "gemini-2.5-flash")

agent = create_agent(
    model=model,
    response_format=ProviderStrategy(ResultInfo),
    system_prompt=SystemMessage(content=f"""\
### ROLE
You are a highly accurate Intent Classification specialist. Your task is to analyze a conversation and identify the specific intent of the LAST user message.

### CONTEXT & TOPIC TRACKING
- **Conversation Thread:** You will receive a list of messages. The dialogue represents a continuous task (e.g., booking a ticket, finding a house).
- **Core Task:** Many user messages are short follow-ups (e.g., "Yes", "8 PM", "Near the park"). These messages INHERIT their intent from the ongoing topic established earlier in the chat.
- **Ambiguity Resolution:** If the last message is vague, you MUST look at the preceding messages to identify what service or object is being discussed.

### GUIDELINES
1. **Focus:** Categorize ONLY the last message from the user.
2. **Contextual Awareness:** If the last message is a follow-up (e.g., "8 PM", "In London", "Yes"), use the preceding dialogue to determine the correct intent from the list.
3. **Intent List:** You must choose exactly one intent from this list:
    
{intent_list}

### OUTPUT FORMAT
Return ONLY a valid JSON object. Do not include any explanations or markdown formatting outside the JSON.
Schema: {{ "extracted_intent": "<chosen_intent>" }}\
"""
))



def parse_intent(resp) -> str:
    structured = resp.get("structured_response")
    if structured:
        return structured.extracted_intent
    return ""


def evaluate_intent_accuracy(agent, dataset):
    correct = 0
    total = 0

    GREEN = "\033[92m"
    RED   = "\033[91m"
    RESET = "\033[0m"

    for dialog in dataset:
        print(f"\n--- Dialogue ID: {dialog['dialogue_id']} ---")
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
                gt_intent   = ground_truth.strip()

                is_correct = pred_intent.lower() == gt_intent.lower()
                if is_correct:
                    correct += 1

                # Anlık accuracy
                accuracy_now = correct / total if total else 0

                # Renk seçimi
                color = GREEN if is_correct else RED

                # Yazdır
                print(f"User: {user_text}")
                print(f"{color}Pred: {pred_intent} | True: {gt_intent}{RESET}")
                print(f"[{total} messages] Current Accuracy: {accuracy_now:.4f}\n")

            chat_history.append(current_message)

    final_accuracy = correct / total if total else 0
    return {"total": total, "correct": correct, "accuracy": final_accuracy}


def test_intent_pipeline():
    # mock dataset


    results = evaluate_intent_accuracy(agent, dataset)

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

    print(f"Results saved to: {path}")

test_intent_pipeline()


#edge case

"""
{
            "dialogue_id": "2",
            "messages": [
                {"role": "user", "message": "I need to find a place to stay in Paris.", "intent": "BookHouse"},
                {"role": "ai", "message": "What is your budget per night?"},
                {"role": "user", "message": "Around 150 Euros.", "intent": "BookHouse"},
                {"role": "ai", "message": "I found 3 apartments. Would you like to see them?"},
                {"role": "user", "message": "Yes, show me the details.", "intent": "BookHouse"}
            ]
        }
"""

