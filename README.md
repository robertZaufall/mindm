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
  
Supported:
- topics (central topic + subtopics)
- notes
- icons
- images
- tags
- links (external and topic links)
- relationships
- rtf
  
Not supported:
- floating topics
- callouts
- colors, lines, boundaries
  
### MacOS
  
Supported:
- topics (central topic + subtopics)
- notes
- relationships
  
Not supported:
- icons
- images
- tags
- links (external and topic links)
- rtf
- floating topics
- callouts
- colors, lines, boundaries
  
## Development
  
```bash
git clone htpps://gtihub.com/robertZaufall/mindm
python3 -m pip install --upgrade build
python3 -m build
pip install --upgrade pip
pip install -e .
python3 ./tests/clone_map_by_dom.py
```

High level functions of the mindmap_helper-class:  
| Function Name                            | Description                                                                                  |
|------------------------------------------|----------------------------------------------------------------------------------------------|
| get_max_topic_level                      | Recursively finds the highest level among subtopics.                                         |
| get_parent_topic                         | Retrieves the parent topic of a given topic (if any).                                        |
| get_selection                            | Returns a list of selected topics as MindmapTopic objects.                                   |
| get_mindmap_topic_from_topic             | Builds a MindmapTopic (with subtopics) from a given MindManager topic.                       |
| get_relationships_from_mindmap           | Collects relationship references by recursively traversing subtopics.                        |
| get_topic_links_from_mindmap             | Gathers link references from each topic by traversing subtopics.                             |
| get_tags_from_mindmap                    | Collects unique tags from the entire subtopic tree.                                          |
| get_parents_from_mindmap                 | Maps child GUIDs to their parent GUIDs during recursion.                                     |
| get_map_icons_and_fix_refs_from_mindmap  | Updates or reuses custom icons while traversing subtopics.                                   |
| get_topic_texts_from_selection           | Returns lists of selected topics’ texts, levels, and GUIDs.                                  |
| clone_mindmap_topic                      | Creates a new MindmapTopic object, optionally duplicating subtopics.                         |
| set_topic_from_mindmap_topic             | Places a MindmapTopic into the MindManager document, handling subtopics.                     |
| create_mindmap                           | Generates a new MindManager document, sets icons, tags, and topics.                          |
| create_mindmap_and_finalize              | Calls create_mindmap then finalizes map creation.                                            |
| finalize                                 | Completes the mind map by finalizing its maximum level.                                      |
| set_background_image                     | Applies an image to the document background.                                                 |
| get_library_folder                       | Returns the library folder path from Mindmanager.                                            |
| get_grounding_information                | Retrieves selected topic texts and their levels or falls back to the central topic.          |

Raw functions of the mindmanager-class on Windows:  
| Function Name                  | Description                                                                                   |
|--------------------------------|-----------------------------------------------------------------------------------------------|
| get_mindmanager_version        | Returns a String containing MindManager version number (e.g. "26", "25", etc.)                |
| document_exists                | Returns a Boolean indicating if document exists                                               |
| get_central_topic              | Returns the central topic from active document                                                |
| get_topic_by_id                | Returns a topic if found by GUID                                                              |
| get_selection                  | Returns a list of selected topics                                                             |
| get_level_from_topic           | Returns the level value (numeric) from a topic                                                |
| get_text_from_topic            | Returns the topic text                                                                        |
| get_title_from_topic           | Returns the topic title or RTF content                                                        |
| get_subtopics_from_topic       | Returns a list of subtopic objects                                                            |
| get_links_from_topic           | Returns a list of links                                                                       |
| get_image_from_topic           | Returns the image path of a topic image                                                       |
| get_icons_from_topic           | Returns a list of icon objects                                                                |
| get_notes_from_topic           | Returns the notes of a topic                                                                  |
| get_tags_from_topic            | Returns a list of tag objects                                                                 |
| get_references_from_topic      | Returns a list of relationship objects                                                        |
| get_guid_from_topic            | Returns the topic GUID                                                                        |
| get_parent_from_topic          | Returns a topic’s parent                                                                      |
| add_subtopic_to_topic          | Adds a new subtopic to a topic and returns it                                                 |
| set_topic_from_mindmap_topic   | Updates the topic and returns a tuple of (topic object, topic GUID)                           |
  
Raw functions of the mindmanager-class on MacOS:  
| Function Name                    | Description                                                           |
|----------------------------------|-----------------------------------------------------------------------|
| document_exists                  | Returns a Boolean indicating document availability                    |
| get_central_topic                | Returns the central topic from active document                        |
| get_topic_by_id                  | Returns a topic if found by guid                                      |
| get_selection                    | Returns a list of selected topics                                     |
| get_level_from_topic             | Returns the level value (numeric) from a topic                        |
| get_text_from_topic              | Returns the topic text                                                |
| get_title_from_topic             | Returns the title from a topic                                        |
| get_subtopics_from_topic         | Returns a list of subtopics                                           |
| get_notes_from_topic             | Returns the notes of a topic                                          |
| get_references_from_topic        | Returns a list of relationship objects                                |
| get_guid_from_topic              | Returns the topic guid                                                |
| get_parent_from_topic            | Returns a topic’s parent                                              |
| add_subtopic_to_topic            | Adds a new subtopic to a topic and returns it                         |
| set_topic_from_mindmap_topic     | Updates the topic and returns a tuple of (topic object, topic guid)   |

