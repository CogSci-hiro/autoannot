import logging
import os
from pathlib import Path

from autoannot import ROOT_DIR


def get_log_dir() -> Path:
    """
    Get path to the directory where logs are saved

    :returns: path to the logging directory
    :rtype: Path
    """

    path = Path(ROOT_DIR).parent / "data" / "logs"  # /summ_re/logger.py
    log_dir = Path(path)

    return log_dir


def setup_logging(name: str) -> logging.Logger:
    """
    Get the logger

    :param name: name of the log file
    :type name: str
    :returns: logger
    :rtype: logging.Logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_dir = get_log_dir()

    if not log_dir.exists():
        os.makedirs(log_dir)

    # Setup handlers
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_dir / f"{name}.log")
    stream_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    # Setup formatters
    fmt = "%(levelname)s :: %(asctime)s :: Process ID %(process)s :: %(module)s :: " + \
          "%(funcName)s() :: Line %(lineno)d :: %(message)s"
    formatter = logging.Formatter(fmt)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(logging.Formatter(""))

    # Add handlers
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
