# mindm

Python library for interacting with locally installed MindManager™ on Windows and macOS platforms.

[![PyPI version](https://img.shields.io/pypi/v/mindm.svg)](https://pypi.org/project/mindm/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://robertzaufall.github.io/mindm/)

## Installation

Install using `pip`:
```bash
pip install mindm
```

## Getting Started

### Low-level example

Example for iterating over all topics in a mindmap and changing the topic text to uppercase:  
  
```python
import mindm.mindmanager

def iterate_topics(topic):
    text = m.get_text_from_topic(topic)
    m.set_text_to_topic(topic, text.upper())

    subtopics = m.get_subtopics_from_topic(topic)
    for subtopic in subtopics:
        iterate_topics(subtopic)

m = mindm.mindmanager.Mindmanager()
central_topic = m.get_central_topic()
iterate_topics(central_topic)
```

### High-level examples
  
Example for loading a mindmap from an open mindmap document and cloning it to a new document:  
  
```python
import mindmap.mindmap as mm

document = mm.MindmapDocument()
document.get_mindmap()
document.create_mindmap()
```
  
Example for serializing a mindmap to YAML format:  
  
```python
import yaml
import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

yaml_data = mms.serialize_object(document.mindmap, guid_mapping)
print(yaml.dump(yaml_data, sort_keys=False))
```
  
Example for serializing / deserializing a mindmap to / from Mermaid format including all attributes:  
  
```python
import json
import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

serialized = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
print(serialized)

deserialized = mms.deserialize_mermaid_full(serialized, guid_mapping)
print(json.dumps(mms.serialize_object_simple(deserialized), indent=1))

document_new = mm.MindmapDocument()
document_new.mindmap = deserialized
document_new.create_mindmap()
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