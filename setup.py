#!/usr/bin/env python
import sys
import os
from setuptools import setup, find_packages

# Exit if running on Linux since it's not supported.
if sys.platform.startswith("linux"):
    sys.exit("Error: This package does not support Linux. Please use Windows or MacOS.")

VERSION = "0.1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="mindm",
    version=VERSION,
    description=(
        "Python library for interacting with local installed MindManager(tm) on Windows and MacOS platform. "
    ),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Robert Zaufall",
    url="https://github.com/robertZaufall/mindm",
    #project_urls={
    #    "Documentation": "https://github.com/robertZaufall/mindm/docs",
    #    "Issues": "https://github.com/robertZaufall/mindm/issues",
    #    "CI": "https://github.com/robertZaufall/mindm/actions",
    #    "Changelog": "https://github.com/robertZaufall/mindm/releases",
    #},
    license="MIT License",
    packages=find_packages(),
    install_requires=[
        "pywin32; sys_platform == 'win32'",
        "appscript; sys_platform == 'darwin'",
        "regex",
        "markdown",
        "setuptools",
        "pip",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
)
