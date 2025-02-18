# mindm

Python library for interacting with local installed MindManager(tm) on Windows and MacOS platform.

## Installation

Install using `pip`:
```bash
pip install mindm
```

## Getting started

Example for loading a mindmap from an open mindmap document and cloning it to a new document:  
```python
import mindm.mindmap_helper as mm

document = mm.MindmapDocument()
if not document.get_mindmap():
    print("No mindmap found.")
else:
    document.create_mindmap()
```

## Platform specific functionality

### Windows

### MacOS