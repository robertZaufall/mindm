"""
mindm - Python library for interacting with local installed MindManager.

This package provides functionality to interact with MindManager on both
Windows and MacOS platforms. It allows reading, creating, and manipulating
mindmaps programmatically.

Main components:
- mindmap_helper: High-level interface for mindmap operations
- mindmanager: Platform-independent base class
- mindmanager_win: Windows-specific implementations
- mindmanager_mac: MacOS-specific implementations
"""

# Version information
try:
    from importlib.metadata import version as _version
    __version__ = _version("mindm")
except ImportError:
    __version__ = "unknown"