import os
from pathlib import Path
from typing import Dict

import pandas as pd
from pyannote.audio import Pipeline

from ..diarization import PYANNOT_MODEL
from autoannot.docs import fill_doc


@fill_doc
def fill_missing(df: pd.DataFrame, target: None | str,
                 fill_symbol: str = "#", min_duration: float = 0.01) -> pd.DataFrame:

    result = {"tier": [], "start": [], "end": [], "annotation": []}
    last_end = 0.0

    for _, row in df.iterrows():

        # Skip if specific target is set
        if not row["annotation"] != target and target is not None:
            continue

        if row["start"] > last_end + min_duration:

            # Add silence
            result["tier"].append(row["tier"])
            result["start"].append(last_end)
            result["end"].append(row["start"])
            result["annotation"].append(fill_symbol)

        # Add annotation
        result["tier"].append(row["tier"])
        result["start"].append(row["start"])
        result["end"].append(row["end"])
        result["annotation"].append(row["annotation"])

        # Update
        last_end = row["end"]

    if len(df[df["end"] < df["start"]]) > 0:
        raise ValueError("end is before start")

    return pd.DataFrame(result)


@fill_doc
def check_parameters(params: Dict) -> None:
    """

    Parameters
    ----------
    %(params)s

    Returns
    -------
    None
    """

    _check_keys(params, ["target", "paths", "diarization", "transcription", "alignment", "advanced"])

    # Number of jobs
    n_jobs = params["n_jobs"]
    if not isinstance(n_jobs, int) or n_jobs is not None:
        raise TypeError(f"'n_jobs' must be either 'int' or 'None'")

    # Target file to make
    target = params["target"]
    if target not in ["diarization", "transcription", "alignment"]:
        raise NotImplementedError(f"'target' == '{target}' is not implemented")

    # Extensions
    _check_extension(params["extension"], target)

    # Use existing
    if not isinstance(params["use_existing"], bool):
        raise TypeError(f"'use_existing' must be 'bool'")

    # Sub-dictionary
    _check_paths(params["paths"])
    _check_diarization(params["diarization"])
    _check_transcription(params["transcription"])
    _check_alignment(params["alignment"])
    _check_advanced(params["advanced"])


########################################################################################################################


def _check_keys(params, keys):

    for key in keys:
        if key not in params.keys():
            raise KeyError(f"'{key}' is required in the parameter JSON")


def _check_extension(extension, target):

    if target == "diarization":
        if extension not in ["csv", "CSV", "textgrid", "TextGrid"]:
            raise ValueError(f"'extension' == '{extension}' is not valid for 'target' == '{target}'")

    elif target == "transcription":
        if extension not in ["csv", "CSV", "textgrid", "TextGrid"]:
            raise ValueError(f"'extension' == '{extension}' is not valid for 'target' == '{target}'")

    if target == "alignment":
        if extension not in ["textgrid", "TextGrid"]:
            raise ValueError(f"'extension' == '{extension}' is not valid for 'target' == '{target}'")


def _check_paths(paths):

    _check_keys(paths, ["src_dir", "dst_dir"])

    src_dir = paths["src_dir"]
    dst_dir = paths["dst_dir"]
    if src_dir == dst_dir:
        raise ValueError(f"'src_dir' == '{src_dir}' cannot be the same as 'dst_dir' == '{dst_dir}'")

    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    if not src_dir.exists():
        raise FileNotFoundError(f"'src_dir' == '{src_dir}' does not exist")

    if dst_dir.exists():
        os.makedirs(dst_dir)


def _check_diarization(diarization):

    _check_keys(diarization, ["backend"])

    backend = diarization["backend"]
    if backend in ["sppas", "combined"]:
        _check_keys(diarization, ["sppas"])
        _check_sppas(diarization["sppas"])

    elif backend in ["pyannote", "combined"]:
        _check_keys(diarization, ["pyannote"])
        _check_pyannote(diarization["pyannote"])

    elif backend == "combined":
        _check_keys(diarization, ["sppas", "pyannote"])
        _check_combined(diarization["combined"])

    else:
        raise NotImplementedError(f"'backend' == '{backend}' is not implemented")


def _check_sppas(sppas):

    _check_keys(sppas, ["min_sil", "min_ipu", "shift_start", "shift_end", "min_n_ipus", "min_mean_duration",
                        "rms", "manual_thresholds"])

    def _check_type(var, name):
        if not isinstance(var, float) or not isinstance(var, int) or var is not None:
            raise TypeError(f"'{name}' must be either 'float', 'int' or 'None'")

    _check_type(sppas["min_sil"], "min_sil")
    _check_type(sppas["min_ipu"], "min_ipu")
    _check_type(sppas["shift_start"], "shift_start")
    _check_type(sppas["shift_end"], "shift_end")
    _check_type(sppas["min_n_ipus"], "min_n_ipus")
    _check_type(sppas["min_mean_duration"], "min_mean_duration")
    _check_type(sppas["rms"], "rms")
    _check_type(sppas["manual_thresholds"], "manual_thresholds")


def _check_pyannote(pyannote):
    _check_keys(pyannote, ["auth_token", "use_cuda", "max_speakers"])

    auth_token = pyannote["auth_token"]
    if not isinstance(auth_token, str):
        raise TypeError(f"'auth_token' must be a 'str'")

    pipeline = Pipeline.from_pretrained(checkpoint_path=PYANNOT_MODEL, use_auth_token=auth_token)

    if pipeline is None:
        raise ValueError(f"Could not load the pyannote model. Probably the 'auth_token' is invalid")

    if not isinstance(pyannote["use_cuda"], bool):
        raise TypeError(f"'use_cuda' must be a 'bool'")

    if not isinstance(pyannote["max_speakers"], int) or pyannote["max_speakers"] is not None:
        raise TypeError(f"'max_speakers' must be an 'int' or 'None'")


def _check_combined(combined):

    _check_keys(combined, ["combined", "min_duration"])

    if not isinstance(combined["tier_name"], str):
        raise TypeError(f"'tier_name' must be 'str'")

    if not isinstance(combined["min_duration"], float):
        raise TypeError(f"'min_duration' must be a 'float'")


def _check_transcription(transcription):

    _check_keys(transcription, ["backend"])

    backend = transcription["backend"]

    if backend == "whisper":
        _check_keys(transcription["whisper"], ["model", "use_cuda"])
    elif backend == "wav2vec2":
        _check_keys(transcription["wav2vec2"], ["model", "use_cuda"])
    else:
        raise NotImplementedError(f"'backend' == '{backend}' is not implemented")


def _check_alignment(alignment):
    _check_keys(alignment, ["julius"])


def _check_advanced(advanced):
    _check_keys(advanced, ["sppas_log"])
