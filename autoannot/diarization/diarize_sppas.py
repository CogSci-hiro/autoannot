import os
from pathlib import Path


import pandas as pd

import autoannot  # noqa
from sppas.src.annotations import sppasSearchIPUs  # noqa

from . import MIN_SIL, MIN_IPU, SHIFT_START, SHIFT_END, MIN_MEAN_DURATION, MIN_N_IPUS


def diarize_sppas(in_file: str | Path, out_file: str | Path, error_log: str | Path,
                  min_sil: None | float = None, min_ipu: None | float = None,
                  shift_start: None | float = None, shift_end: None | float = None,
                  min_n_ipus: None | int = None, min_mean_duration: None | int = None,
                  rms: None | int = None, manual_thresholds: None | str | Path = None) -> None:

    # Make the SPPAS annotator object
    annotator = sppasSearchIPUs(log=None)

    # Set default parameters
    if min_sil is None:
        min_sil = MIN_SIL

    if min_ipu is None:
        min_ipu = MIN_IPU

    if shift_start is None:
        shift_start = SHIFT_START

    if shift_end is None:
        shift_end = SHIFT_END

    if min_n_ipus is None:
        min_n_ipus = MIN_N_IPUS

    if min_mean_duration is None:
        min_mean_duration = MIN_MEAN_DURATION

    # Set parameters
    annotator.set_min_sil(min_sil)
    annotator.set_min_ipu(min_ipu)
    annotator.set_shift_start(shift_start)
    annotator.set_shift_end(shift_end)

    # Set manual threshold if available
    basename = os.path.basename(in_file)

    if manual_thresholds is not None:

        manual_df = pd.read_csv(manual_thresholds)

        if basename in list(manual_df["file"]):
            annotator.set_threshold(manual_df[manual_df["file"] == basename].iloc[0]["threshold"])

    if rms is not None:
        annotator.set_threshold(rms)

    # Annotate #########################################################################################################

    in_file, out_file = str(in_file), str(out_file)

    try:
        annotator.run([in_file], output=out_file)

    except OSError as e:  # No IPUs to write
        pass

    # Check if reasonable number of IPUs have been found ###############################################################

    df = pd.read_csv(out_file, header=None, names=["tier", "start", "end", "annotation"])
    n_ipus = len(df.index)
    mean_duration = df["end"].sub(df["start"], axis=0).mean()

    quality_ok = n_ipus > min_n_ipus and mean_duration < min_mean_duration

    # Write the error log ##############################################################################################

    # Make sure the path exists
    error_log = Path(error_log)
    if not error_log.parent.exists():
        os.makedirs(error_log.parent)

        # Write the header
        with open(error_log, "w") as f:
            f.write(f"name,n_ipus,ok\n")

    # Write the result
    with open(error_log, "a") as f:
        fname = os.path.basename(in_file)
        f.write(f"{fname},{n_ipus},{quality_ok}\n")
