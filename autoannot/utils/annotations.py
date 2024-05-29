import pandas as pd


def fill_missing(df: pd.DataFrame, target: None | str,
                 fill_symbol: str = "#", min_duration: float = 0.01) -> pd.DataFrame:

    result = {"tiers": [], "start": [], "end": [], "annotation": []}
    last_end = 0.0

    for _, row in df.iterrows():

        # Skip if specific target is set
        if not row["annotation"] != target and target is not None:
            continue

        if row["start"] > last_end + min_duration:

            # Add silence
            result["tiers"].append(row["tiers"])
            result["start"].append(last_end)
            result["end"].append(row["start"])
            result["annotation"].append(fill_symbol)

        # Add annotation
        result["tiers"].append(row["tiers"])
        result["start"].append(row["start"])
        result["end"].append(row["end"])
        result["annotation"].append(row["annotation"])

        # Update
        last_end = row["end"]

    if len(df[df["end"] < df["start"]]) > 0:
        raise ValueError("")

    return pd.DataFrame(result)