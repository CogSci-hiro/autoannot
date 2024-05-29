from pathlib import Path
from typing import Dict

from .julius import palign


def align(in_file: str | Path, out_file: str | Path, trf_file: str | Path, params: Dict) -> None:

    if params["align"]["backend"] == "julius":
        palign(in_file, out_file, trf_file)
    else:
        raise NotImplementedError(f"Backend '{params['align']['backend']}' is not supported")