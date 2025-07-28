# scripts/generate_checks_batch.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import json
from utils.generate_check import (
    load_prompt_template,
    generate_unique_sample,
)

def main(args):
    with open(args.metadata) as f:
        metadata = json.load(f)

    prompt_template = load_prompt_template(metadata["prompt_file"])
    output_dir = metadata["data_folder"]
    os.makedirs(output_dir, exist_ok=True)

    hash_file = os.path.join(output_dir, "seen_hashes.txt")
    seen_hashes = set()
    if os.path.exists(hash_file):
        with open(hash_file) as f:
            seen_hashes = set(line.strip() for line in f)

    generated = 0
    retries = 0

    while generated < args.n_samples and retries < args.max_retries:
        sample, sample_id = generate_unique_sample(prompt_template, seen_hashes, output_dir)
        if sample is None:
            retries += 1
            continue
        generated += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=str, required=True, help="Path to subcategory metadata JSON")
    parser.add_argument("--n_samples", type=int, default=1, help="Number of unique prompt groups to generate")
    parser.add_argument("--max_retries", type=int, default=10, help="Maximum attempts to generate unique samples")
    args = parser.parse_args()
    main(args)
