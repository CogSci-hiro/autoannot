from pathlib import Path
from typing import Dict

from .transcribe_whisper import transcribe_whisper


def transcribe(in_file: str | Path, out_file: str | Path, params: Dict):

    backend = params["transcription"]["backend"]
    if backend == "whisper":
        transcribe_whisper(in_file, out_file, **params["transcription"]["whisper"])
    else:
        NotImplementedError(f"Backend '{backend}' is not implemented")
