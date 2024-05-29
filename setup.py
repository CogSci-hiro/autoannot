import os
from pathlib import Path
from setuptools import setup
import shutil
import subprocess
import zipfile

LIB_DIR = Path(os.getcwd()) / "libs"

# Set up SPPAS first ###################################################################################################
if not (LIB_DIR / "SPPAS").exists():

    # Add -k to avoid verification issues
    sppas = "curl -L -k https://sourceforge.net/projects/sppas/files/SPPAS-4.8-2022-12-14.zip > sppas.zip"
    subprocess.run(sppas, shell=True)

    if not LIB_DIR.exists():
        os.makedirs(LIB_DIR)

    with zipfile.ZipFile("sppas.zip", "r") as zip_ref:
        zip_ref.extractall(LIB_DIR / "SPPAS")

    os.remove("sppas.zip")

    # Setup SPPAS
    script_path = LIB_DIR.parent / "scripts" / "setup_sppas.py"
    new_script_path = LIB_DIR / "SPPAS" / "setup_sppas.py"
    shutil.copy(script_path, new_script_path)

    os.chdir(LIB_DIR / "SPPAS")
    subprocess.run("python setup_sppas.py install", shell=True)

# Make logs dir
log_dir = Path(os.getcwd()) / "data" / "logs"
if not log_dir.exists():
    os.makedirs(log_dir)

# Set up autoannot #####################################################################################################


setup(name="autoannot",
      version="0.0.0dev",
      description="Automatic annotation from audio file",
      author="Hiro Yamasaki",
      author_email="cog.sci.hiro.yamasaki@gmail.com",
      packages=["autoannot"],
      install_requires=[])
