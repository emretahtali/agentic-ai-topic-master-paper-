from dotenv import load_dotenv, find_dotenv
import os

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from langchain.agents.structured_output import ProviderStrategy

import llm.client_types
from benchmark.core import ResultInfo
from benchmark.data import intent_list

#intent_tuple = tuple(intent_list)
#IntentLiteral = Literal[*intent_tuple]

load_dotenv(find_dotenv())
API_KEY = os.getenv("APPOINTMENT_LLM_API_KEY")

model = llm.client_types.get_llm_gemini(llm_key= API_KEY, model_name= "gemini-2.5-flash")

agent = create_agent(
    model=model,
    response_format=ProviderStrategy(ResultInfo),
    system_prompt=SystemMessage(content=f"""
    ### ROLE
    You are a highly accurate Intent Classification specialist. Your task is to analyze a conversation and identify the specific intent of the LAST user message.

    ### CONTEXT
    You will be provided with a conversation history. Use this history to resolve ambiguities. For example, if the user says "Yes, book it," look at the previous AI messages to understand WHAT is being booked (a bus ticket, a movie, etc.).

    ### GUIDELINES
    1. **Focus:** Categorize ONLY the last message from the user.
    2. **Contextual Awareness:** If the last message is a follow-up (e.g., "8 PM", "In London", "Yes"), use the preceding dialogue to determine the correct intent from the list.
    3. **Intent List:** You must choose exactly one intent from this list:
    {intent_list}

    ### OUTPUT FORMAT
    Return ONLY a valid JSON object. Do not include any explanations or markdown formatting outside the JSON.
    Schema: {{ "extracted_intent": "<chosen_intent>" }}
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

                pred_intent = parse_intent(result)

                if pred_intent.strip().lower() == ground_truth.strip().lower():
                    correct += 1

                print(f"User: {user_text}")
                print(f"Pred: {pred_intent} | True: {ground_truth}")

            chat_history.append(current_message)

    accuracy = correct / total if total else 0
    return {"total": total, "correct": correct, "accuracy": accuracy}

def test_intent_pipeline():
    # mock dataset
    dataset = [
        {
            "dialogue_id": "1",
            "messages": [
                {"role": "user", "message": "I want to book a movie ticket for tonight.", "intent": "BuyMovieTickets"},
                {"role": "ai", "message": "Sure, which movie would you like to see?"},
                {"role": "user", "message": "The new Batman movie at around 8 PM please.", "intent": "BuyMovieTickets"}
            ]
        },
        {
            "dialogue_id": "3",
            "messages": [
                {"role": "user", "message": "Are there any buses to Istanbul this afternoon?", "intent": "FindBus"},
                {"role": "ai", "message": "There are buses at 2 PM and 5 PM. Should I book one?"},
                {"role": "user", "message": "Yes, buy a ticket for the 5 PM one.", "intent": "BuyBusTicket"}
            ]
        },
        {
            "dialogue_id": "4",
            "messages": [
                {"role": "user", "message": "Set an alarm for me.", "intent": "AddAlarm"},
                {"role": "ai", "message": "Of course, for what time?"},
                {"role": "user", "message": "7 AM sharp.", "intent": "AddAlarm"},
                {"role": "ai", "message": "Done. Anything else?"},
                {"role": "user", "message": "What other alarms do I have?", "intent": "GetAlarms"}
            ]
        },
        {
            "dialogue_id": "5",
            "messages": [
                {"role": "user", "message": "I'm looking for a nice Italian restaurant nearby.",
                 "intent": "FindRestaurants"},
                {"role": "ai", "message": "I found 'Bella Ciao' and 'Roma Kitchen'. Do you want to book a table?"},
                {"role": "user", "message": "Make a reservation at Bella Ciao for two.", "intent": "BookAppointment"}
            ]
        },
        {
            "dialogue_id": "6",
            "messages": [
                {"role": "user", "message": "I want to go to a concert this weekend.", "intent": "FindEvents"},
                {"role": "ai", "message": "There is a Rock Festival and a Jazz Night. Interested?"},
                {"role": "user", "message": "Get me two tickets for the Jazz Night.", "intent": "BuyEventTickets"}
            ]
        },
        {
            "dialogue_id": "7",
            "messages": [
                {"role": "user", "message": "Show me houses for rent in Kadıköy.", "intent": "FindHomeByArea"},
                {"role": "ai", "message": "I listed 5 houses. Do you want to see the cheapest one?"},
                {"role": "user", "message": "Actually, show me the ones with a balcony.", "intent": "FindHomeByArea"}
            ]
        },
        {
            "dialogue_id": "8",
            "messages": [
                {"role": "user", "message": "I need a ride to the airport.", "intent": "GetRide"},
                {"role": "ai", "message": "I can call a taxi. Do you want a standard or a VIP car?"},
                {"role": "user", "message": "Standard is fine, thanks.", "intent": "GetRide"}
            ]
        },
        {
            "dialogue_id": "9",
            "messages": [
                {"role": "user", "message": "Are there any trains to London tomorrow morning?", "intent": "FindTrains"},
                {"role": "ai", "message": "Yes, the first one is at 6:30 AM."},
                {"role": "user", "message": "What about the afternoon?", "intent": "FindTrains"}
            ]
        },
        {
            "dialogue_id": "10",
            "messages": [
                {"role": "user", "message": "I want to see some tourist attractions in Rome.",
                 "intent": "FindAttractions"},
                {"role": "ai", "message": "The Colosseum and Trevi Fountain are popular. Need more?"},
                {"role": "user", "message": "Are there any museums near the Colosseum?", "intent": "FindAttractions"}
            ]
        }
    ]

    results = evaluate_intent_accuracy(agent, dataset)

    print("--- Test Results ---")
    print("Total user messages:", results["total"])
    print("Correct predictions:", results["correct"])
    print("Accuracy:", results["accuracy"])

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

