import uuid

import mindm.mindmanager as mm

DUPLICATED_TAG = 'Duplicated'
DUPLICATE_LABEL = 'DUPLICATE'

class MindmapLink:
    def __init__(self, text: str = '', url: str = '', guid: str = ''):
        """
        Initialize a MindmapLink instance.

        Args:
            text (str): The display text for the link.
            url (str): The URL that the link points to.
            guid (str): A unique identifier for the link.
        """
        self.text = text
        self.url = url
        self.guid = guid

class MindmapImage:
    def __init__(self, text: str = ''):
        """
        Initialize a MindmapImage instance.

        Args:
            text (str): Path to the image.
        """
        self.text = text

class MindmapNotes:
    def __init__(self, text: str = '', xhtml: str = '', rtf: str = ''):
        """
        Initialize a MindmapNotes instance.

        Args:
            text (str): Plain text version of the notes.
            xhtml (str): XHTML formatted notes.
            rtf (str): RTF formatted notes.
        """
        self.text = text
        self.xhtml = xhtml
        self.rtf = rtf

class MindmapIcon:
    def __init__(self, 
                 text: str = '', 
                 is_stock_icon=True, 
                 index: int = 1, 
                 signature: str = '', 
                 path: str = '',
                 group: str = ''):
        """
        Initialize a MindmapIcon instance.

        Args:
            text (str): The display text for the icon.
            is_stock_icon (bool): Flag indicating if the icon is a stock icon.
            index (int): The index of a stock icon.
            signature (str): A unique signature for the icon.
            path (str): File path to the icon if it is custom.
            group (str): The group/category of the icon.
        """
        self.text = text
        self.is_stock_icon = is_stock_icon
        self.index = index
        self.signature = signature
        self.path = path
        self.group = group

class MindmapTag:
    def __init__(self, text: str = ''):
        """
        Initialize a MindmapTag instance.

        Args:
            text (str): The text representing the tag.
        """
        self.text = text

class MindmapReference:
    def __init__(self, 
                 guid_1: str = '', 
                 guid_2: str = '', 
                 direction: int = 1, 
                 label: str = ''):
        """
        Initialize a MindmapReference (relationship) instance.

        Args:
            guid_1 (str): The GUID of the first topic.
            guid_2 (str): The GUID of the second topic.
            direction (int): The direction of the reference (1 indicates a standard direction).
            label (str): A label for the relationship.
        """
        self.guid_1 = guid_1
        self.guid_2 = guid_2
        self.direction = direction
        self.label = label

class MindmapTopic:
    def __init__(self,
                 guid: str = '',
                 text: str = '',
                 rtf: str = '',
                 level: int = 0,
                 selected: bool = False,
                 parent: 'MindmapTopic' = None,
                 subtopics: list['MindmapTopic'] = None,
                 links: list['MindmapLink'] = None,
                 image: 'MindmapImage' = None,
                 icons: list['MindmapIcon'] = None,
                 notes: 'MindmapNotes' = None,
                 tags: list['MindmapTag'] = None,
                 references: list['MindmapReference'] = None):
        """
        Initialize a MindmapTopic instance.

        Args:
            guid (str): Unique identifier for the topic.
            text (str): The text content of the topic.
            rtf (str): RTF formatted text for the topic.
            level (int): The hierarchical level of the topic.
            selected (bool): Flag to indicate if the topic is selected.
            parent (MindmapTopic): The parent topic if any.
            subtopics (list[MindmapTopic]): List of subtopics.
            links (list[MindmapLink]): List of associated links.
            image (MindmapImage): Associated image object.
            icons (list[MindmapIcon]): List of associated icons.
            notes (MindmapNotes): Associated notes.
            tags (list[MindmapTag]): List of associated tags.
            references (list[MindmapReference]): List of associated relationships.
        """
        self.guid = guid
        self.text = text.replace('"', '`').replace("'", "`").replace("\r", "").replace("\n", "")
        self.rtf = rtf
        self.level = level
        self.selected = selected
        self.parent = parent
        self.links = links if links is not None else []
        self.image = image
        self.icons = icons if icons is not None else []
        self.notes = notes
        self.tags = tags if tags is not None else []
        self.references = references if references is not None else []
        self.subtopics = subtopics if subtopics is not None else []


