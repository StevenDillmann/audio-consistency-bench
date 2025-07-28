# utils/generate_check.py

import os
import json
import hashlib
from dotenv import load_dotenv
load_dotenv()
import openai
import re


def load_prompt_template(prompt_path):
    with open(prompt_path) as f:
        template = f.read()
    return template

def get_sample_hash(sample):
    key = sample["input_text"] + " ".join(sample["options_text"])
    return hashlib.sha256(key.encode()).hexdigest()

def parse_json_response(response):
    try:
        start = response.index("{")
        return json.loads(response[start:])
    except Exception as e:
        print(f"❌ Failed to parse GPT output: {e}")
        return None
    
def parse_json_response(response):
    try:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found.")

        json_str = match.group(0)

        # Load only the first JSON object, allow trailing text
        decoder = json.JSONDecoder()
        parsed, _ = decoder.raw_decode(json_str)

        return parsed

    except Exception as e:
        print("❌ Failed to parse GPT output:", e)
        print("↪ Response was:\n", response[:500], "...\n")  # preview the output
        return None
    

def generate_gpt_sample(prompt, model="gpt-4o"):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for generating structured dataset samples."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def get_next_sample_id(data_dir):
    existing = [
        d for d in os.listdir(data_dir)
        if d.startswith("sample_") and os.path.isdir(os.path.join(data_dir, d))
    ]
    if not existing:
        return 1
    ids = [int(d.split("_")[1]) for d in existing]
    return max(ids) + 1

def save_sample_json(sample, out_dir, sample_id):
    sample_folder = os.path.join(out_dir, f"sample_{sample_id:04d}")
    os.makedirs(sample_folder, exist_ok=True)
    out_path = os.path.join(sample_folder, "meta.json")
    with open(out_path, "w") as f:
        json.dump(sample, f, indent=2)
    print(f"✅ Saved: {out_path}")

def generate_unique_sample(prompt_template, seen_hashes, output_dir):
    full_prompt = prompt_template + "\n\nMake sure the example is distinct."
    response = generate_gpt_sample(full_prompt)
    sample = parse_json_response(response)
    if not sample:
        return None, None

    sample_hash = get_sample_hash(sample)
    if sample_hash in seen_hashes:
        print("⚠️ Duplicate detected. Skipping.")
        return None, None

    seen_hashes.add(sample_hash)
    with open(os.path.join(output_dir, "seen_hashes.txt"), "a") as f:
        f.write(sample_hash + "\n")

    sample_id = get_next_sample_id(output_dir)
    save_sample_json(sample, output_dir, sample_id)

    return sample, sample_id

