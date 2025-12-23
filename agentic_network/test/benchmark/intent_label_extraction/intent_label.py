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
    # Define directories
    INPUT_DIR = '../io/input_files'
    OUTPUT_DIR = '../io/output_files'

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Map input schema filenames to desired output text filenames
    files_map = {'train_schema.json': 'train_intents.txt', 'test_schema.json': 'test_intents.txt'}

    generated_files = []

    for json_filename, txt_filename in files_map.items():
        # Construct full paths
        input_path = os.path.join(INPUT_DIR, json_filename)
        output_path = os.path.join(OUTPUT_DIR, txt_filename)

        logger.info(f"Processing {input_path}...")

        # Extract
        intents = extract_unique_intents([input_path])

        if intents:
            # Save
            save_labels_to_file(intents, output_path)
            generated_files.append(output_path)

            # Verify
            loaded_intents = read_labels_from_file(output_path)

            if len(intents) == len(loaded_intents):
                logger.info(f"Save operation successful for {txt_filename}.")
            else:
                logger.error(f"Save operation failed for {txt_filename}: Count mismatch.")
        else:
            logger.warning(f"No intents extracted from {json_filename}.")

    # Final Aggregation Check
    # Reading back the files we just created in the output directory
    train_intents_path = os.path.join(OUTPUT_DIR, 'train_intents.txt')
    test_intents_path = os.path.join(OUTPUT_DIR, 'test_intents.txt')

    all_intents = set()

    if os.path.exists(train_intents_path):
        all_intents.update(read_labels_from_file(train_intents_path))

    if os.path.exists(test_intents_path):
        all_intents.update(read_labels_from_file(test_intents_path))

    logger.info(f"Total unique intents across all files: {len(all_intents)}")