class MindmapDocument:
    def __init__(self, charttype: str = 'auto', turbo_mode: bool = False, inline_editing_mode: bool = False, mermaid_mode: bool = True):
        """
        Initialize a MindmapDocument instance which automates MindManager operations.

        Args:
            charttype (str): The type of chart to be used (orgchart, radial, auto).
            turbo_mode (bool): Flag for enabling turbo mode -> use only text.
            inline_editing_mode (bool): Flag for enabling inline editing mode.
            mermaid_mode (bool): Flag for enabling mermaid mode.
        """
        self.charttype: str = charttype
        self.turbo_mode: bool = turbo_mode
        self.inline_editing_mode: bool = inline_editing_mode
        self.mermaid_mode: bool = mermaid_mode
        self.mindmap: 'MindmapTopic' = None
        self.central_topic_selected: bool = False
        self.selected_topic_texts: list[str] = []
        self.selected_topic_levels: list[int] = []
        self.selected_topic_ids: list[str] = []
        self.max_topic_level: int = 0

        self.mindm = mm.Mindmanager(charttype)

    def get_mindmap(self, topic=None):
        """
        Retrieve the mind map structure from the currently open MindManager document.

        Args:
            topic: (Optional) A specific topic from which to start building the mindmap.
                   If not provided, the central topic is used.

        Returns:
            bool: True if the mind map was successfully retrieved, otherwise False.
        """
        if not self.mindm.document_exists():
            print("No document found. Please open MindManager with a document.")    
            return False

        if topic is None:
            topic = self.mindm.get_central_topic()
        
        # Build the mindmap topic structure from the provided topic
        mindmap = self.get_mindmap_topic_from_topic(topic)

        # Retrieve the current selection information
        selection = self.get_selection()
        selected_topic_texts, selected_topic_levels, selected_topic_ids, central_topic_selected = self.get_topic_texts_from_selection(selection)
        self.central_topic_selected = central_topic_selected
        self.selected_topic_texts = selected_topic_texts
        self.selected_topic_levels = selected_topic_levels
        self.selected_topic_ids = selected_topic_ids
        self.max_topic_level = self.get_max_topic_level(mindmap)
        self.mindmap = mindmap
        return True
    
    def get_max_topic_level(self, mindmap_topic, max_topic_level=0, visited=None):
        """
        Recursively compute the maximum topic level within the mind map.

        Args:
            mindmap_topic (MindmapTopic): The current topic to evaluate.
            max_topic_level (int): The current maximum level found.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.

        Returns:
            int: The highest topic level found in the mindmap.
        """
        if visited is None:
            visited = set()
        if mindmap_topic.guid in visited:
            return max_topic_level
        visited.add(mindmap_topic.guid)
        for subtopic in mindmap_topic.subtopics:
            if subtopic.level > max_topic_level:
                max_topic_level = subtopic.level
            max_topic_level = self.get_max_topic_level(subtopic, max_topic_level, visited)
        return max_topic_level

    def get_parent_topic(self, topic):
        """
        Retrieve the parent topic for a given MindManager topic.

        Args:
            topic: The current topic from which to get the parent.

        Returns:
            MindmapTopic or None: The parent topic wrapped as a MindmapTopic, or None if at the root.
        """
        topic_level = self.mindm.get_level_from_topic(topic)
        if topic_level == 0:
            return None
        parent_topic = self.mindm.get_parent_from_topic(topic)
        parent_mindmap_topic = MindmapTopic(
            guid=self.mindm.get_guid_from_topic(parent_topic),
            text=self.mindm.get_text_from_topic(parent_topic), 
            level=self.mindm.get_level_from_topic(parent_topic),
            parent=self.get_parent_topic(parent_topic),
        )
        return parent_mindmap_topic

    def get_selection(self):
        """
        Retrieve the currently selected topics in the MindManager document.

        Returns:
            list[MindmapTopic]: A list of MindmapTopic instances representing the selection.
        """
        selection = self.mindm.get_selection()
        mindmap_topics = []
        for topic in selection:
            level = self.mindm.get_level_from_topic(topic)
            mindmap_topic = MindmapTopic(
                guid=self.mindm.get_guid_from_topic(topic),
                text=self.mindm.get_text_from_topic(topic), 
                level=level,
                parent=self.get_parent_topic(topic),
                selected=True,
            )
            mindmap_topics.append(mindmap_topic)
        return mindmap_topics

    def get_mindmap_topic_from_topic(self, topic, parent_topic=None):
        """
        Recursively convert a MindManager topic into a MindmapTopic object.

        Args:
            topic: The current MindManager topic to convert.
            parent_topic (MindmapTopic): The parent MindmapTopic, if any.

        Returns:
            MindmapTopic: The converted topic with its subtopics.
        """
        mindmap_topic = MindmapTopic(
            guid=self.mindm.get_guid_from_topic(topic),
            text=self.mindm.get_text_from_topic(topic),
            rtf=self.mindm.get_title_from_topic(topic),
            level=self.mindm.get_level_from_topic(topic),
            links=self.mindm.get_links_from_topic(topic),
            image=self.mindm.get_image_from_topic(topic),
            icons=self.mindm.get_icons_from_topic(topic),
            notes=self.mindm.get_notes_from_topic(topic),
            tags=self.mindm.get_tags_from_topic(topic),
            references=self.mindm.get_references_from_topic(topic),
            parent=parent_topic,
        )
        subtopics = self.mindm.get_subtopics_from_topic(topic)
        mindmap_subtopics = []
        for subtopic in subtopics:
            child = self.get_mindmap_topic_from_topic(subtopic, mindmap_topic)
            mindmap_subtopics.append(child)
        mindmap_topic.subtopics = mindmap_subtopics
        return mindmap_topic 

    def get_relationships_from_mindmap(self, mindmap, references, visited=None):
        """
        Recursively extract relationships (references) from the mindmap.

        Args:
            mindmap (MindmapTopic): The current topic in the mindmap.
            references (list[MindmapReference]): List to collect the relationships.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if mindmap.guid in visited:
            return
        visited.add(mindmap.guid)
        for reference in mindmap.references:
            if reference.direction == 1:
                references.append(MindmapReference(
                    guid_1=reference.guid_1,
                    guid_2=reference.guid_2,
                    direction=reference.direction,
                    label=reference.label
                ))
        for subtopic in mindmap.subtopics:
            self.get_relationships_from_mindmap(subtopic, references, visited)

    def get_topic_links_from_mindmap(self, mindmap, links, visited=None):
        """
        Recursively extract topic links from the mindmap.

        Args:
            mindmap (MindmapTopic): The current topic in the mindmap.
            links (list[MindmapReference]): List to collect topic links as MindmapReference objects.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if mindmap.guid in visited:
            return
        visited.add(mindmap.guid)
        for link in mindmap.links:
            if link.guid != '':
                links.append(MindmapReference(
                    guid_1=mindmap.guid, 
                    guid_2=link.guid, 
                    direction=1, 
                    label=link.text
                ))
        for subtopic in mindmap.subtopics:
            self.get_topic_links_from_mindmap(subtopic, links, visited)

    def get_tags_from_mindmap(self, mindmap, tags, visited=None):
        """
        Recursively collect unique tags from the mindmap.

        Args:
            mindmap (MindmapTopic): The current topic in the mindmap.
            tags (list[str]): List to collect tag texts.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if mindmap.guid in visited:
            return
        visited.add(mindmap.guid)
        for tag in mindmap.tags:
            if tag.text != '' and tag.text not in tags:
                tags.append(tag.text)
        for subtopic in mindmap.subtopics:
            self.get_tags_from_mindmap(subtopic, tags, visited)

    def get_parents_from_mindmap(self, mindmap, parents, visited=None):
        """
        Build a dictionary mapping subtopic GUIDs to their parent's GUID.

        Args:
            mindmap (MindmapTopic): The current topic in the mindmap.
            parents (dict): Dictionary to store parent-child GUID mappings.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if mindmap.guid in visited:
            return
        visited.add(mindmap.guid)
        for subtopic in mindmap.subtopics:
            if subtopic.guid not in parents:
                parents[subtopic.guid] = mindmap.guid
                self.get_parents_from_mindmap(subtopic, parents, visited)
        return

    def get_map_icons_and_fix_refs_from_mindmap(self, mindmap, map_icons: list['MindmapIcon'], visited=None):
        """
        Extract icons from mindmap topics and fix their references if needed.

        Args:
            mindmap (MindmapTopic): The current topic in the mindmap.
            map_icons (list[MindmapIcon]): List to collect unique icons.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if mindmap.guid in visited:
            return
        visited.add(mindmap.guid)
        
        for i, topic_icon_ref in enumerate(mindmap.icons):
            # Only process non-stock icons belonging to the 'Types' group
            if not topic_icon_ref.is_stock_icon and topic_icon_ref.group == 'Types':
                found = False
                for map_icon in map_icons:
                    if map_icon.signature == topic_icon_ref.signature:
                        found = True
                        new_icon = map_icon
                        break
                if not found:
                    new_icon = MindmapIcon(
                        text=topic_icon_ref.text, 
                        index=topic_icon_ref.index,
                        is_stock_icon=topic_icon_ref.is_stock_icon, 
                        path=topic_icon_ref.path,
                        signature=topic_icon_ref.signature,
                        group=topic_icon_ref.group)                
                    map_icons.append(new_icon)
                mindmap.icons[i] = new_icon
        for subtopic in mindmap.subtopics:
            self.get_map_icons_and_fix_refs_from_mindmap(subtopic, map_icons, visited)

    def count_parent_and_child_occurrences(self, mindmap_topic, guid_counts, visited=None):
        """
        Recursively count the occurrences of parent and child relationships for each topic.

        Args:
            mindmap_topic (MindmapTopic): The current topic in the mindmap.
            guid_counts (dict): Dictionary to store counts with topic GUID as keys.
            visited (set): Set of visited topic GUIDs to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if str(mindmap_topic.guid) == '':
            mindmap_topic.guid = str(uuid.uuid4())
        if mindmap_topic.guid not in visited:
            visited.add(mindmap_topic.guid)
            if mindmap_topic.guid not in guid_counts:
                guid_counts[mindmap_topic.guid] = {'parent': 0, 'child': 0}
            for subtopic in mindmap_topic.subtopics:
                if mindmap_topic.guid:
                    guid_counts[mindmap_topic.guid]['parent'] += 1
                if subtopic.guid:
                    if subtopic.guid not in guid_counts:
                        guid_counts[subtopic.guid] = {'parent': 0, 'child': 0}
                    guid_counts[subtopic.guid]['child'] += 1
                self.count_parent_and_child_occurrences(subtopic, guid_counts, visited)

    def get_topic_texts_from_selection(self, mindmap_topics):
        """
        Extract topic texts, levels, and GUIDs from selected topics.

        Args:
            mindmap_topics (list[MindmapTopic]): List of topics to process.

        Returns:
            tuple: (list of topic texts, list of topic levels, list of topic GUIDs, bool indicating if the central topic is selected)
        """
        topic_texts = []
        topic_levels = []
        topic_ids = []
        central_topic_selected = False
        for topic in mindmap_topics:
            if topic.selected:
                if topic.level > 0:
                    topic_texts.append(topic.text)
                    topic_levels.append(topic.level)
                    topic_ids.append(topic.guid)
                else:
                    central_topic_selected = True
        return topic_texts, topic_levels, topic_ids, central_topic_selected
            
    def clone_mindmap_topic(self, mindmap_topic, subtopics: list['MindmapTopic'] = None, parent=None):
        """
        Clone a MindmapTopic instance including its subtopics.

        Args:
            mindmap_topic (MindmapTopic): The topic to clone.
            subtopics (list[MindmapTopic], optional): A list of subtopics to clone.
            parent: The parent for the cloned topic.

        Returns:
            MindmapTopic: A new instance that is a clone of the given topic.
        """
        cloned_subtopics = []
        if subtopics is not None:
            for subtopic in subtopics:
                cloned_subtopic = self.clone_mindmap_topic(subtopic)
                cloned_subtopics.append(cloned_subtopic)
        return MindmapTopic(
            guid=mindmap_topic.guid,
            text=mindmap_topic.text, 
            rtf=mindmap_topic.rtf,
            level=mindmap_topic.level,
            parent=parent,
            links=mindmap_topic.links,
            image=mindmap_topic.image,
            icons=mindmap_topic.icons,
            notes=mindmap_topic.notes,
            tags=mindmap_topic.tags,
            subtopics=cloned_subtopics
        )

    def update_done(self, topic_guid, mindmap_topic, level, done, done_global):
        """
        Update tracking dictionaries for processed topics and create duplicate links/tags.

        Args:
            topic_guid (str): The GUID of the current topic in MindManager.
            mindmap_topic (MindmapTopic): The MindmapTopic being processed.
            level (int): The current level in the topic hierarchy.
            done (dict): Dictionary tracking topics processed at a given level.
            done_global (dict): Global dictionary tracking processed topics for duplicate detection.
        """
        if mindmap_topic.guid == '':
            return
        if level <= 1:
            done = {}
        elif level >= 2: 
            done[mindmap_topic.guid] = [topic_guid] if mindmap_topic.guid not in done else done[mindmap_topic.guid] + [topic_guid]
        if mindmap_topic.guid in done_global:
            # Check for duplicate relationships and add links/tags accordingly.
            if self.guid_counts[mindmap_topic.guid]['child'] < 11 and self.guid_counts[mindmap_topic.guid]['parent'] >= 0:
                for i in range(len(done_global[mindmap_topic.guid])):
                    link_from = topic_guid
                    link_to = done_global[mindmap_topic.guid][i]
                    self.mindm.add_topic_link(link_from, link_to, DUPLICATE_LABEL)
                    self.mindm.add_topic_link(link_to, link_from, DUPLICATE_LABEL)
                if len(done_global[mindmap_topic.guid]) == 1:
                    self.mindm.add_tag_to_topic(topic=None, tag_text=DUPLICATED_TAG, topic_guid=done_global[mindmap_topic.guid][0])
            self.mindm.add_tag_to_topic(topic=None, tag_text=DUPLICATED_TAG, topic_guid=topic_guid)
            done_global[mindmap_topic.guid] = done_global[mindmap_topic.guid] + [topic_guid]
        else:
            done_global[mindmap_topic.guid] = [topic_guid]

    def set_topic_from_mindmap_topic(self, topic, mindmap_topic, map_icons, done=None, done_global=None, level=0):
        """
        Create or update a MindManager topic from a MindmapTopic instance recursively.

        Args:
            topic: The current MindManager topic to update.
            mindmap_topic (MindmapTopic): The source MindmapTopic data.
            map_icons (list[MindmapIcon]): List of map icons to use.
            done (dict, optional): Dictionary tracking processed topics at current level.
            done_global (dict, optional): Global dictionary for tracking duplicate processing.
            level (int): Current hierarchical level.
            
        Returns:
            MindmapTopic: The processed MindmapTopic.
        """
        if done is None:
            done = {}
        if done_global is None:
            done_global = {}
        try:
            if self.turbo_mode:
                topic_guid = self.mindm.get_guid_from_topic(topic)
                self.update_done(topic_guid, mindmap_topic, level, done, done_global)
                for subtopic in mindmap_topic.subtopics:
                    try:
                        sub = self.mindm.add_subtopic_to_topic(topic, subtopic.text)
                        self.set_topic_from_mindmap_topic(sub, subtopic, map_icons, done, done_global, level + 1)
                    except Exception as e:
                        print(f"Error(1) processing topic/subtopic {mindmap_topic.guid}/{subtopic.guid}: {e}")
            else:
                topic, topic_guid = self.mindm.set_topic_from_mindmap_topic(topic, mindmap_topic, map_icons)
                self.update_done(topic_guid, mindmap_topic, level, done, done_global)

                if mindmap_topic.subtopics and len(mindmap_topic.subtopics) > 0:
                    # Sort subtopics alphabetically by text
                    mindmap_topic.subtopics.sort(key=lambda sub: sub.text)

                for subtopic in mindmap_topic.subtopics:
                    try:
                        if subtopic.guid in done:
                            this_guid_as_parent_exists = self.check_parent_exists(topic_guid, subtopic.guid)
                            if not this_guid_as_parent_exists:
                                cloned_subtopic = self.clone_mindmap_topic(subtopic)
                                sub = self.mindm.add_subtopic_to_topic(topic, cloned_subtopic.text)
                                self.set_topic_from_mindmap_topic(sub, cloned_subtopic, map_icons, done, done_global, level + 1)
                        else:
                            sub = self.mindm.add_subtopic_to_topic(topic, subtopic.text)
                            self.set_topic_from_mindmap_topic(sub, subtopic, map_icons, done, done_global, level + 1)
                    except Exception as e:
                        print(f"Error(2) processing topic/subtopic {mindmap_topic.guid}/{subtopic.guid}: {e}")
            return mindmap_topic
        except Exception as e:
            print(f"Error in set_topic_from_mindmap_topic at level {level} with topic {mindmap_topic.guid}: {e}")

    def check_parent_exists(self, topic_guid, this_guid, visited=None):
        """
        Recursively check if a parent-child relationship exists between topics.

        Args:
            topic_guid (str): The GUID of the topic to check.
            this_guid (str): The GUID that might be a parent of the topic.
            visited (set, optional): Set of visited GUIDs to avoid infinite recursion.

        Returns:
            bool: True if the parent-child relationship exists, False otherwise.
        """
        if visited is None:
            visited = set()
        if topic_guid in visited:
            return False
        visited.add(topic_guid)
        
        check = False
        if topic_guid in self.parents:
            parent_guid = self.parents[topic_guid]
            if parent_guid == this_guid:
                check = True
            else:
                check = self.check_parent_exists(parent_guid, this_guid, visited)
        return check

    def create_mindmap(self, verbose=False):
        """
        Create a MindManager mindmap document from the internal MindmapTopic structure.
        This includes counting occurrences, extracting tags/icons, and setting up relationships and links.

        Args:
            verbose (bool): (Optional) Enable verbose output.
        """
        tags = []
        map_icons = []
        relationships = []
        links = []

        self.parents = {}
        self.guid_counts = {}
        self.count_parent_and_child_occurrences(self.mindmap, self.guid_counts)
        self.get_parents_from_mindmap(self.mindmap, self.parents)

        self.get_tags_from_mindmap(self.mindmap, tags)
        self.get_map_icons_and_fix_refs_from_mindmap(self.mindmap, map_icons)
        self.get_relationships_from_mindmap(self.mindmap, relationships)
        self.get_topic_links_from_mindmap(self.mindmap, links)

        self.mindm.add_document(0)
        self.mindm.create_map_icons(map_icons)
        self.mindm.create_tags(tags, DUPLICATED_TAG)
        self.mindm.set_text_to_topic(self.mindm.get_central_topic(), self.mindmap.text)

        topic = self.mindm.get_central_topic()

        done_global = {}
        self.set_topic_from_mindmap_topic(topic=topic, mindmap_topic=self.mindmap, map_icons=map_icons, done={}, done_global=done_global)

        # Create relationships between topics
        for reference in relationships:
            object1_guids = done_global[reference.guid_1]
            object2_guids = done_global[reference.guid_2]
            for object1_guid in object1_guids:
                for object2_guid in object2_guids:
                    self.mindm.add_relationship(object1_guid, object2_guid, reference.label)

        # Create topic links
        for link in links:
            object1_guids = done_global[link.guid_1]
            object2_guids = done_global[link.guid_2]
            for object1_guid in object1_guids:
                for object2_guid in object2_guids:
                    self.mindm.add_topic_link(object1_guid, object2_guid, link.label)

    def create_mindmap_and_finalize(self):
        """
        Create the mindmap document and finalize it.
        """
        self.create_mindmap()
        self.finalize()

    def finalize(self):
        """
        Finalize the mindmap document by ensuring the maximum topic level is set, then calling MindManager's finalize.
        """
        if self.max_topic_level == 0:
            self.max_topic_level = self.get_max_topic_level(self.mindmap)
        self.mindm.finalize(self.max_topic_level)
    
    def set_background_image(self, image_path):
        """
        Set the background image for the MindManager document.

        Args:
            image_path (str): The file path to the background image.
        """
        self.mindm.set_document_background_image(image_path)
    
    def get_library_folder(self):
        """
        Get the library folder used by MindManager.

        Returns:
            The path to the library folder.
        """
        return self.mindm.get_library_folder()
    
    def get_grounding_information(self):
        """
        Extract grounding information from the mindmap, including the central topic and selected subtopics.

        Returns:
            tuple: (top_most_topic, subtopics) where top_most_topic is the central topic or a concatenated string
                   of non-selected topics, and subtopics is a comma-separated string of selected subtopics.
        """
        central_topic_text = self.mindmap.text
        subtopics = ""
        if len(self.selected_topic_texts) == 0: 
            top_most_topic = central_topic_text
        else:
            if self.central_topic_selected:
                top_most_topic = central_topic_text
                subtopics =  ",".join(self.selected_topic_texts)
            else:
                min_level = min(self.selected_topic_levels)
                max_level = max(self.selected_topic_levels)
                if (min_level == max_level):
                    top_most_topic = central_topic_text
                    subtopics =  ",".join(self.selected_topic_texts)
                else:
                    top_most_topic = ""
                    for i in range(len(self.selected_topic_levels)):
                        if self.selected_topic_levels[i] != max_level:
                            top_most_topic += self.selected_topic_texts[i] + "/"
                        else:
                            subtopics += self.selected_topic_texts[i] + ","

                    if top_most_topic.endswith("/"):
                        top_most_topic = top_most_topic[:-1]
                    if subtopics.endswith(","):
                        subtopics = subtopics[:-1]        
        return top_most_topic, subtopics
