import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from autoannot import ROOT_DIR
from autoannot.diarization.diarize_pyannote import diarize_pyannote

TEST_WAV_FILE = ROOT_DIR / "data" / "test" / "wav_dir" / "AB-buzz.wav"
TEST_PARAMETERS_FILE = ROOT_DIR / "data" / "parameters.json"


class DiarizePyannote(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_name = Path(self.temp_dir.name)

        with open(TEST_PARAMETERS_FILE, "r") as f:
            self.params = json.load(f)["diarization"]["pyannot"]

    def test_pyannote_diarization(self):

        test_out_file = self.temp_dir_name / "test_diarization.csv"

        diarize_pyannote(in_file=TEST_WAV_FILE, out_file=test_out_file, n_speakers=self.params["speakers"],
                         auth_token=self.params["auth_token"], use_cuda=self.params["use_cuda"])

        # Check the output file exists
        df = pd.read_csv(test_out_file, header=None, names=["tier", "start", "end", "annotation"])

        self.temp_dir.cleanup()