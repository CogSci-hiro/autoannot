import os
from pathlib import Path
import traceback
from typing import Dict

import pandas as pd
from joblib import Parallel, delayed

from autoannot import diarize, transcribe, align, get_wav_paths, get_path_list


def annotate(params: Dict):

    # Parameters
    n_jobs = params["n_jobs"]
    use_existing = params["use_existing"]
    target = params["target"]

    # Paths
    src_dir = Path(params["paths"]["src_dir"])
    dst_dir = Path(params["paths"]["dst_dir"])

    # Get WAV paths
    wav_list = get_wav_paths(src_dir)

    # Save all errors
    errors = {"file": [], "error": []}

    # Diarize
    if _make_diarization(dst_dir, wav_list, use_existing):
        dia_dir = _make_dirs(dst_dir, "diarizations")
        log_dir = _make_dirs(dst_dir, "error_logs")

        dia_list = get_path_list(dia_dir, wav_list, extension="csv", suffix="diarization")
        log_list = get_path_list(log_dir, wav_list, extension="log", suffix="error")

        # Parallel(n_jobs=n_jobs)(delayed(diarize)(w, o, l, params) for w, o, l in zip(wav_list, dia_list, log_list))
        for w, o, l in zip(wav_list, dia_list, log_list):

            try:
                diarize(w, o, l, params)

            except Exception:  # noqa
                errors["file"].append(os.path.basename(w))
                errors["error"].append(traceback.format_exc())

    # Transcribe
    if _make_transcription(dst_dir, wav_list, use_existing, target):

        trs_dir = _make_dirs(dst_dir, "transcriptions")
        trs_list = get_path_list(trs_dir, wav_list, extension="csv", suffix="transcription")
        dia_dir = _make_dirs(dst_dir, "diarizations")
        dia_list = get_path_list(dia_dir, wav_list, extension="csv", suffix="diarization")

        # Parallel(n_jobs=n_jobs)(delayed(transcribe)(w, t, d, params) for w, t, d in zip(wav_list, trs_list, dia_list))
        for w, t, d in zip(wav_list, trs_list, dia_list):

            try:
                transcribe(w, t, d, params)

            except Exception:  # noqa
                errors["file"].append(os.path.basename(w))
                errors["error"].append(traceback.format_exc())

    # Align
    if _make_alignment(dst_dir, wav_list, use_existing, target):

        align_dir = _make_dirs(dst_dir, "transcriptions")
        align_list = get_path_list(align_dir, wav_list, extension="csv", suffix="aligned")
        palign_dir = _make_dirs(dst_dir, "palign_transcriptions")
        palign_list = get_path_list(palign_dir, wav_list, extension="TextGrid", suffix="palign")

        # Parallel(n_jobs=n_jobs)(delayed(align)(w, p, a, params) for w, p, a in zip(wav_list, palign_list, align_list))
        for w, p, a in zip(wav_list, palign_list, align_list):

            try:
                align(w, p, a, params)

            except Exception:  # noqa
                errors["file"].append(os.path.basename(w))
                errors["error"].append(traceback.format_exc())

    error_df = pd.DataFrame(errors)
    error_df.to_csv(dst_dir / "errors.csv", index=False)


def _make_dirs(dst_dir: Path, name: str):

    sub_dir = dst_dir / name
    if not sub_dir.exists():
        os.makedirs(sub_dir)

    return sub_dir


def _make_diarization(dst_dir, wav_list, use_existing):

    if use_existing:
        dia_dir = _make_dirs(dst_dir, "diarizations")
        dia_list = get_path_list(dia_dir, wav_list, extension="csv", suffix="diarization")

        for dia_path in dia_list:

            if not dia_path.exists():
                return True
        return False

    else:
        return True


def _make_transcription(dst_dir, wav_list, use_existing, target):

    if target not in ["transcription", "alignment"]:
        return False

    if use_existing:
        trs_dir = _make_dirs(dst_dir, "transcriptions")
        trs_list = get_path_list(trs_dir, wav_list, extension="csv", suffix="transcription")

        for trs_path in trs_list:

            if not trs_path.exists():
                return True
        return False

    else:
        return True


def _make_alignment(dst_dir, wav_list, use_existing, target):

    if target != "alignment":
        return False

    if use_existing:

        palign_dir = _make_dirs(dst_dir, "palign_transcriptions")
        palign_list = get_path_list(palign_dir, wav_list, extension="TextGrid", suffix="palign")

        for palign_list in palign_list:

            if not palign_list.exists():
                return True
        return False

    else:
        return True


if __name__ == "__main__":

    import json
    import yaml

    from autoannot import ROOT_DIR

    with open(ROOT_DIR / "config.yaml") as stream:
        config = yaml.safe_load(stream)

    params_path = config["parameter_file"]

    with open(params_path, "r") as f:
        params = json.load(f)

    annotate(params)
