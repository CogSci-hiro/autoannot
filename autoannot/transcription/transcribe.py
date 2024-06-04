from pathlib import Path
from typing import Dict

from .transcribe_whisper import transcribe_whisper
from .clean_transcription import clean_transcription


def transcribe(in_file: str | Path, out_file: str | Path, dia_file: str | Path, params: Dict):

    backend = params["transcription"]["backend"]

    if backend == "whisper":
        df = transcribe_whisper(in_file, dia_file, **params["transcription"]["whisper"])
    else:
        raise NotImplementedError(f"Backend '{backend}' is not implemented")

    df = clean_transcription(df, empty=params["transcription"]["empty"])

    df.to_csv(out_file)
