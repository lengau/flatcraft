# Configuration file for the Sphinx documentation builder.
# This file only contains a selection of the most common options.

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'Flatcraft'
copyright = '2024, Flatcraft Contributors'
author = 'Flatcraft Contributors'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output options
html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
    'fixed_sidebar': True,
}

# Language and locale
language = 'en'
locale_dirs = ['locale/']
