from pathlib import Path
import tempfile
from typing import Tuple
import warnings

import numpy as np
from scipy.io import wavfile
import pandas as pd
import torch
import whisper
import whisper_timestamped

from autoannot.docs import fill_doc

# UserWarning: FP16 is not supported on CPU; using FP32 instead
warnings.filterwarnings(action="ignore", category=UserWarning)


@fill_doc
def transcribe_whisper(in_file: str | Path, dia_file: str | Path,
                       model: str, use_cuda: bool, condition_on_previous_text: bool = False) -> pd.DataFrame:
    """

    Parameters
    ----------
    %(in_file)s
    %(dia_file)s
    %(model)s
    %(use_cuda)s
    condition_on_previous_text

    Returns
    -------
    %(df)s
    """

    # Make cropped audio file
    temp_audio, ipu_df, dia_df = _make_cropped(in_file, dia_file)

    # Load model
    model = whisper.load_model(model)

    # Use CUDA
    if torch.cuda.is_available() and use_cuda:
        model.to(torch.device("cuda"))

    # Prompt
    prompt = "Bon. Ben je crois euh je vois ce que euh tu veux dire"

    # Transcribe
    results = whisper_timestamped.transcribe(model, initial_prompt=prompt,
                                             condition_on_previous_text=condition_on_previous_text,
                                             audio=temp_audio.name)  # noqa

    # Convert to standard format and save
    results = _convert_to_dataframe(results, ipu_df, dia_df)

    # Clean up
    temp_audio.close()

    return results


@fill_doc
def _make_cropped(audio_file: str | Path,
                  dia_file: str | Path) -> Tuple[tempfile.NamedTemporaryFile, pd.DataFrame, pd.DataFrame]:
    """

    Parameters
    ----------
    %(audio_file)s
    %(dia_file)s

    Returns
    -------
    %(temp_file)s
    %(ipu_df)s
    %(df)s
    """

    # Read files
    sr, data = wavfile.read(audio_file)
    if data.shape[0] == 2:  # stereo data
        data = data.mean(axis=0)

    df = pd.read_csv(dia_file)

    data_list = []
    ipu_df = {"start": [], "end": [], "index": []}
    current_start = 0.0
    for idx, row in df.iterrows():

        duration = row["end"] - row["start"]
        if row["annotation"] == "ipu":

            # Get a segment of the audio
            start, end = int(row["start"] * sr), int(row["end"] * sr)
            data_list.append(data[start:end])

            # Note the total offset and regions where this offset is valid
            ipu_df["start"].append(current_start)
            ipu_df["end"].append(current_start + duration)
            ipu_df["index"].append(idx)

            # Update current start point in the new audio
            current_start += duration

    # Concatenate data
    data = np.concatenate(data_list)

    ipu_df = pd.DataFrame(ipu_df)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    wavfile.write(temp_file, sr, data)

    return temp_file, ipu_df, df


@fill_doc
def _convert_to_dataframe(transcription, ipu_df: pd.DataFrame, dia_df: pd.DataFrame,
                          partial_overlap: str = "ignore") -> pd.DataFrame:
    """

    Parameters
    ----------
    %(transcription)s
    %(ipu_df)s
    %(dia_df)s
    %(partial_overlap)s

    Returns
    -------
    %(df)s
    """

    # Assign IPU index to each word
    annotation = {"annotation": [], "index": []}
    for segment in transcription["segments"]:

        for word in segment["words"]:

            start = _get_index(word["start"], ipu_df, start=True)
            end = _get_index(word["end"], ipu_df, start=False)

            # Start and end are not in the same interval
            if start != end:

                if partial_overlap == "ignore":
                    continue
                else:
                    raise NotImplementedError(f"'partial_overlap' == '{partial_overlap}' is not implemented")

            annotation["annotation"].append(word["text"])
            annotation["index"].append(start)

    annotation = pd.DataFrame(annotation)

    # Fall back on the diarization file
    df = {"tier": [], "start": [], "end": [], "annotation": []}
    for idx, row in dia_df.iterrows():

        if row["annotation"] == "ipu":

            # Extract text that corresponds to the IPU index
            text = annotation[annotation["index"] == idx]["annotation"]

            if len(text) == 0:
                text = ""

            elif len(text) > 1:
                text = text.to_list()
                text = " ".join(text)

            else:
                text = text.values[0]

        else:
            text = "#"

        df["tier"].append("transcription")
        df["start"].append(row["start"])
        df["end"].append(row["end"])
        df["annotation"].append(text)

    df = pd.DataFrame(df)
    return df


@fill_doc
def _get_index(timestamp: float, df: pd.DataFrame, start: bool) -> int:
    """

    Parameters
    ----------
    %(timestamp)s
    %(df)s
    %(start)s

    Returns
    -------
    %(index)s
    """

    # Beyond the last timestamp
    last_timestamp = df["end"].values[-1]
    if timestamp > last_timestamp:
        return df["index"].values[-1]

    df = df[(df["start"] <= timestamp) & (timestamp <= df["end"])]

    # Sanity check (these should not happen)
    if len(df) == 0:
        raise ValueError(f"timestamp '{timestamp}' was not found anywhere in the IPU dataframe")

    elif len(df) == 2:
        if start:
            return df["index"].values[1]
        else:
            return df["index"].values[0]

    elif len(df) > 2:
        raise ValueError(f"timestamp '{timestamp}' is in multiple IPUs")

    return df["index"].values[-1]
