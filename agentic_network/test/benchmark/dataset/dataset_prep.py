import json
import os
from loguru import logger

def reformat_dialogues(input_paths, output_path):

    processed_dialogues = []

    for input_path in input_paths:
        if not os.path.exists(input_path):
            logger.warning(f"Input file not found: {input_path}")
            continue

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            for dialogue in raw_data:
                dialogue_id = dialogue.get('dialogue_id')
                raw_messages = dialogue.get('turns', [])

                structured_messages = []

                for turn in raw_messages:
                    speaker = turn.get('speaker')
                    text = turn.get('utterance')

                    if speaker == "USER":
                        frames = turn.get('frames', [])
                        active_intent = "NONE"

                        if frames:
                            state = frames[0].get('state', {})
                            active_intent = state.get('active_intent', "NONE")

                        structured_messages.append({"role": "user", "message": text, "intent": active_intent})

                    elif speaker == "SYSTEM":
                        structured_messages.append({"role": "ai", "message": text})

                dialogue_len = len(structured_messages)

                processed_dialogues.append({"dialogue_id": dialogue_id, "length": dialogue_len,
                    "messages": structured_messages})

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {input_path}: {e}")
        except IOError as e:
            logger.error(f"File I/O error for {input_path}: {e}")

    if processed_dialogues:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_dialogues, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved {len(processed_dialogues)} dialogues to {output_path}")
        except IOError as e:
            logger.error(f"Error saving output file: {e}")
    else:
        logger.warning("No dialogues processed; output file not created.")


def read_dataset(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return []


def extract_intents_from_dataset(data):
    unique_intents = set()

    for dialogue in data:
        for message in dialogue.get('messages', []):
            intent = message.get('intent')
            if intent:
                unique_intents.add(intent)

    # Sort alphabetically
    sorted_intents = sorted(list(unique_intents))

    print("\n--- Extracted Intents ---")
    for label in sorted_intents:
        print(label)

    return sorted_intents


if __name__ == "__main__":
    INPUT_DIR = '../io/input_files'
    OUTPUT_DIR = '../io/output_files'
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    N_FILES = 34

    input_files = [os.path.join(INPUT_DIR, f"dialogues_{i:03d}.json") for i in range(1, N_FILES + 1)]

    output_file = os.path.join(OUTPUT_DIR, 'dataset.json')

    reformat_dialogues(input_files, output_file)

    dataset = read_dataset(output_file)

    logger.info(f"Number of dialogues: {len(dataset)}")

    n_messages = sum(dialogue["length"] for dialogue in dataset)
    logger.info(f"Total messages across all dialogues: {n_messages}")

    if dataset:
        first_dialogue = dataset[0]
        dialogue_id = first_dialogue.get('dialogue_id')
        messages = first_dialogue.get('messages', [])

        logger.info(f"--- First 10 messages of Dialogue {dialogue_id} ---")
        for i, message in enumerate(messages[:10]):
            role = message['role'].upper()
            msg = message['message']
            intent = message.get('intent', '')

            log_msg = f"[{i + 1}] {role}: {msg}"
            if intent:
                log_msg += f" (Intent: {intent})"

            logger.info(log_msg)

        extract_intents_from_dataset(dataset)
    else:
        logger.warning("No data found to verify.")