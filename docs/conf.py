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
    "win32com.client",
    "winreg",
    "appscript",
    "pythoncom",
    "pywintypes",
    "_winreg",  # Alternative name sometimes used
]

html_css_files = ['css/custom.css']

def setup(app):
    app.add_css_file('css/custom.css')
    
    # Enhanced mocking for Windows modules
    from unittest.mock import Mock
    import sys
    import types
    
    # Create a specialized mock that avoids recursion issues
    class SafeMock(Mock):
        # Cache to prevent infinite recursion
        _attribute_cache = {}
        
        def __getattr__(self, name):
            if name in self._attribute_cache:
                return self._attribute_cache[name]
            
            result = SafeMock()
            self._attribute_cache[name] = result
            return result
            
    # Set up mock objects for all Windows-specific modules
    MOCK_MODULES = [
        'win32com', 
        'win32com.client',
        'winreg',
        'pythoncom', 
        'pywintypes',
        '_winreg'
    ]
    
    # Create the mocks
    for mod_name in MOCK_MODULES:
        parts = mod_name.split('.')
        
        # Handle root module
        if len(parts) == 1:
            sys.modules[mod_name] = SafeMock()
        # Handle submodules
        else:
            parent_mod_name = ".".join(parts[:-1])
            child_name = parts[-1]
            
            # Ensure parent module exists
            if parent_mod_name not in sys.modules:
                # For parent modules, use a simple ModuleType to avoid recursion
                parent_mod = types.ModuleType(parent_mod_name)
                sys.modules[parent_mod_name] = parent_mod
            else:
                parent_mod = sys.modules[parent_mod_name]
            
            # Create child module as a SafeMock
            child_mod = SafeMock()
            sys.modules[mod_name] = child_mod
            
            # Set child as attribute of parent
            setattr(parent_mod, child_name, child_mod)
    
    # Specific common attributes that might be accessed
    win32com = sys.modules.get('win32com')
    if win32com and hasattr(win32com, 'client'):
        win32com.client.Dispatch = SafeMock()
        win32com.client.constants = SafeMock()
