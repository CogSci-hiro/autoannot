import os
from pathlib import Path
import re
from typing import List


def get_wav_paths(dir_name: str | Path) -> List[Path]:

    path_list = []
    dir_name = Path(dir_name)
    for file in os.listdir(dir_name):

        if re.match(r".*(wav|WAV)", file):
            path_list.append(dir_name / file)

        elif re.match(r".*(mp3|MP3)", file):
            raise ValueError(f"MP3 is not supported, please convert to WAV first")

        else:
            fname, extension = os.path.splitext(file)
            raise ValueError(f"'{extension}' is not supported, please convert to WAV first")

    path_list.sort()

    return path_list
