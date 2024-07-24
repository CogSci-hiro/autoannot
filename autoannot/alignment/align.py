from pathlib import Path
from typing import Dict

from .julius import palign


def align(in_file: str | Path, out_file: str | Path, trf_file: str | Path, params: Dict) -> None:
    """
    Force-alignment to create phoneme level annotations

    Parameters
    ----------
    in_file : str | Path
        path to input file
    out_file : str | Path
        path to output file
    trf_file : str | Path
        path to transcription file
    params : dict
        parameter dictionary
    Returns
    -------
    None
    """

    if params["alignment"]["backend"] == "julius":
        palign(in_file, out_file, trf_file)
    else:
        raise NotImplementedError(f"Backend '{params['align']['backend']}' is not supported")