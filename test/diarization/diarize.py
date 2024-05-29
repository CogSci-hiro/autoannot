import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from autoannot import ROOT_DIR
from autoannot.diarization.diarize import diarize

TEST_WAV_FILE = ROOT_DIR / "data" / "test" / "wav_dir" / "AB-buzz.wav"
TEST_PARAMETERS_FILE = ROOT_DIR / "data" / "parameters.json"


class Diarize(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_name = Path(self.temp_dir.name)

        with open(TEST_PARAMETERS_FILE, "r") as f:
            self.params = json.load(f)

    def test_diarization(self):

        test_out_file = self.temp_dir_name / "test_diarization.csv"
        log_file = self.temp_dir_name / "test_log.log"

        diarize(in_file=TEST_WAV_FILE, out_file=test_out_file, log_file=log_file, params=self.params)

        # Check the output file exists
        df = pd.read_csv(test_out_file, header=None, names=["tier", "start", "end", "annotation"])

        self.temp_dir.cleanup()
