import re

import pandas as pd

from autoannot.docs import fill_doc


@fill_doc
def clean_transcription(df: pd.DataFrame, empty: str = "noise") -> pd.DataFrame:

    results = {"tier": [], "start": [], "end": [], "annotation": []}
    for _, row in df.iterrows():

        text = row["annotation"]
        if isinstance(text, float):  # NaN
            text = ""
        elif isinstance(text, str):
            text = text
        else:
            raise TypeError(f"Invalid type '{type(text)}' for text")

        # Cleaning nonsense
        text = _remove_subtitles(text)
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

        # Handle empty segment
        if text == "" or text is None:
            if empty == "noise":  # treat the empty segment as unrecognized noise
                text = "*"
            else:
                raise NotImplementedError(f"'empty' == '{empty}' is not implemented")

        results["tier"].append(row["tier"])
        results["start"].append(row["start"])
        results["end"].append(row["end"])
        results["annotation"].append(text)

    df = pd.DataFrame(results)
    return df


########################################################################################################################
# Private methods                                                                                                      #
########################################################################################################################


@fill_doc
def _remove_subtitles(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """

    text = re.sub(r"^.*\.(com|org)", "", text)  # .com, .org, subtitle sites
    text = re.sub(r".*[Ss]ous-titrage.*", "", text)  # ... Sous-titrage ...
    text = re.sub(r".*❤️\spar\sSousTitreur\.com.*", "", text)  # ❤️ par SousTitreur.com

    return text


@fill_doc
def _normalize_spaces(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """

    text = re.sub(r"\s+", " ", text)

    return text


@fill_doc
def _remove_miscellaneous(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """

    text = re.sub(r"<\|\w*\|>", "", text)  # remove tags <|tag name|>

    return text


@fill_doc
def _normalize_currencies(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """
    return text


@fill_doc
def _normalize_roman(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """
    return text


@fill_doc
def _normalize_ligatures(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """

    text = re.sub(r"œ", "oe", text)
    text = re.sub(r"æ", "ae", text)
    text = re.sub(r"ﬁ", "fi", text)
    text = re.sub(r"ﬂ", "fl", text)
    text = re.sub("ĳ", "ij", text)

    return text


@fill_doc
def _normalize_ordinals(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """
    return text


@fill_doc
def _normalize_cardinals(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """
    return text


@fill_doc
def _normalize_symbols(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """
    return text


@fill_doc
def _normalize_dashes(text: str) -> str:
    """

    Parameters
    ----------
    %(text)s

    Returns
    -------
    %(text)s
    """
    return text
