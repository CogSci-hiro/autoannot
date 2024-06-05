from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import torch
from transformers import Wav2Vec2ForCTC, AutoProcessor

SR_RATE = 16_000


def transcribe_w2v2(in_file: str | Path, dia_file: str | Path,
                    model: str, use_cuda: bool) -> pd.DataFrame:

    data_list, dia_df = _make_cropped(in_file, dia_file)

    # Load model
    processor = AutoProcessor.from_pretrained(model)
    model = Wav2Vec2ForCTC.from_pretrained(model)

    processor.tokenizer.set_target_lang("fra")
    model.load_adapter("fra")

    idx = 0
    df = {"tier": [], "start": [], "end": [], "annotation": []}
    for _, row in dia_df.iterrows():

        if row["annotation"] == "#":
            transcription = "#"

        else:

            inputs = processor(data_list[idx], sampling_rate=SR_RATE, return_tensors="pt")

            with torch.no_grad():
                try:
                    outputs = model(**inputs).logits

                    ids = torch.argmax(outputs, dim=-1)[0]
                    transcription = processor.decode(ids)
                    print(transcription)
                    idx += 1

                # RuntimeError: Calculated padded input size per channel: (1). Kernel size: (2).
                # Kernel size can't be greater than actual input size
                except RuntimeError:
                    transcription = ""

        df["tier"].append("transcription")
        df["start"].append(row["start"])
        df["end"].append(row["end"])
        df["annotation"].append(transcription)

    df = pd.DataFrame(df)

    return df


def _make_cropped(audio_file, dia_file):

    data, sr = librosa.load(audio_file, sr=SR_RATE)
    if data.shape[0] == 2:  # stereo data
        data = data.mean(axis=0).astype(np.float32)

    df = pd.read_csv(dia_file)

    data_list = []
    for _, row in df.iterrows():

        if row["annotation"] == "#":
            continue

        # Get a segment of the audio
        start, end = int(row["start"] * sr), int(row["end"] * sr)
        data_list.append(data[start:end])

    return data_list, df
