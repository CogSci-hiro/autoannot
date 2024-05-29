import logging
from pathlib import Path
import sys

import yaml

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# Configuration
with open(ROOT_DIR / "config.yaml") as stream:
    config = yaml.safe_load(stream)

if not config["logging"]["sppas"]:
    logging.getLogger().disabled = True  # SPPAS logs to root by default

# Add SPPAS path
sys.path.append(str(ROOT_DIR / "libs" / "SPPAS"))
