#!/usr/bin/env python3

import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.generate_audio import generate_audio_for_sample_dir

def main(args):
    base_dir = args.subcategory_dir
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Directory not found: {base_dir}")

    sample_folders = [
        os.path.join(base_dir, d)
        for d in sorted(os.listdir(base_dir))
        if d.startswith("sample_") and os.path.isdir(os.path.join(base_dir, d))
    ]

    if not sample_folders:
        print(f"No sample folders found in: {base_dir}")
        return

    for folder in sample_folders:
        try:
            print(f"\n🔊 Generating audio for: {folder}")
            generate_audio_for_sample_dir(folder, voice=args.voice)
        except Exception as e:
            print(f"❌ Failed for {folder}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subcategory_dir", type=str, required=True, help="Path to subcategory dir like data/lexical_stress_shift")
    parser.add_argument("--voice", type=str, default="alloy", help="Voice to use for TTS")
    args = parser.parse_args()

    main(args)
