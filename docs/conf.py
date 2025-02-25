import os
import sys
from sphinx_pyproject import SphinxConfig

# Add the project root directory to the Python path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('..'))

config = SphinxConfig("../pyproject.toml", globalns=globals())

project = 'mindm'
version = "0.0.3"
release = "0.0.3"
author = 'Robert Zaufall'
copyright = '%Y, Robert Zaufall'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'classic'
html_static_path = ['_static']
html_show_sphinx = False
html_show_sourcelink = False  # Hide "Show Source" links
html_copy_source = False      # Don't copy source files to output
html_theme_options = {
    # Layout options
    'stickysidebar': False,         # Sidebar follows scroll
    'sidebarwidth': '30em',        # Width of the sidebar
    'rightsidebar': False,         # Sidebar on the left side
    'collapsiblesidebar': False,   # Don't use collapsible sidebar (not supported in classic theme)
    'body_max_width': None,        # Maximum content width (None = theme default)
    
    # Colors
    'bgcolor': 'white',            # Main background color
    'textcolor': 'black',          # Main text color
    'linkcolor': '#0072B2',        # Link color
    'visitedlinkcolor': '#9400D3',  # Visited link color
    'relbarbgcolor': 'black',      # Relation bar background color
    'footerbgcolor': '#333333',    # Footer background color
    'headbgcolor': 'white',        # Heading background color
    'headtextcolor': 'black',      # Heading text color
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

def setup(app):
    app.add_css_file('css/custom.css')
