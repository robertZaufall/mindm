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
import mindmap.mindmap as mm

# load and clone mindmap to new a document
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

## Documentation
[Link to GitHub Pages](https://robertzaufall.github.io/mindm/)