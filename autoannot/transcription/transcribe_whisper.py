from pathlib import Path
from typing import Dict
import warnings

import pandas as pd
import torch
import whisper
import whisper_timestamped

# UserWarning: FP16 is not supported on CPU; using FP32 instead
warnings.filterwarnings(action="ignore", category=UserWarning)


def transcribe_whisper(in_file: str | Path, out_file: str | Path, model: str, use_cuda: bool):

    # Load model
    model = whisper.load_model(model)

    # Use CUDA
    if torch.cuda.is_available() and use_cuda:
        model.to(torch.device("cuda"))

    # Transcribe
    results = whisper_timestamped.transcribe(model, audio=str(in_file))  # noqa

    # Convert to standard format and save
    results = _convert_to_dataframe(results)
    results.to_csv(out_file, index=False)


def _convert_to_dataframe(transcription: Dict) -> pd.DataFrame:

    results = {"tier": [], "start": [], "end": [], "annotation": []}
    for segment in transcription["segments"]:

        for word in segment["words"]:

            results["tier"].append("transcription")
            results["start"].append(word["start"])
            results["end"].append(word["end"])
            results["annotation"].append(word["text"])

    results = pd.DataFrame(results)
    return results
