# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from intersphinx_registry import get_intersphinx_mapping
sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "autoannot"
copyright = "2024, Hiro Yamasaki"
author = "Hiro Yamasaki"

# The full version, including alpha/beta/rc tags
release = '0.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.viewcode",
              "sphinx.ext.intersphinx",
              "numpydoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    # More niche so didn't upstream to intersphinx_registry
    "python": ("https://docs.python.org/3", None),
    "mne": ("https://mne.tools/dev", None),
    "scipy": ("https://scipy.github.io/devdocs", None),
    "matplotlib": ("https://matplotlib.org", None),
    "pandas": ("https://pandas.pydata.org/", None)
}
intersphinx_mapping.update(
    get_intersphinx_mapping(
        packages=set(
            """
imageio matplotlib numpy pandas python scipy statsmodels sklearn numba joblib nibabel
seaborn patsy pyvista dipy nilearn pyqtgraph
""".strip().split()
        ),
    )
)


# NumPyDoc configuration -----------------------------------------------------
# Based on MNE-python config https://github.com/mne-tools/mne-python/blob/main/doc/conf.py
numpydoc_use_plots = True
numpydoc_class_members_toctree = True
numpydoc_attributes_as_param_list = True
numpydoc_xref_param_type = True
numpydoc_xref_aliases = {
    # Python

    "file-like": ":term:`file-like <python:file object>`",
    "iterator": ":term:`iterator <python:iterator>`",
    "path-like": ":term:`path-like`",
    "array-like": ":term:`array_like <numpy:array_like>`",
    "Path": ":class:`python:pathlib.Path`",

    # Matplotlib
    "colormap": ":ref:`colormap <matplotlib:colormaps>`",
    "color": ":doc:`color <matplotlib:api/colors_api>`",
    "Axes": "matplotlib.axes.Axes",
    "Figure": "matplotlib.figure.Figure",
    "Axes3D": "mpl_toolkits.mplot3d.axes3d.Axes3D",
    "ColorbarBase": "matplotlib.colorbar.ColorbarBase"
}

numpydoc_xref_ignore = {
    # words
    "and",
    "between",
    "instance",
    "instances",
    "of",
    "default",
    "shape",
    "or",
    "with",
    "length",
    "pair",
    "matplotlib",
    "optional",
    "kwargs",
    "in",
    "dtype",
    "object",

    # sklearn subclasses
    "mapping",
    "to",
    "any",
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Other extension configuration -------------------------------------------

# autodoc / autosummary
autosummary_generate = True
autodoc_default_options = {"inherited-members": None}
