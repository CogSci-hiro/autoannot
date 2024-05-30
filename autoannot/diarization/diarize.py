import csv
from pathlib import Path
import tempfile
from typing import Dict

import pandas as pd

from autoannot.diarization.diarize_sppas import diarize_sppas
from autoannot.diarization.diarize_pyannote import diarize_pyannote
from autoannot.utils.annotations import fill_missing


def diarize(in_file: str | Path, out_file: str | Path, log_file: None | str | Path, params: Dict) -> None:

    backend = params["diarization"]["backend"]

    if backend == "sppas":
        diarize_sppas(in_file, out_file, log_file, **params["diarization"]["sppas"])

    elif backend == "pyannot":
        diarize_pyannote(in_file, out_file, **params["diarization"]["pyannote"])

    elif backend == "combined":
        _diarize_combined(in_file, out_file, log_file, **params["diarization"])

    else:
        raise NotImplementedError(f"Backend '{backend}' is not implemented")


########################################################################################################################
# Private methods                                                                                                      #
########################################################################################################################


def _diarize_combined(in_file: str | Path, out_file: str | Path, log_file: str | Path, **kwargs) -> None:

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)
        diarize_sppas(in_file, temp_dir / "sppas.csv", log_file, **kwargs["sppas"])
        diarize_pyannote(in_file, temp_dir / "pyannote.csv", **kwargs["pyannote"])
        _combine(temp_dir / "sppas.csv", temp_dir / "pyannote.csv", out_file, **kwargs["combined"])


def _combine(sppas_file: str | Path, pyannote_file: str | Path, out_file: str | Path, tier_name: str = "combined",
             min_duration: float = 0.0) -> None:

    sppas_df = pd.read_csv(sppas_file, header=None, names=["tier", "start", "end", "annotation"])
    pyannote_df = pd.read_csv(pyannote_file)

    # If main_speaker is not found use dataframe is empty -> use SPPAS alone
    if len(pyannote_df.index) == 0:

        sppas_df["annotation"] = sppas_df["annotation"].apply(lambda x: x if x == "#" else "ipu")
        sppas_df.to_csv(out_file, index=False, header=False, quoting=csv.QUOTE_NONNUMERIC)
        return

    # Move the `cursor` to next closest boundary one by one and compare current annotations
    cursor = 0.0
    last = min(sppas_df.iloc[-1]["end"], pyannote_df.iloc[-1]["end"])  # last timestamp
    tier_list, start_list, end_list, annotation_list = [], [], [], []

    while cursor < last:

        # Possible intervals in which `cursor` can be in
        sppas_match = sppas_df[(sppas_df["start"] <= cursor) & (cursor < sppas_df["end"])]
        pyannot_match = pyannote_df[(pyannote_df["start"] <= cursor) & (cursor < pyannote_df["end"])]

        if len(sppas_match.index) > 0:

            sppas_annotation = sppas_match.iloc[0]["annotation"]
            sppas_start = sppas_match.iloc[0]["start"]
            sppas_end = sppas_match.iloc[0]["end"]

        else:
            raise ValueError(f"Cursor {cursor} not in any interval in SPPAS")

        if len(pyannot_match.index) > 0:

            pyannot_annotation = pyannot_match.iloc[0]["annotation"]
            pyannot_start = pyannot_match.iloc[0]["start"]
            pyannot_end = pyannot_match.iloc[0]["end"]

        else:
            raise ValueError(f"Cursor {cursor} not in any interval in Pyannote")

        # Only accept IPUs if both annotations agree
        current_annotation = "#" if sppas_annotation == "#" or pyannot_annotation == "#" else "ipu"

        # Select timestamps after cursor and remove duplicates
        timestamps = [sppas_start, sppas_end, pyannot_start, pyannot_end, cursor]
        timestamps = [item for item in timestamps if item >= cursor]
        timestamps = list(set(timestamps))
        timestamps.sort()

        start = timestamps[0]
        end = timestamps[1]  # noqa

        tier_list.append(tier_name)
        start_list.append(start)
        end_list.append(end)
        annotation_list.append(current_annotation)

        cursor = end

    df = pd.DataFrame({"tier": tier_list, "start": start_list, "end": end_list, "annotation": annotation_list})
    df = df[df["start"] + min_duration < df["end"]]
    df = fill_missing(df, target=None)
    df = _merge_rows(df)

    # Save
    df.to_csv(out_file, index=False)


def _merge_rows(df: pd.DataFrame) -> pd.DataFrame:

    if not len(df):
        return df

    tier_name = df.iloc[0]["tier"]
    current_annotation = None
    last_start = 0.0

    result = {"tier": [], "start": [], "end": [], "annotation": []}

    for _, row in df.iterrows():

        if current_annotation is None:
            current_annotation = row["annotation"]
            last_start = row["start"]
            continue

        if current_annotation == row["annotation"]:
            continue

        result["tier"].append(tier_name)
        result["start"].append(last_start)
        result["end"].append(row["start"])
        result["annotation"].append(current_annotation)

        current_annotation = row["annotation"]
        last_start = row["start"]

    # The last one
    result["tier"].append(tier_name)
    result["start"].append(df.iloc[-1]["start"])
    result["end"].append(df.iloc[-1]["end"])
    result["annotation"].append(df.iloc[-1]["annotation"])

    return pd.DataFrame(result)


if __name__ == "__main__":
    import json
    with open("/Users/hiro/PycharmProjects/autoannot/data/parameters.json", "r") as f:
        params = json.load(f)

    path = "/Users/hiro/PycharmProjects/autoannot/data/test/wav_dir/AB-buzz.wav"
    path2 = "/Users/hiro/PycharmProjects/autoannot/workspace/annot.csv"
    path3 = "/Users/hiro/PycharmProjects/autoannot/workspace/annot.log"
    diarize(path, path2, path3, params)
