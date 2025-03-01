# mindm

Python library for interacting with locally installed MindManager™ on Windows and macOS platforms.

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://robertzaufall.github.io/mindm/)

## Installation

Install using `pip`:
```bash
pip install mindm
```

## Getting Started

Example for loading a mindmap from an open mindmap document and cloning it to a new document:
```python
import mindm.mindmap_helper as mm

document = mm.MindmapDocument()
if not document.get_mindmap():
    print("No mindmap found.")
else:
    document.create_mindmap()
```

## Platform Specific Functionality

### Windows

Supported:
- topics (central topic + subtopics)
- notes
- icons
- images
- tags
- links (external and topic links)
- relationships
- rtf

Not Supported:
- floating topics
- callouts
- colors, lines, boundaries

### macOS

Supported:
- topics (central topic + subtopics)
- notes
- relationships

Not Supported:
- icons
- images
- tags
- links
- rtf
- floating topics
- callouts
- colors, lines, boundaries

## Development

### Installation

```bash
git clone https://github.com/robertZaufall/mindm

pip install --upgrade build
python -m build

pip install -e .
pip install --extra-index-url https://pypi.org/simple mindm

# run tests
python -m unittest discover tests

# execute example script to clone an open mindmap
python ./examples/clone_map_by_dom.py
```

### Documentation
[Link to GitHub Pages](https://robertzaufall.github.io/mindm/)