import logging
from pathlib import Path
import sys

import yaml

from .alignment.align import align
from .constants import ROOT_DIR
from .diarization.diarize import diarize
from .transcription.transcribe import transcribe
from .transcription.clean_transcription import clean_transcription
from .transcription.align_transcription import align_transcription
from .utils.files import get_path_list, get_wav_paths

__version__ = "0.0.0"

# Configuration
with open(ROOT_DIR / "config.yaml") as stream:
    config = yaml.safe_load(stream)

if not config["logging"]["sppas"]:
    logging.getLogger().disabled = True  # SPPAS logs to root by default

# Add SPPAS path
sys.path.append(str(ROOT_DIR / "libs" / "SPPAS"))

__all__ = ["align", "diarize", "transcribe", "clean_transcription", "align_transcription",
           "get_path_list", "get_wav_paths", "ROOT_DIR"]
