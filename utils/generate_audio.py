# utils/generate_audio.py

import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

def tts_call(text, voice, instructions, out_path):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        instructions=instructions,
        response_format="wav"
    )
    with open(out_path, "wb") as f:
        f.write(response.content)
    print(f"✅ Saved: {out_path}")

def generate_audio_for_sample_dir(sample_dir, voice="ash"):
    meta_path = os.path.join(sample_dir, "meta.json")
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"No meta.json found in: {sample_dir}")

    with open(meta_path) as f:
        data = json.load(f)

    input_text = data["input_text"]
    input_instructions = data["input_instructions_per_option"]
    options = data["options_text"]
    option_instructions = data["options_instructions"]

    assert len(input_instructions) == len(options) == len(option_instructions), \
        "Mismatched input/options/instructions lengths"

    for i, (instr, opt, opt_instr) in enumerate(zip(input_instructions, options, option_instructions)):
        input_out_path = os.path.join(sample_dir, f"target{i+1}.wav")
        option_out_path = os.path.join(sample_dir, f"option{i+1}.wav")

        tts_call(input_text, voice, instr, input_out_path)
        tts_call(opt, voice, opt_instr, option_out_path)

