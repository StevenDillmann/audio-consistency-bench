# audio-consistency-bench

AudioConsistencyBench is a dataset that tests whether models can use audio cues — such as stress, intonation, emotion, or background noise — to pick the correct continuation of a spoken sentence. Each sample includes a target audio sentence and multiple candidate follow-up audios, but only one continuation is logically consistent given how the sentence was spoken.

Without access to the audio (e.g. with a text-only model), all options appear equally plausible. The goal is to evaluate large audio models on their ability to resolve this ambiguity using sound alone.




python scripts/generate_checks_batch.py --metadata categories/lexical_stress_shift.json --n_samples 10

