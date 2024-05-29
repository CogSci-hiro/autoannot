import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from autoannot import ROOT_DIR
from autoannot.transcription.align_transcription import align_transcription

TEST_WAV_FILE = ROOT_DIR / "data" / "test" / "wav_dir" / "AB-buzz.wav"
TEST_PARAMETERS_FILE = ROOT_DIR / "data" / "parameters.json"
TEST_ANNOTATION_FILE = ROOT_DIR / "data" / "test" / "dst_dir" / "diarizations" / "AB-buzz.csv"
TEST_TRANSCRIPTION_FILE = ROOT_DIR / "data" / "test" / "dst_dir" / "transcriptions" / "AB-buzz.csv"


class AlignTranscription(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_name = Path(self.temp_dir.name)

        with open(TEST_PARAMETERS_FILE, "r") as f:
            self.params = json.load(f)

    def test_align_transcription(self):

        out_file = self.temp_dir_name / "aligned_transcription.csv"
        align_transcription(TEST_ANNOTATION_FILE, TEST_TRANSCRIPTION_FILE, out_file, mode="partial")

        df = pd.read_csv(out_file)
        print(df)
        self.temp_dir.cleanup()
