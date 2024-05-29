import csv
from pathlib import Path
import re

import torch
import pandas as pd
from pyannote.audio import Pipeline

from autoannot.diarization import PYANNOT_MODEL


def diarize_pyannote(in_file: str | Path, out_file: str | Path, n_speakers: int,
                     auth_token: str, use_cuda: bool = True) -> None:

    # Load pretrained model
    pipeline = Pipeline.from_pretrained(checkpoint_path=PYANNOT_MODEL, use_auth_token=auth_token)

    # Use CUDA
    if torch.cuda.is_available() and use_cuda:
        pipeline.to(torch.device("cuda"))

    # Set maximum number of speakers
    n_speakers = 10 if n_speakers is None else n_speakers

    # Annotate
    diarization = pipeline(in_file, max_speakers=n_speakers)

    # Convert to familiar dataframe
    dia_df = _convert_to_df(str(diarization))
    dia_df.to_csv(out_file, index=False, header=False, quoting=csv.QUOTE_NONNUMERIC)

########################################################################################################################
# Private methods                                                                                                      #
########################################################################################################################


def _convert_to_df(diarization: str, tier_name: str = "pyannote"):

    results = {"tiers": [], "start": [], "end": [], "annotation": []}

    for line in diarization.splitlines():
        print(line)

        # e.g. [ 00:00:00.722 -->  00:00:03.372] A SPEAKER_01
        pattern = r"\[\s(\d{2}):(\d{2}):(\d+\.\d+)\s+-->\s+(\d{2}):(\d{2}):(\d+\.\d+)]\s\w+\s(SPEAKER_\d{2})"
        match = re.match(pattern, line)

        if not match:
            raise ValueError(f"Unmatched line '{line}' in annotation result")

        # Extract the time
        start_hour = float(match.group(1))
        start_min = float(match.group(2))
        start_sec = float(match.group(3))
        end_hour = float(match.group(4))
        end_min = float(match.group(5))
        end_sec = float(match.group(6))
        speaker = match.group(7)

        # To time in seconds
        start = start_hour * 3600 + start_min * 60 + start_sec
        end = end_hour * 3600 + end_min * 60 + end_sec

        results["tiers"].append(tier_name)
        results["start"].append(start)
        results["end"].append(end)
        results["annotation"].append(speaker)

    return pd.DataFrame(results)
