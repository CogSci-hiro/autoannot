import os
from pathlib import Path
from typing import Dict

from joblib import Parallel, delayed

from autoannot import diarize, transcribe, align, clean_transcription, align_transcription, get_wav_paths, get_path_list


def _make_dirs(dst_dir: Path, name: str):

    sub_dir = dst_dir / name
    if not sub_dir.exists():
        os.makedirs(sub_dir)

    return sub_dir


def annotate(params: Dict):

    # n_jobs
    n_jobs = params["n_jobs"]

    # Paths
    src_dir = Path(params["paths"]["src_dir"])
    dst_dir = Path(params["paths"]["dst_dir"])

    # Get WAV paths
    wav_list = get_wav_paths(src_dir)

    # Diarize
    dia_dir = _make_dirs(dst_dir, "diarizations")
    log_dir = _make_dirs(dst_dir, "error_logs")

    dia_list = get_path_list(dia_dir, wav_list, extension="csv", suffix="diarization")
    log_list = get_path_list(log_dir, wav_list, extension="log", suffix="error")
    Parallel(n_jobs=n_jobs)(delayed(diarize)(w, o, l, params) for w, o, l in zip(wav_list, dia_list, log_list))

    # Transcribe
    trs_dir = _make_dirs(dst_dir, "transcriptions")
    trs_list = get_path_list(trs_dir, wav_list, extension="csv", suffix="transcription")
    Parallel(n_jobs=n_jobs)(delayed(transcribe)(w, t, params) for w, t in zip(wav_list, trs_list))

    # Clean the transcription
    clean_dir = _make_dirs(dst_dir, "clean_transcriptions")
    clean_list = get_path_list(clean_dir, wav_list, extension="csv", suffix="clean")
    Parallel(n_jobs=n_jobs)(delayed(clean_transcription)(t, c) for t, c in zip(trs_list, clean_list))

    # Align with diarization file
    align_dir = _make_dirs(dst_dir, "aligned_transcriptions")
    align_list = get_path_list(align_dir, wav_list, extension="csv", suffix="aligned")
    Parallel(n_jobs=n_jobs)(delayed(align_transcription)(d, c, a, mode=params["transcription"]["mode"])
                            for d, c, a in zip(dia_list, clean_list, align_list))

    # Align
    palign_dir = _make_dirs(dst_dir, "palign_transcriptions")
    palign_list = get_path_list(palign_dir, wav_list, extension="TextGrid", suffix="palign")
    Parallel(n_jobs=n_jobs)(delayed(align)(w, p, a, params) for w, p, a in zip(wav_list, palign_list, align_list))


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
