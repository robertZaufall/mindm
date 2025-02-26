# mindm

Python library for interacting with local installed MindManager(tm) on Windows and MacOS platform.

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://robertzaufall.github.io/mindm/)

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
- links
- rtf
- floating topics
- callouts
- colors, lines, boundaries
  
## Development
  
### Installation  
  
```bash
git clone htpps://github.com/robertZaufall/mindm

pip install --upgrade build
python -m build

pip install -e .
pip install --extra-index-url https://pypi.org/simple mindm

python ./tests/clone_map_by_dom.py
```
  
### High level functions (mindmap_helper-class)  
  
High level functions of the mindmap_helper-class:  
| Function | Parameters | Description |
|---|---|---|
| `__init__` | - charttype: str = 'auto'<br>- turbo_mode: bool = False<br>- inline_editing_mode: bool = False<br>- mermaid_mode: bool = True | Initialize a MindmapDocument instance which automates MindManager operations. |
| `get_mindmap` | - topic (default: None) | Retrieve the mind map structure from the currently open MindManager document. |
| `get_max_topic_level` | - mindmap_topic<br>- max_topic_level (default: 0)<br>- visited (default: None) | Recursively compute the maximum topic level within the mind map. |
| `get_parent_topic` | - topic | Retrieve the parent topic for a given MindManager topic. |
| `get_selection` | None | Retrieve the currently selected topics in the MindManager document. |
| `get_mindmap_topic_from_topic` | - topic<br>- parent_topic (default: None) | Recursively convert a MindManager topic into a MindmapTopic object. |
| `get_relationships_from_mindmap` | - mindmap<br>- references<br>- visited (default: None) | Recursively extract relationships (references) from the mindmap. |
| `get_topic_links_from_mindmap` | - mindmap<br>- links<br>- visited (default: None) | Recursively extract topic links from the mindmap. |
| `get_tags_from_mindmap` | - mindmap<br>- tags<br>- visited (default: None) | Recursively collect unique tags from the mindmap. |
| `get_parents_from_mindmap` | - mindmap<br>- parents<br>- visited (default: None) | Build a dictionary mapping subtopic GUIDs to their parent's GUID. |
| `get_map_icons_and_fix_refs_from_mindmap` | - mindmap<br>- map_icons: list['MindmapIcon']<br>- visited (default: None) | Extract icons from mindmap topics and fix their references if needed. |
| `count_parent_and_child_occurrences` | - mindmap_topic<br>- guid_counts<br>- visited (default: None) | Recursively count the occurrences of parent and child relationships for each topic. |
| `get_topic_texts_from_selection` | - mindmap_topics | Extract topic texts, levels, and GUIDs from selected topics. |
| `clone_mindmap_topic` | - mindmap_topic<br>- subtopics: list['MindmapTopic'] (optional, default: None)<br>- parent (optional) | Clone a MindmapTopic instance including its subtopics. |
| `update_done` | - topic_guid<br>- mindmap_topic<br>- level<br>- done<br>- done_global | Update tracking dictionaries for processed topics and create duplicate links/tags. |
| `set_topic_from_mindmap_topic` | - topic<br>- mindmap_topic<br>- map_icons<br>- done (optional, default: None)<br>- done_global (optional, default: None)<br>- level (default: 0) | Create or update a MindManager topic from a MindmapTopic instance recursively. |
| `check_parent_exists` | - topic_guid<br>- this_guid<br>- visited (default: None) | Recursively check if a parent-child relationship exists between topics. |
| `create_mindmap` | - verbose (default: False) | Create a MindManager mindmap document from the internal MindmapTopic structure. This includes counting occurrences, extracting tags/icons, and setting up relationships and links. |
| `create_mindmap_and_finalize` | None | Create the mindmap document and finalize it. |
| `finalize` | None | Finalize the mindmap document by ensuring the maximum topic level is set, then calling MindManager's finalize. |
| `set_background_image` | - image_path | Set the background image for the MindManager document. |
| `get_library_folder` | None | Get the library folder used by MindManager. |
| `get_grounding_information` | None | Extract grounding information from the mindmap, including the central topic and selected subtopics. |

  
### Low level functions (mindmanager-class)  
#### Windows:  
| Function | Description |
| --- | --- |
| `document_exists(self)` | Checks if the active document exists and returns a boolean value accordingly. |
| `get_mindmanager_version()` | Determines the installed MindManager version by checking registry keys for known version numbers and returns the version string if found. |
| `set_document_background_image(self, path)` | Sets or replaces the document’s background image using the provided file path, applying centering and transparency settings. |
| `get_central_topic(self)` | Retrieves and returns the central (root) topic of the active document. |
| `get_topic_by_id(self, id)` | Finds and returns a topic in the document based on its unique GUID. |
| `get_selection(self)` | Returns a list of currently selected topics in the document by filtering for valid topic objects. |
| `get_level_from_topic(self, topic)` | Returns the hierarchical level of a given topic. |
| `get_text_from_topic(self, topic)` | Retrieves and returns the text from a topic after sanitizing it (e.g., replacing quotes and removing line breaks). |
| `get_title_from_topic(self, topic)` | Retrieves and returns the title of a topic in rich text format (RTF), if available. |
| `get_subtopics_from_topic(self, topic)` | Returns all subtopics of the specified topic. |
| `get_links_from_topic(self, topic) -> list[MindmapLink]` | Extracts and returns a list of hyperlinks from a topic as `MindmapLink` objects. |
| `get_image_from_topic(self, topic) -> MindmapImage` | If the topic contains an image, saves it temporarily as a PNG file and returns it wrapped in a `MindmapImage` object. |
| `get_icons_from_topic(self, topic) -> list[MindmapIcon]` | Retrieves both stock and custom icons from a topic, returning them as a list of `MindmapIcon` objects. |
| `get_notes_from_topic(self, topic) -> MindmapNotes` | Extracts the notes from a topic (in RTF, XHTML, or plain text) and returns them as a `MindmapNotes` object. |
| `get_tags_from_topic(self, topic) -> list[MindmapTag]` | Retrieves text labels (tags) from a topic and returns them as a list of `MindmapTag` objects. |
| `get_references_from_topic(self, topic) -> list[MindmapReference]` | Gathers relationships (references) from a topic and returns them as a list of `MindmapReference` objects, including directional information. |
| `get_guid_from_topic(self, topic) -> str` | Returns the GUID (unique identifier) of the given topic. |
| `add_subtopic_to_topic(self, topic, topic_text)` | Adds a new subtopic with the provided text to the given topic and returns the newly created subtopic. |
| `get_parent_from_topic(self, topic)` | Retrieves and returns the parent topic of the specified topic. |
| `set_text_to_topic(self, topic, topic_text)` | Sets the text content of a topic to the provided string. |
| `set_title_to_topic(self, topic, topic_rtf)` | Sets the title of a topic using rich text format if a non-empty RTF string is provided. |
| `add_tag_to_topic(self, tag_text, topic=None, topic_guid=None)` | Adds a tag (text label) to a topic; the topic can be provided directly or looked up via its GUID. |
| `set_topic_from_mindmap_topic(self, topic, mindmap_topic, map_icons)` | Updates a topic’s properties—text, title, tags, notes, icons, image, and links—based on the provided `mindmap_topic` data and returns the updated topic along with its GUID. |
| `add_links_to_topic(self, topic, mindmap_topic_links)` | Iterates through a list of link objects and adds them as hyperlinks to the specified topic. |
| `add_image_to_topic(self, topic, mindmap_topic_image)` | Adds an image to the topic using the file path provided in a `MindmapImage` object. |
| `add_icons_to_topic(self, topic, mindmap_topic_icons, map_icons)` | Adds icons to a topic from a list of `MindmapIcon` objects, handling both stock icons and custom icons (with optional mapping). |
| `set_notes_to_topic(self, topic, mindmap_topic_notes)` | Sets the notes for a topic using the provided `MindmapNotes` object, choosing between plain text, XHTML, or RTF as available. |
| `add_tags_to_topic(self, topic, mindmap_topic_tags)` | Adds multiple tags to a topic by iterating over a list of `MindmapTag` objects. |
| `create_map_icons(self, map_icons)` | Creates and groups custom map icons in the document from a list of map icon objects and assigns them custom signatures. |
| `create_tags(self, tags: list['str'], DUPLICATED_TAG: str)` | Creates tags in the document using a mandatory marker group, adding each tag from the list and ensuring a duplicated tag is included if specified. |
| `add_relationship(self, guid1, guid2, label='')` | Adds a relationship between two topics (identified by their GUIDs) unless they share a parent-child relationship, optionally with a label. |
| `add_topic_link(self, guid1, guid2, label='')` | Creates a hyperlink from one topic to another (using GUIDs) with an optional label (defaulting to the target topic’s title). |
| `add_document(self, max_topic_level)` | Creates a new document by copying the style from the current one and sets it as the active document. |
| `finalize(self, max_topic_level)` | Finalizes the document layout by adjusting topic collapse levels and growth directions based on the chart type and topic hierarchy, then zooms and displays the MindManager application. |

  
#### MacOS:  
| Function | Description |
| --- | --- |
| `document_exists(self)` | Checks whether a MindManager document exists, returning `True` if it does and `False` otherwise. |
| `get_central_topic(self)` | Retrieves the central topic from the active MindManager document. |
| `get_topic_by_id(self, id)` | Finds and returns a topic by its unique identifier; returns `None` if the topic isn’t found. |
| `get_selection(self)` | Retrieves the current selection in the document and filters it to include only topics. |
| `get_level_from_topic(self, topic)` | Returns the hierarchical level (depth) of the specified topic. |
| `get_text_from_topic(self, topic)` | Retrieves and sanitizes the text from a topic by replacing certain characters and removing line breaks. |
| `get_title_from_topic(self, topic)` | Retrieves the title (rich text) of the given topic. |
| `get_subtopics_from_topic(self, topic)` | Returns the list of subtopics for the specified topic. |
| `get_notes_from_topic(self, topic)` | Retrieves the notes from a topic and returns them encapsulated in a `MindmapNotes` object. |
| `get_references_from_topic(self, topic)` | Extracts relationships from a topic and returns them as a list of `MindmapReference` objects. |
| `get_guid_from_topic(self, topic)` | Retrieves the unique identifier (GUID) of the specified topic. |
| `get_parent_from_topic(self, topic)` | Retrieves the parent topic of the provided topic. |
| `add_subtopic_to_topic(self, topic, topic_text)` | Adds a new subtopic with the given text to the specified topic. |
| `set_text_to_topic(self, topic, topic_text)` | Updates the text of a topic with the provided string. |
| `set_title_to_topic(self, topic, topic_rtf)` | Sets the title (rich text) of a topic with the provided content. |
| `set_topic_from_mindmap_topic(self, topic, mindmap_topic, map_icons)` | Updates a topic’s properties (text, title, and notes) based on a given MindmapTopic object and refreshes the topic reference. |
| `add_relationship(self, guid1, guid2, label='')` | Creates a relationship between two topics identified by their GUIDs. |
| `add_document(self, max_topic_level)` | Opens a new document using a template (org-chart or radial) chosen based on the chart type, maximum topic level, and number of subtopics. |
| `finalize(self, max_topic_level)` | Balances the map, activates MindManager, optionally merges windows, and cleans up the instance. |

