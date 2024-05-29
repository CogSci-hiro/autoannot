import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from autoannot import ROOT_DIR
from autoannot.diarization.diarize_sppas import diarize_sppas

TEST_WAV_FILE = ROOT_DIR / "data" / "test" / "wav_dir" / "AB-buzz.wav"
TEST_PARAMETERS_FILE = ROOT_DIR / "data" / "parameters.json"


class DiarizeSPPAS(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_name = Path(self.temp_dir.name)

        with open(TEST_PARAMETERS_FILE, "r") as f:
            self.params = json.load(f)["diarization"]["sppas"]

    def test_sppas_diarization(self):

        test_out_file = self.temp_dir_name / "test_diarization.csv"
        error_log_file = self.temp_dir_name / "error_log.log"

        diarize_sppas(in_file=TEST_WAV_FILE, out_file=test_out_file, error_log=error_log_file,
                      min_sil=self.params["min_sil"], min_ipu=self.params["min_ipu"],
                      shift_start=self.params["shift_start"], shift_end=self.params["shift_end"],
                      min_n_ipus=self.params["min_n_ipus"], min_mean_duration=self.params["min_mean_duration"],
                      rms=self.params["rms"], manual_thresholds=self.params["manual_thresholds"])

        # Check the output file exists
        df = pd.read_csv(test_out_file, header=None, names=["tier", "start", "end", "annotation"])

        self.temp_dir.cleanup()
