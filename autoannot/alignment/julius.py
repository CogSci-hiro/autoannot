import os
from pathlib import Path
import re
import sys
import tempfile

from autoannot.constants import ROOT_DIR
from autoannot.docs import fill_doc

# Add SPPAS path
sys.path.append(str(ROOT_DIR / "libs" / "SPPAS"))

from sppas.src.annotations import sppasTextNorm  # noqa
from sppas.src.annotations import sppasPhon      # noqa
from sppas.src.annotations import sppasAlign     # noqa

# Resource paths
RESOURCE_PATH = ROOT_DIR / "libs" / "SPPAS" / "resources"
VOCAB_PATH = RESOURCE_PATH / "vocab" / "fra.vocab"
DICT_PATH = RESOURCE_PATH / "dict" / "fra.dict"
MODEL_PATH = RESOURCE_PATH / "models" / "models-fra"
LANG = "fra"


@fill_doc
def palign(in_file: str | Path, out_file: str | Path, trs_file: str | Path) -> None:
    """
    Phoneme level alignment in Julius

    Parameters
    ----------
    %(in_file)s
    %(out_file)s
    %(trs_file)s

    Returns
    -------
    None
    """

    tmp = tempfile.TemporaryDirectory()
    tmp_dir = Path(tmp.name)

    fname = os.path.basename(trs_file)
    match = re.match(r"(.*)(\.csv|TextGrid)", fname)
    if match:
        file_stem = match.group(1)
    else:
        raise ValueError(f"File type must be '.csv' or '.TextGrid' but got {fname}")

    # Normalize the transcription ######################################################################################
    token_file = f"{file_stem}-token.TextGrid"
    _sppas_normalize(in_file=str(trs_file), out_file=str(tmp_dir / token_file))

    # Phonetize the transcription ######################################################################################
    phon_file = f"{file_stem}-phon.TextGrid"
    _sppas_phonetize(in_file=str(tmp_dir / token_file), out_file=str(tmp_dir / phon_file))

    # Align with WAV file ##############################################################################################
    annotator = sppasAlign(log=None)
    annotator.load_resources(str(MODEL_PATH))

    annotator.run([str(tmp_dir / phon_file), str(in_file), str(tmp_dir / token_file)], str(out_file))

    tmp.cleanup()

########################################################################################################################
# Private methods                                                                                                      #
########################################################################################################################


@fill_doc
def _sppas_normalize(in_file: str | Path, out_file: str | Path) -> None:
    """
    Text normalization with SPPAS

    Parameters
    ----------
    %(in_file)s
    %(out_file)s

    Returns
    -------
    None
    """

    text_norm = sppasTextNorm(log=None)
    text_norm.load_resources(str(VOCAB_PATH), lang=LANG)
    text_norm.run([in_file], output=out_file)


@fill_doc
def _sppas_phonetize(in_file: str | Path, out_file: str | Path) -> None:
    """
    Phonetization with SPPAS

    Parameters
    ----------
    %(in_file)s
    %(out_file)s

    Returns
    -------
    None
    """

    phon = sppasPhon(log=None)
    phon.load_resources(str(DICT_PATH))
    phon.run([in_file], output=out_file)
