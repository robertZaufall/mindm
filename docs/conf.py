import os
import sys
import datetime
from sphinx_pyproject import SphinxConfig

# Add the project root directory to the Python path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('..'))

config = SphinxConfig("../pyproject.toml", globalns=globals())

project = 'mindm'
version = config.version
release = config.version
author = 'Robert Zaufall'
copyright = f"{datetime.datetime.now().year}, Robert Zaufall"

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']
html_show_sphinx = False
html_show_sourcelink = False  # Hide "Show Source" links
html_copy_source = False      # Don't copy source files to output
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0072B2",
        "color-brand-content": "#0072B2",
    },
    "dark_css_variables": {
        "color-brand-primary": "#6BA7D6",
        "color-brand-content": "#6BA7D6",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

extensions = [
    "sphinx.ext.autodoc",     # Extract docstrings from your modules
    "sphinx.ext.napoleon",    # Support Google/NumPy style docstrings
    "sphinx.ext.autosummary", # Generate summary tables
]

html_sourcelink_suffix = ''  # Use .py file extension for source links

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "special-members": "__init__",
    "inherited-members": True,
}

autodoc_mock_imports = [
    "win32com",
    "winreg",
    "appscript",
]

html_css_files = ['css/custom.css']

def setup(app):
    app.add_css_file('css/custom.css')
