import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from autoannot import ROOT_DIR
from autoannot.utils.annotations import fill_missing

TEST_WAV_FILE = ROOT_DIR / "data" / "test" / "wav_dir" / "AB-buzz.wav"
TEST_PARAMETERS_FILE = ROOT_DIR / "data" / "parameters.json"
TEST_ANNOTATION_FILE = ROOT_DIR / "data" / "test" / "dst_dir" / "diarizations" / "AB-buzz.csv"
TEST_TRANSCRIPTION_FILE = ROOT_DIR / "data" / "test" / "dst_dir" / "transcriptions" / "AB-buzz.csv"


class FillMissing(unittest.TestCase):

    def setUp(self):

        df = {"tier": ["test", "test", "test"],
              "start": [0.0, 1.0, 2.0],
              "end": [0.5, 1.5, 2.5],
              "annotation": ["test", "test", "test"]}

        self.df = pd.DataFrame(df)

    def test_align_transcription(self):

        df = fill_missing(self.df, target=None, fill_symbol="#")
        print(df)
