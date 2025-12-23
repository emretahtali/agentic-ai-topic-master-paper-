import os
from typing import Literal

from benchmark.dataset import read_dataset
from benchmark.dataset.dataset_prep import extract_intents_from_dataset


script_dir = os.path.dirname(os.path.realpath(__file__))
dataset_path = os.path.normpath(os.path.join(script_dir, "../io/output_files/dataset.json"))

dataset = read_dataset(dataset_path)

intent_list = extract_intents_from_dataset(dataset)
intent_tuple = tuple(intent_list)
intent_literal = Literal[*intent_tuple]