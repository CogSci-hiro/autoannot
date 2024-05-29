import unittest

from autoannot import ROOT_DIR
from autoannot.utils.files import get_wav_paths

TEST_WAV_DIR = ROOT_DIR / "data" / "test" / "wav_dir"


class GetWAVPaths(unittest.TestCase):

    def test_align_transcription(self):

        paths = get_wav_paths(TEST_WAV_DIR)

        print(paths)
        self.assertEqual(list, type(paths))
