from pathlib import Path
import re

import pandas as pd


def clean_transcription(in_file: str | Path, out_file: str | Path) -> None:

    df = pd.read_csv(in_file)

    results = {"tier": [], "start": [], "end": [], "annotation": []}
    for _, row in df.iterrows():

        # Cleaning nonsense
        text = _remove_subtitles(row["annotation"])
        text = _normalize_spaces(text)
        text = _remove_miscellaneous(text)

        # Normalization
        text = _normalize_currencies(text)
        text = _normalize_roman(text)
        text = _normalize_ligatures(text)
        text = _normalize_ordinals(text)
        text = _normalize_cardinals(text)
        text = _normalize_symbols(text)
        text = _normalize_dashes(text)

        results["tier"].append(row["tier"])
        results["start"].append(row["start"])
        results["end"].append(row["end"])
        results["annotation"].append(text)

    df = pd.DataFrame(results)
    df.to_csv(out_file)


########################################################################################################################
# Private methods                                                                                                      #
########################################################################################################################

def _remove_subtitles(text: str) -> str:

    text = re.sub(r"^.*\.(com|org)", "", text)  # .com, .org, subtitle sites
    text = re.sub(r".*[Ss]ous-titrage.*", "", text)  # ... Sous-titrage ...
    text = re.sub(r".*❤️\spar\sSousTitreur\.com.*", "", text)  # ❤️ par SousTitreur.com

    return text


def _normalize_spaces(text: str) -> str:

    text = re.sub(r"\s+", " ", text)

    return text


def _remove_miscellaneous(text: str) -> str:

    text = re.sub(r"<\|\w*\|>", "", text)  # remove tags <|tag name|>

    return text


def _normalize_currencies(text: str) -> str:
    return text


def _normalize_roman(text: str) -> str:
    return text


def _normalize_ligatures(text: str) -> str:

    text = re.sub(r"œ", "oe", text)
    text = re.sub(r"æ", "ae", text)
    text = re.sub(r"ﬁ", "fi", text)
    text = re.sub(r"ﬂ", "fl", text)
    text = re.sub("ĳ", "ij", text)

    return text


def _normalize_ordinals(text: str) -> str:
    return text


def _normalize_cardinals(text: str) -> str:
    return text


def _normalize_symbols(text: str) -> str:
    return text


def _normalize_dashes(text: str) -> str:
    return text
