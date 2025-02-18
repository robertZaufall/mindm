import sys

class Mindmanager():

    def __init__(self, charttype):

        if sys.platform.startswith('win'):
            import mindm.mindmanager_win as mm
            platform = "win"
        elif sys.platform.startswith('darwin'):
            import mindm.mindmanager_mac as mm
            platform = "darwin"

        self.mindm = mm.Mindmanager(charttype)

    def merge_windows(self) -> None:
        return self.mindm.merge_windows()

    def set_document_background_image(self, path: str) -> None:
        return self.mindm.set_document_background_image(path)

    def document_exists(self) -> bool:
        return self.mindm.document_exists()

    def get_central_topic(self) -> any:
        return self.mindm.get_central_topic()

    def get_topic_by_id(self, id: any) -> any:
        return self.mindm.get_topic_by_id(id)

    def get_selection(self) -> list:
        return self.mindm.get_selection()

    def get_level_from_topic(self, topic: any) -> any:
        return self.mindm.get_level_from_topic(topic)

    def get_text_from_topic(self, topic: any) -> str:
        return self.mindm.get_text_from_topic(topic)

    def get_title_from_topic(self, topic: any) -> str:
        return self.mindm.get_title_from_topic(topic)

    def get_subtopics_from_topic(self, topic: any) -> list:
        return self.mindm.get_subtopics_from_topic(topic)

    def get_links_from_topic(self, topic: any) -> list:
        return self.mindm.get_links_from_topic(topic)

    def get_image_from_topic(self, topic: any) -> any:
        return self.mindm.get_image_from_topic(topic)

    def get_icons_from_topic(self, topic: any) -> list:
        return self.mindm.get_icons_from_topic(topic)

    def get_notes_from_topic(self, topic: any) -> any:
        return self.mindm.get_notes_from_topic(topic)

    def get_tags_from_topic(self, topic: any) -> list:
        return self.mindm.get_tags_from_topic(topic)

    def get_references_from_topic(self, topic: any) -> list:
        return self.mindm.get_references_from_topic(topic)

    def get_guid_from_topic(self, topic: any) -> str:
        return self.mindm.get_guid_from_topic(topic)

    def add_subtopic_to_topic(self, topic: any, topic_text: str) -> any:
        return self.mindm.add_subtopic_to_topic(topic, topic_text)

    def get_parent_from_topic(self, topic: any) -> any:
        return self.mindm.get_parent_from_topic(topic)

    def set_text_to_topic(self, topic: any, topic_text: str) -> None:
        return self.mindm.set_text_to_topic(topic, topic_text)

    def set_title_to_topic(self, topic: any, topic_rtf: str) -> None:
        return self.mindm.set_title_to_topic(topic, topic_rtf)

    def add_tag_to_topic(self, topic: any, tag_text: str) -> None:
        return self.mindm.add_tag_to_topic(topic, tag_text)

    def set_topic_from_mindmap_topic(self, topic: any, mindmap_topic: any, map_icons: any) -> any:
        return self.mindm.set_topic_from_mindmap_topic(topic, mindmap_topic, map_icons)

    def create_map_icons(self, map_icons: any) -> None:
        return self.mindm.create_map_icons(map_icons)

    def create_tags(self, tags: list[str], DUPLICATED_TAG: str) -> None:
        return self.mindm.create_tags(tags, DUPLICATED_TAG)

    def add_relationship(self, guid1: any, guid2: any, label: str = '') -> None:
        return self.mindm.add_relationship(guid1, guid2, label)

    def add_topic_link(self, guid1: any, guid2: any, label: str = '') -> None:
        return self.mindm.add_topic_link(guid1, guid2, label)

    def add_document(self, max_topic_level: int) -> None:
        return self.mindm.add_document(max_topic_level)

    def finalize(self, max_topic_level: int) -> None:
        return self.mindm.finalize(max_topic_level)