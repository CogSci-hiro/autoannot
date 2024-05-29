from pathlib import Path

import pandas as pd

from autoannot.utils.annotations import fill_missing


def align_transcription(diarization_file: str | Path, transcription_file: str | Path, out_file: str | Path,
                        mode: str = "full", tier_name: str = "transcription"):

    dia_df = pd.read_csv(diarization_file)
    trs_df = pd.read_csv(transcription_file)

    results = {"tier": [], "start": [], "end": [], "annotation": []}
    for _, row in dia_df.iterrows():

        if row["annotation"] == "#":

            # Add the annotations
            results["tier"].append(tier_name)
            results["start"].append(row["start"])
            results["end"].append(row["end"])
            results["annotation"].append("#")
            continue

        # Select matching transcriptions and discard rest
        if mode == "full":

            # Only keep transcriptions fully inside IPUs
            selection = trs_df[(row["start"] <= trs_df["start"]) & (trs_df["end"] <= trs_df["end"])]

        elif mode == "partial":

            # Keep transcriptions partially overlapping
            selection = trs_df[(row["start"] <= trs_df["start"]) | (trs_df["end"] <= trs_df["end"])]

        else:
            raise NotImplementedError(f"The 'mode' '{mode}' is not implemented")

        # Matched text
        text = selection["annotation"].to_list()
        text = " ".join(text)

        # Add the annotations
        results["tier"].append(tier_name)
        results["start"].append(row["start"])
        results["end"].append(row["end"])
        results["annotation"].append(text)

    results = pd.DataFrame(results)
    results = fill_missing(results, target=None)
    results[results.isna()]["annotation"] = "#"
    results.to_csv(out_file, index=False)
