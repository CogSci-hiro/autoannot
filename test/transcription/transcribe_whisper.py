import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from autoannot import ROOT_DIR
from autoannot.transcription.transcribe_whisper import transcribe_whisper

TEST_WAV_FILE = ROOT_DIR / "data" / "test" / "wav_dir" / "AB-buzz.wav"
TEST_PARAMETERS_FILE = ROOT_DIR / "data" / "parameters.json"


class TranscribeWhisper(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_name = Path(self.temp_dir.name)

        with open(TEST_PARAMETERS_FILE, "r") as f:
            self.params = json.load(f)

    def test_transcribe_whisper(self):

        out_file = self.temp_dir_name / "transcription.csv"
        transcribe_whisper(TEST_WAV_FILE, out_file, model="tiny", use_cuda=True)

        df = pd.read_csv(out_file)

        self.temp_dir.cleanup()
