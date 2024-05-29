import csv
from pathlib import Path
import re
from typing import Tuple

import librosa
import numpy as np
import torch
import pandas as pd
from pyannote.audio import Pipeline

from . import PYANNOT_MODEL
from autoannot.utils.annotations import fill_missing


def diarize_pyannote(in_file: str | Path, out_file: str | Path,  max_speakers: None | int,
                     auth_token: str, use_cuda: bool = True) -> None:

    # Load pretrained model
    pipeline = Pipeline.from_pretrained(checkpoint_path=PYANNOT_MODEL, use_auth_token=auth_token)

    # Use CUDA
    if torch.cuda.is_available() and use_cuda:
        pipeline.to(torch.device("cuda"))

    # Set maximum number of speakers
    max_speakers = 10 if max_speakers is None else max_speakers

    # Annotate
    diarization = pipeline(in_file, max_speakers=max_speakers)

    # Convert to familiar dataframe
    dia_df = _convert_to_df(str(diarization))
    dia_df.to_csv(out_file, index=False, quoting=csv.QUOTE_NONNUMERIC)


def get_main_speaker(diarization_file: str | Path, wav_file: str | Path,
                     intensity_threshold_upper: float = 0.8, intensity_threshold_lower: float = 0.5,
                     duration_threshold_upper: float = 0.3,
                     duration_threshold_lower: float = 0.2) -> Tuple[str, str, bool]:

    # Columns are `speaker`, `intensity` (average) `duration` (total)
    result_df = _get_df(diarization_file, wav_file)

    # Normalization
    result_df["duration"] = result_df["duration"] / result_df["duration"].max()
    result_df["intensity"] = result_df["intensity"] / result_df["intensity"].max()

    # Check if there is a loud and short speaker (potentially main speaker assigned a different speaker ID)
    loud_and_short = result_df[(result_df["intensity"] > intensity_threshold_upper) &
                               (result_df["duration"] < duration_threshold_upper)]
    loud_and_short = len(loud_and_short.index) > 0

    # Remove speakers with extremely short speaking time (disturbs normalization calculation
    result_df = result_df[result_df["duration"] > duration_threshold_lower]

    # Filter speakers
    selected = result_df[result_df["intensity"] > intensity_threshold_lower]

    candidates = "NA"
    if len(selected) == 1:  # single match
        main_speaker = selected.iloc[0]["speaker"]

    elif len(selected) > 1:  # multiple match
        main_speaker = selected.sort_values(by=["intensity"], ascending=False).iloc[0]["speaker"]  # loudest
        candidates = ";".join(selected["speaker"])
    else:
        main_speaker = "NA"

    return main_speaker, candidates, loud_and_short

########################################################################################################################
# Private methods                                                                                                      #
########################################################################################################################


def _convert_to_df(diarization: str, tier_name: str = "pyannote"):

    results = {"tier": [], "start": [], "end": [], "annotation": []}

    for line in diarization.splitlines():

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

        results["tier"].append(tier_name)
        results["start"].append(start)
        results["end"].append(end)
        results["annotation"].append(speaker)

    results = pd.DataFrame(results)
    results = fill_missing(results, target=None)  # fill missing silence with #

    return results


def _get_df(diarization_file: str | Path, wav_file: str | Path) -> pd.DataFrame:

    # Load data
    diarization_df = pd.read_csv(diarization_file)
    wav_data, sample_rate = librosa.load(wav_file)

    # List of all unique speakers
    speakers = list(set(diarization_df["annotation"]))

    speaker_list, intensity_list, duration_list = [], [], []

    # Work speaker by speaker
    for speaker in speakers:

        # Select speaker
        speaker_df = diarization_df[diarization_df["annotation"] == speaker]

        # Intensity and duration per speaker
        speaker_intensity_list, speaker_duration_list = [], []
        for idx, row in speaker_df.iterrows():

            intensity = _get_intensity(row["start"], row["end"], wav_data, sample_rate)
            speaker_intensity_list.append(intensity)
            speaker_duration_list.append(row["end"] - row["start"])

        # Average intensity
        intensity = np.array(speaker_intensity_list).mean() if len(speaker_intensity_list) != 0 else 0

        # Total duration
        duration = np.array(speaker_duration_list).sum()

        # Save
        speaker_list.append(speaker)
        intensity_list.append(intensity)
        duration_list.append(duration)

    result_df = pd.DataFrame({"speaker": speaker_list, "intensity": intensity_list, "duration": duration_list})

    return result_df


def _get_intensity(start: float, end: float, wav_data: np.array, sample_rate: int) -> float:

    start_idx = int(start * sample_rate)
    end_idx = int(end * sample_rate)

    return np.abs(wav_data[start_idx: end_idx]).mean()
