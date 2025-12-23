import json
import os
from loguru import logger


def extract_unique_intents(file_paths):
    intents = set()

    for file_path in file_paths:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                schema_data = json.load(f)
                logger.info(f"Loaded {file_path} with {len(schema_data)} services.")

                for service in schema_data:
                    for intent in service.get('intents', []):
                        intents.add(intent['name'])

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON in {file_path}: {e}")

    return sorted(list(intents))


def save_labels_to_file(labels, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for label in labels:
                f.write(f"{label}\n")
        logger.info(f"Saved {len(labels)} labels to '{output_path}'.")
    except IOError as e:
        logger.error(f"Error saving file: {e}")


def read_labels_from_file(input_path):
    if not os.path.exists(input_path):
        logger.error(f"File not found: {input_path}")
        return []

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            labels = [line.strip() for line in f if line.strip()]
        logger.info(f"Read {len(labels)} labels from '{input_path}'.")
        return labels
    except IOError as e:
        logger.error(f"Error reading file: {e}")
        return []


if __name__ == "__main__":
    files_map = {'train_schema.json': 'train_intents.txt', 'test_schema.json': 'test_intents.txt'}

    for json_file, txt_file in files_map.items():
        logger.info(f"Processing {json_file}...")

        intents = extract_unique_intents([json_file])

        if intents:
            save_labels_to_file(intents, txt_file)

            loaded_intents = read_labels_from_file(txt_file)

            if len(intents) == len(loaded_intents):
                logger.info(f"Save operation successful for {txt_file}.")
            else:
                logger.error(f"Save operation failed for {txt_file}: Count mismatch.")
        else:
            logger.warning(f"No intents extracted from {json_file}.")

    all_intents = set(read_labels_from_file('train_intents.txt') + read_labels_from_file('test_intents.txt'))
    print(len(all_intents))