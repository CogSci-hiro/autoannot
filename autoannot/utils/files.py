import os
from pathlib import Path
import re
import sys
import tempfile
from typing import List

import pandas as pd

from autoannot.constants import ROOT_DIR

# Add SPPAS path
sys.path.append(str(ROOT_DIR / "libs" / "SPPAS"))

from sppas.src.anndata import sppasTrsRW  # noqa


def get_wav_paths(dir_name: str | Path) -> List[Path]:

    path_list = []
    dir_name = Path(dir_name)
    for file in os.listdir(dir_name):

        if file.startswith("."):
            continue

        if re.match(r".*(wav|WAV)", file):
            path_list.append(dir_name / file)

        elif re.match(r".*(mp3|MP3)", file):
            raise ValueError(f"MP3 is not supported, please convert to WAV first")

        else:
            fname, extension = os.path.splitext(file)
            raise ValueError(f"'{extension}' is not supported, please convert to WAV first")

    path_list.sort()

    return path_list


def get_path_list(dst_dir: Path, wav_list: List[Path], extension: str,
                  prefix: None | str = None, suffix: None | str = None):

    path_list = []
    for wav_path in wav_list:

        fname = os.path.basename(wav_path)
        stem, _ = os.path.splitext(fname)

        # Add nothing if None or add prefix/suffix + "_"
        prefix_ = "" if prefix is None else f"{prefix}_"
        suffix_ = "" if suffix is None else f"_{suffix}"

        path = dst_dir / f"{prefix_}{stem}{suffix_}.{extension}"
        path_list.append(path)

    return path_list


def convert_annotation(in_file: str | Path, out_file: str | Path) -> None:

    # SPPAS conversion
    parser = sppasTrsRW(str(in_file))
    trs = parser.read()
    parser.set_filename(str(out_file))
    parser.write(trs)


def to_textgrid(out_file: str | Path, df: pd.DataFrame) -> None:

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)
        df.to_csv(temp_dir / "annotation.csv", header=False)

        convert_annotation(temp_dir / "annotation.csv", out_file)
