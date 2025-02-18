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
  
### Installation  
  
```bash
git clone htpps://gtihub.com/robertZaufall/mindm
python3 -m pip install --upgrade build
python3 -m build
pip install --upgrade pip
pip install -e .
python3 ./tests/clone_map_by_dom.py
```
  
### High level functions (mindmap_helper-class)  
  
High level functions of the mindmap_helper-class:  
| Function                                                       | Description                                                                                                                                                                                                                  |
|----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `get_mindmap(topic=None)`                                      | Retrieves the current mindmap from MindManager, processes the selection, computes the maximum topic level, and builds the internal mindmap structure.                                                   |
| `get_max_topic_level(mindmap_topic, max_topic_level=0, visited=None)` | Recursively calculates the maximum level (depth) among all topics in the mindmap, ensuring cycles are avoided.                                                                                              |
| `get_parent_topic(topic)`                                      | Returns the parent topic for a given MindManager topic by converting it into an internal `MindmapTopic` representation.                                                                                   |
| `get_selection()`                                              | Retrieves the selected topics from MindManager and returns them as a list of `MindmapTopic` objects with their respective levels and parent information.                                                |
| `get_relationships_from_mindmap(mindmap, references, visited=None)` | Recursively traverses the mindmap to collect relationship references (directional links) between topics and appends them to the provided list.                                                            |
| `get_topic_links_from_mindmap(mindmap, links, visited=None)`   | Recursively collects topic link information from the mindmap into a list of `MindmapReference` objects, avoiding duplicates by tracking visited topics.                                                |
| `get_tags_from_mindmap(mindmap, tags, visited=None)`           | Recursively gathers unique tag texts from the mindmap and appends them to the provided list.                                                                                                               |
| `get_map_icons_and_fix_refs_from_mindmap(mindmap, map_icons: list['MindmapIcon'], visited=None)` | Recursively collects map icons from the mindmap; for non-stock icons in a specific group, it replaces them with shared references from a central list to ensure consistency.                          |
| `get_topic_texts_from_selection(mindmap_topics)`               | Extracts and returns a tuple containing lists of topic texts, levels, IDs, and a flag indicating if the central topic was selected, based on a list of `MindmapTopic` objects.                        |
| `clone_mindmap_topic(mindmap_topic, subtopics: list['MindmapTopic'] = None, parent=None)` | Creates a duplicate (clone) of a given `MindmapTopic`, including recursively cloning its subtopics.                                                                                                        |
| `set_topic_from_mindmap_topic(topic, mindmap_topic, map_icons, done=None, done_global=None, level=0)` | Recursively updates MindManager’s document by creating topics and subtopics that mirror the internal `MindmapTopic` structure, also handling duplicate detection and linking.                      |
| `create_mindmap(verbose=False)`                                | Processes the entire internal mindmap structure to create the MindManager document by generating tags, icons, relationships, and topic links, as well as preparing parent-child mappings.             |
| `create_mindmap_and_finalize()`                                | Combines the mindmap creation and finalization steps, so the MindManager document is built and then finalized in one call.                                                                                 |
| `finalize()`                                                   | Finalizes the MindManager document by applying finishing touches, including updating the document with the maximum topic level determined from the internal structure.                             |
| `set_background_image(image_path)`                             | Sets a background image for the MindManager document using the provided image path.                                                                                                                      |
| `get_library_folder()`                                         | Returns the folder path of the MindManager library, which might contain additional resources or templates used by the document.                                                                           |
| `get_grounding_information()`                                  | Extracts grounding information by combining the central topic’s text with texts from selected subtopics, helping to provide context for further processing or analysis.                              |
  
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

