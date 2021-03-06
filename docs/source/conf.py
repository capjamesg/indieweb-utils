# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Project information

project = "IndieWeb Utils"
copyright = "capjamesg 2021"
author = "capjamesg"

sys.path.insert(0, os.path.abspath("../../src/"))

release = "0.2.0"
version = "0.2.0"

# -- General configuration

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
