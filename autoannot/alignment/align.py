from pathlib import Path
from typing import Dict

from .julius import palign
from autoannot.docs import fill_doc


@fill_doc
def align(in_file: str | Path, out_file: str | Path, trs_file: str | Path, params: Dict) -> None:
    """
    Force-alignment to create phoneme level annotations
    Perform forced alignment from transcription file and WAV file

    Currently only SPPAS + Julius forced alignment is supported
    (For more information, see https://sppas.org/workdemo.html#stepa5,
    https://www.sp.nitech.ac.jp/~ri/julius-dev/doxygen/julius/4.0/en/index.html)

    Parameters
    ----------
    %(in_file)s
    %(out_file)s
    %(trs_file)s
    %(params)s

    Returns
    -------
    None
    """

    if params["alignment"]["backend"] == "julius":
        palign(in_file, out_file, trs_file)
    else:
        raise NotImplementedError(f"Backend '{params['align']['backend']}' is not supported")