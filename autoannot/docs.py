import re

DOC_DICT = {}


# A
DOC_DICT["auth_token"] = "auth_token : str\n\t\t"
DOC_DICT["audio_file"] = "audio_file : \n\t\t"

# B

# C
DOC_DICT["candidates"] = "candidates : \n\t\t"
DOC_DICT["condition_on_previous_text"] = "condition_on_previous_text : \n\t\t"

# D
DOC_DICT["data_list"] = "data_list : \n\t\t"
DOC_DICT["dia_df"] = "dia_df : str | Path\n\t\t"
DOC_DICT["diarization"] = "diarization : \n\t\t"
DOC_DICT["diarization_file"] = "diarization_file : str | Path\n\t\t"
DOC_DICT["dia_file"] = "dia_file : str | Path\n\t\t"
DOC_DICT["dir_name"] = "dir_name : \n\t\t"
DOC_DICT["df"] = "df : pd.DataFrame\n\t\t"
DOC_DICT["dst_dir"] = "dst_dir : \n\t\t"
DOC_DICT["duration_threshold_upper"] = "duration_threshold_upper : float\n\t\t"
DOC_DICT["duration_threshold_lower"] = "duration_threshold_lower : float\n\t\t"

# E
DOC_DICT["empty"] = "empty : str\n\t\t"
DOC_DICT["end"] = "end : \n\t\t"
DOC_DICT["error_log"] = "error_log : str | Path\n\t\t"
DOC_DICT["extension"] = "extension : str\n\t\t"

# F
DOC_DICT["fill_symbol"] = "fill_symbol : str\n\t\t"

# G

# H

# I
DOC_DICT["index"] = "index : int\n\t\t"
DOC_DICT["intensity"] = "intensity : \n\t\t"
DOC_DICT["intensity_threshold_upper"] = "intensity_threshold_upper : float\n\t\t"
DOC_DICT["intensity_threshold_lower"] = "intensity_threshold_lower : float\n\t\t"
DOC_DICT["in_file"] = "in_file : str | Path\n\t\t"
DOC_DICT["ipu_df"] = "ipu_df : \n\t\t"
# J

# K
DOC_DICT["kwargs"] = "kwargs : Dict\n\t\t"

# L
DOC_DICT["log_file"] = "log_file : \n\t\t"
DOC_DICT["loud_and_short"] = "loud_and_short : \n\t\t"

# M
DOC_DICT["main_speaker"] = "main_speaker : \n\t\t"
DOC_DICT["manual_thresholds"] = "manual_thresholds : None | str | Path\n\t\t"
DOC_DICT["max_speakers"] = "max_speakers : None | int\n\t\t"
DOC_DICT["min_duration"] = "min_duration : float\n\t\t"
DOC_DICT["min_sil"] = "min_sil : None | float\n\t\t"
DOC_DICT["min_ipu"] = "min_ipu : None | float\n\t\t"
DOC_DICT["min_mean_duration"] = "min_mean_duration : None | float\n\t\t"
DOC_DICT["min_n_ipus"] = "min_n_ipus : None | min_n_ipus\n\t\t"
DOC_DICT["model"] = "model : str\n\t\t"

# N

# O
DOC_DICT["out_file"] = "out_file : str | Path\n\t\t"

# P
DOC_DICT["path_list"] = "path_list : \n\t\t"
DOC_DICT["params"] = "params : Dict\n\t\t"
DOC_DICT["partial_overlap"] = "partial_overlap : \n\t\t"
DOC_DICT["prefix"] = "prefix : None | str\n\t\t"
DOC_DICT["pyannote_file"] = "pyannote_file : str | Path\n\t\t"

# Q

# R
DOC_DICT["rms"] = "rms : None | float\n\t\t"

# S
DOC_DICT["sample_rate"] = "sample_rate : \n\t\t"
DOC_DICT["shift_start"] = "shift_start : None | float\n\t\t"
DOC_DICT["shift_end"] = "shift_end : None | float\n\t\t"
DOC_DICT["sppas_file"] = "sppas_file : str | Path\n\t\t"
DOC_DICT["start"] = "start : \n\t\t"
DOC_DICT["suffix"] = "suffix : None | str\n\t\t"

# T
DOC_DICT["target"] = "target : None | str\n\t\t"
DOC_DICT["trs_file"] = "trs_file : str | Path\n\t\t"
DOC_DICT["temp_file"] = "temp_file : \n\t\t"
DOC_DICT["text"] = "text : str\n\t\t"
DOC_DICT["tier_name"] = "tier_name : str\n\t\t"
DOC_DICT["timestamp"] = "timestamp : float\n\t\t"
DOC_DICT["transcription"] = "transcription : \n\t\t"

# U
DOC_DICT["use_cuda"] = "use_cuda : bool\n\t\t"

# V

# W
DOC_DICT["wav_data"] = "wav_data : \n\t\t"
DOC_DICT["wav_file"] = "wav_file : str | Path\n\t\t"
DOC_DICT["wav_list"] = "wav_list : List[Path]\n\t\t"

# X

# Y

# Z


def fill_doc(func):

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
