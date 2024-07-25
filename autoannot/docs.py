import re
from typing import Callable

DOC_DICT = {}


# A
# DOC_DICT["auth_token"] = "auth_token : str\n\t\tAuthentication token for HuggingFace"
DOC_DICT["audio_file"] = "audio_file : str | Path\n\t\tPath to audio file"

# B

# C
# DOC_DICT["candidates"] = "candidates : str \n\t\t Main speaker candidates"
DOC_DICT["condition_on_previous_text"] = "condition_on_previous_text : \n\t\t"

# D
DOC_DICT["data_list"] = "data_list : List[np.ndarray]\n\t\tList of audio data"
DOC_DICT["dia_df"] = "dia_df : str | Path\n\t\t"
DOC_DICT["diarization"] = "diarization : \n\t\t"
DOC_DICT["diarization_file"] = "diarization_file : str | Path\n\t\tPath to diarization file"
DOC_DICT["dia_file"] = "dia_file : str | Path\n\t\tPath to diarization file"
DOC_DICT["dir_name"] = "dir_name : \n\t\t"
DOC_DICT["df"] = "df : pd.DataFrame\n\t\tTextGrid compatible DataFrame"
DOC_DICT["dst_dir"] = "dst_dir : \n\t\t"
# DOC_DICT["duration_threshold_upper"] = "duration_threshold_upper : float\n\t\tUpper threshold for duration"
# DOC_DICT["duration_threshold_lower"] = "duration_threshold_lower : float\n\t\tLower threshold for duration"

# E
DOC_DICT["empty"] = "empty : str\n\t\tString to replace empty string with, default is ``\"noise\"``"
DOC_DICT["end"] = "end : \n\t\t"
DOC_DICT["error_log"] = "error_log : str | Path\n\t\tPath to SPPAS error log file"
DOC_DICT["extension"] = "extension : str\n\t\t"

# F
DOC_DICT["fill_symbol"] = "fill_symbol : str\n\t\t"

# G

# H

# I
DOC_DICT["index"] = "index : int\n\t\t"
DOC_DICT["intensity"] = "intensity : \n\t\t"
# DOC_DICT["intensity_threshold_upper"] = "intensity_threshold_upper : float\n\t\tUpper threshold for intensity"
# DOC_DICT["intensity_threshold_lower"] = "intensity_threshold_lower : float\n\t\tLower threshold for intensity"
DOC_DICT["in_file"] = "in_file : str | Path\n\t\tPath to input file"
DOC_DICT["ipu_df"] = "ipu_df : pd.DataFrame\n\t\tDataFrame containing IPU annotations"
# J

# K
DOC_DICT["kwargs"] = "kwargs : Dict\n\t\tOther parameters"

# L
DOC_DICT["log_file"] = "log_file : None | str | Path\n\t\tPath to the log file"
# DOC_DICT["loud_and_short"] = "loud_and_short : bool\n\t\tLoud and short"

# M
# DOC_DICT["main_speaker"] = "main_speaker : \n\t\tMain speaker"
# DOC_DICT["manual_thresholds"] = ("manual_thresholds : None | str | Path\n\t\tPath to file containing manual threshold"
#                                 "if None, it is ignored")
# DOC_DICT["max_speakers"] = ("max_speakers : None | int\n\t\tMaximum number of speakers in the file, if is unknown"
#                            " ``None`` is specified")
DOC_DICT["min_duration"] = "min_duration : float\n\t\tMinimum duration of the interval, default is ```0.0``"
# DOC_DICT["min_sil"] = "min_sil : None | float\n\t\tMinimum silence duration"
# DOC_DICT["min_ipu"] = "min_ipu : None | float\n\t\tMinimum IPU duration"
DOC_DICT["min_mean_duration"] = "min_mean_duration : None | float\n\t\tMinimum mean duration"
# DOC_DICT["min_n_ipus"] = "min_n_ipus : None | min_n_ipus\n\t\tMinimum number of IPUs"
DOC_DICT["model"] = "model : str\n\t\tName of the model to use"

# N

# O
DOC_DICT["out_file"] = "out_file : str | Path\n\t\tPath to output file"

# P
DOC_DICT["path_list"] = "path_list : \n\t\t"
DOC_DICT["params"] = "params : Dict\n\t\tParameter dictionary"
DOC_DICT["partial_overlap"] = "partial_overlap : \n\t\t"
DOC_DICT["prefix"] = "prefix : None | str\n\t\t"
DOC_DICT["pyannote_file"] = "pyannote_file : str | Path\n\t\tPath to Pyannote diarization file"

# Q

# R
# DOC_DICT["rms"] = "rms : None | float\n\t\tRMS"

# S
DOC_DICT["sample_rate"] = "sample_rate : \n\t\t"
# DOC_DICT["shift_start"] = "shift_start : None | float\n\t\tShift start"
# DOC_DICT["shift_end"] = "shift_end : None | float\n\t\tShift end"
DOC_DICT["sppas_file"] = "sppas_file : str | Path\n\t\tPath to SPPAS diarization file"
DOC_DICT["start"] = "start : \n\t\t"
DOC_DICT["suffix"] = "suffix : None | str\n\t\t"

# T
DOC_DICT["target"] = "target : None | str\n\t\t"
DOC_DICT["trs_file"] = "trs_file : str | Path\n\t\tPath to transcription file"
DOC_DICT["temp_file"] = "temp_file : \n\t\t"
DOC_DICT["text"] = "text : str\n\t\tText to be cleaned"
DOC_DICT["tier_name"] = "tier_name : str\n\t\tName of the tier for annotation file"
DOC_DICT["timestamp"] = "timestamp : float\n\t\t"
DOC_DICT["transcription"] = "transcription : \n\t\t"

# U
DOC_DICT["use_cuda"] = "use_cuda : bool\n\t\tif ``True``, use GPU (if available)"

# V

# W
DOC_DICT["wav_data"] = "wav_data : \n\t\t"
DOC_DICT["wav_file"] = "wav_file : str | Path\n\t\tPath to WAV file"
DOC_DICT["wav_list"] = "wav_list : List[Path]\n\t\t"

# X

# Y

# Z


def fill_doc(func: Callable) -> Callable:
    """
    Replace various repeated docstrings in the format of ``\"%(...)s\"`` with appropriate text

    Parameters
    ----------
    func : Callable
        method whose docstring is to be replaced

    Returns
    -------
    func : Callable
        method whose docstring is to be replaced
    """

    docs = func.__doc__

    line_list = []
    for line in docs.splitlines():

        match = re.match(r"\s+%\((.*)\)s", line)
        if match is None:
            line_list.append(line)
            continue

        key = match.group(1)
        value = DOC_DICT[key]

        line = re.sub(f"%\\({key}\\)s", value, line)
        line_list.append(line)

    func.__doc__ = "\n".join(line_list)
    return func
