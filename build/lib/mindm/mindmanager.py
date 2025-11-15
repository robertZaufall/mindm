"""
Platform-independent interface for MindManager operations.

This module provides a unified interface for working with MindManager
across different platforms (Windows and MacOS) by delegating to the
appropriate platform-specific implementation.
"""

import sys

class Mindmanager():
    def __init__(self, charttype='auto', macos_access='appscript'):
        """
        Initialize a Mindmanager instance and delegate to the platform-specific implementation.

        Args:
            charttype (any): The type of chart to initialize with.
            macos_access (str): Method for accessing macOS features (default is 'appscript', alternative is 'applescript').
        """
        if sys.platform.startswith('win'):
            import mindm.mindmanager_win as mm
            self.platform = "win"
        elif sys.platform.startswith('darwin'):
            if macos_access == 'applescript':
                import mindm.mindmanager_mac_as as mm # AppleScript
            else:
                import mindm.mindmanager_mac as mm # Appscript
            self.platform = "darwin"

        self.mindm = mm.Mindmanager(charttype)

    def get_mindmanager_object(self) -> any:
        """
        Retrieve the MindManager application object.

        Returns:
            any: The MindManager application object.
        """
        return self.mindm.get_mindmanager_object()
    
    def get_active_document_object(self) -> any:
        """
        Retrieve the active document object.

        Returns:
            any: The active document object.
        """
        return self.mindm.get_active_document_object()
    
    def get_version(self) -> str:
        """
        Retrieve the version of the MindManager application.

        Returns:
            str: The version of the application.
        """
        return self.mindm.get_version()

    def get_library_folder(self) -> str:
        """
        Retrieve the library folder path for the MindManager application.

        Returns:
            str: The library folder path.
        """
        return self.mindm.get_library_folder()

    def set_document_background_image(self, path: str) -> None:
        """
        Set the background image for the document.

        Args:
            path (str): The path to the background image.

        Returns:
            None
        """
        return self.mindm.set_document_background_image(path)

    def document_exists(self) -> bool:
        """
        Check if a document exists in the current context.

        Returns:
            bool: True if the document exists, False otherwise.
        """
        return self.mindm.document_exists()

    def get_central_topic(self) -> any:
        """
        Retrieve the central topic of the mind map.

        Returns:
            any: The central topic.
        """
        return self.mindm.get_central_topic()

    def get_mindmaptopic_from_topic(self, topic) -> any:
        """
        Retrieve the topic properties of the topic.

        Returns:
            any: A mindmap topic
        """
        return self.mindm.get_mindmaptopic_from_topic(topic)

    def get_mindmaptopic_from_topic_content(self, topic) -> any:
        """
        Retrieve the topic properties of the topic including notes.

        Returns:
            any: A mindmap topic
        """
        return self.mindm.get_mindmaptopic_from_topic_content(topic)

    def get_mindmaptopic_from_topic_full(self, topic) -> any:
        """
        Retrieve the full set of topic properties of the topic.

        Returns:
            any: The mindmap topic.
        """
        return self.mindm.get_mindmaptopic_from_topic_full(topic)

    def get_topic_by_id(self, id: any) -> any:
        """
        Retrieve a topic by its identifier.

        Args:
            id (any): The identifier of the topic.

        Returns:
            any: The topic corresponding to the given id.
        """
        return self.mindm.get_topic_by_id(id)

    def get_selection(self) -> list:
        """
        Get the currently selected topics.

        Returns:
            list: A list of selected topics.
        """
        return self.mindm.get_selection()

    def get_level_from_topic(self, topic: any) -> any:
        """
        Get the level of the given topic within the mind map hierarchy.

        Args:
            topic (any): The topic to evaluate.

        Returns:
            any: The level of the topic.
        """
        return self.mindm.get_level_from_topic(topic)

    def get_text_from_topic(self, topic: any) -> str:
        """
        Retrieve the text content of a topic.

        Args:
            topic (any): The topic to extract text from.

        Returns:
            str: The text content of the topic.
        """
        return self.mindm.get_text_from_topic(topic)

    def get_title_from_topic(self, topic: any) -> str:
        """
        Retrieve the title of a topic.

        Args:
            topic (any): The topic to extract the title from.

        Returns:
            str: The title of the topic.
        """
        return self.mindm.get_title_from_topic(topic)

    def get_subtopics_from_topic(self, topic: any) -> list:
        """
        Retrieve all subtopics for the specified topic.

        Args:
            topic (any): The parent topic.

        Returns:
            list: A list of subtopics.
        """
        return self.mindm.get_subtopics_from_topic(topic)

    def get_links_from_topic(self, topic: any) -> list:
        """
        Retrieve all links associated with the specified topic.

        Args:
            topic (any): The topic to extract links from.

        Returns:
            list: A list of links.
        """
        return self.mindm.get_links_from_topic(topic)

    def get_image_from_topic(self, topic: any) -> any:
        """
        Retrieve the image associated with the topic.

        Args:
            topic (any): The topic to extract the image from.

        Returns:
            any: The image object or path.
        """
        return self.mindm.get_image_from_topic(topic)

    def get_icons_from_topic(self, topic: any) -> list:
        """
        Retrieve all icons associated with the topic.

        Args:
            topic (any): The topic to extract icons from.

        Returns:
            list: A list of icons.
        """
        return self.mindm.get_icons_from_topic(topic)

    def get_notes_from_topic(self, topic: any) -> any:
        """
        Retrieve the notes for the specified topic.

        Args:
            topic (any): The topic to extract notes from.

        Returns:
            any: The notes of the topic.
        """
        return self.mindm.get_notes_from_topic(topic)

    def get_tags_from_topic(self, topic: any) -> list:
        """
        Retrieve all tags attached to the topic.

        Args:
            topic (any): The topic to extract tags from.

        Returns:
            list: A list of tags.
        """
        return self.mindm.get_tags_from_topic(topic)

    def get_references_from_topic(self, topic: any) -> list:
        """
        Retrieve all references associated with the topic.

        Args:
            topic (any): The topic to extract references from.

        Returns:
            list: A list of references.
        """
        return self.mindm.get_references_from_topic(topic)

    def get_guid_from_topic(self, topic: any) -> str:
        """
        Retrieve the GUID (Globally Unique Identifier) of the topic.

        Args:
            topic (any): The topic to extract the GUID from.

        Returns:
            str: The GUID of the topic.
        """
        return self.mindm.get_guid_from_topic(topic)

    def add_subtopic_to_topic(self, topic: any, topic_text: str) -> any:
        """
        Add a subtopic with the provided text to an existing topic.

        Args:
            topic (any): The parent topic.
            topic_text (str): The text for the new subtopic.

        Returns:
            any: The newly created subtopic.
        """
        return self.mindm.add_subtopic_to_topic(topic, topic_text)

    def get_parent_from_topic(self, topic: any) -> any:
        """
        Retrieve the parent topic of the given topic.

        Args:
            topic (any): The topic to find the parent for.

        Returns:
            any: The parent topic.
        """
        return self.mindm.get_parent_from_topic(topic)

    def set_text_to_topic(self, topic: any, topic_text: str) -> None:
        """
        Set the text content for the specified topic.

        Args:
            topic (any): The topic to update.
            topic_text (str): The new text content.

        Returns:
            None
        """
        return self.mindm.set_text_to_topic(topic, topic_text)

    def set_title_to_topic(self, topic: any, topic_rtf: str) -> None:
        """
        Set the title (as RTF) for the specified topic.

        Args:
            topic (any): The topic to update.
            topic_rtf (str): The new title in RTF format.

        Returns:
            None
        """
        return self.mindm.set_title_to_topic(topic, topic_rtf)

    def add_tag_to_topic(self, topic: any, tag_text: str, topic_guid: str) -> None:
        """
        Add a tag to the specified topic.

        Args:
            topic (any): The topic to update.
            tag_text (str): The tag text to add.

        Returns:
            None
        """
        return self.mindm.add_tag_to_topic(topic, tag_text, topic_guid)

    def set_topic_from_mindmap_topic(self, topic: any, mindmap_topic: any, map_icons: any) -> any:
        """
        Update or create a topic based on the provided mindmap topic and icons.

        Args:
            topic (any): The current topic to update.
            mindmap_topic (any): The reference mindmap topic data.
            map_icons (any): Icons mapping for the topic.

        Returns:
            any: The updated topic.
        """
        return self.mindm.set_topic_from_mindmap_topic(topic, mindmap_topic, map_icons)

    def create_map_icons(self, map_icons: any) -> None:
        """
        Create map icons based on the provided mapping.

        Args:
            map_icons (any): The icons mapping.

        Returns:
            None
        """
        return self.mindm.create_map_icons(map_icons)

    def create_tags(self, tags: list[str], DUPLICATED_TAG: str) -> None:
        """
        Create tags for the mind map.

        Args:
            tags (list[str]): A list of tag names to create.
            DUPLICATED_TAG (str): The tag used in case of duplication.

        Returns:
            None
        """
        return self.mindm.create_tags(tags, DUPLICATED_TAG)

    def add_relationship(self, guid1: any, guid2: any, label: str = '') -> None:
        """
        Add a relationship between two topics.

        Args:
            guid1 (any): The GUID of the first topic.
            guid2 (any): The GUID of the second topic.
            label (str, optional): Optional label for the relationship. Defaults to ''.

        Returns:
            None
        """
        return self.mindm.add_relationship(guid1, guid2, label)

    def add_topic_link(self, guid1: any, guid2: any, label: str = '') -> None:
        """
        Create a link between two topics.

        Args:
            guid1 (any): The GUID of the source topic.
            guid2 (any): The GUID of the target topic.
            label (str, optional): Optional label for the link. Defaults to ''.

        Returns:
            None
        """
        return self.mindm.add_topic_link(guid1, guid2, label)

    def add_document(self, max_topic_level: int) -> None:
        """
        Add a new mind map document with a specified maximum topic level.

        Args:
            max_topic_level (int): The maximum depth of topics in the document.

        Returns:
            None
        """
        return self.mindm.add_document(max_topic_level)

    def finalize(self, max_topic_level: int) -> None:
        """
        Finalize and process the mind map document.

        Args:
            max_topic_level (int): The maximum depth of topics processed.

        Returns:
            None
        """
        return self.mindm.finalize(max_topic_level)