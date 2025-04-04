"""
Windows-specific implementation of the Mindmanager interface.

This module provides Windows platform-specific implementation for interacting
with MindManager application, including functionality for manipulating topics,
properties, relationships, and document structure.
"""

import os
import win32com.client
import winreg
import tempfile

from mindmap.mindmap import MindmapLink, MindmapImage, MindmapNotes, MindmapIcon, MindmapTag, MindmapReference, MindmapTopic

class Mindmanager:

    @staticmethod
    def get_mindmanager_version():
        versions = ["26", "25", "24", "23", "22", "21", "20"]
        for version in versions:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Mindjet\\MindManager\\{version}\\AddIns")
                winreg.CloseKey(key)
                return version
            except FileNotFoundError:
                continue
        return None

    mindmanager_version = get_mindmanager_version()
    if mindmanager_version:
        WINDOWS_LIBRARY_FOLDER = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Mindjet", "MindManager", mindmanager_version, "Library", "ENU")
    else:
        raise Exception("No MindManager version registry keys found.")

    def __init__(self, charttype):
        self._version = Mindmanager.get_mindmanager_version()
        self._mindmanager = win32com.client.Dispatch("Mindmanager.Application")
        self._mindmanager.Options.BalanceNewMainTopics = True
        self._charttype = charttype
        self._library_folder = self.WINDOWS_LIBRARY_FOLDER
        self._document = self._mindmanager.ActiveDocument
    
    def get_mindmanager_object(self):
        return self._mindmanager
        
    def get_active_document_object(self):
        return self._mindmanager.ActiveDocument
        
    def get_library_folder(self):
        return self._library_folder

    def get_version(self):
        return self._version

    def set_document_background_image(self, path):
        try:
            background = self._document.Background
            if background.HasImage:
                background.RemoveImage()
            background.InsertImage(path)
            background.TileOption = 1  # center
            background.Transparency = 88
        except Exception as e:
            print(f"Error setting document background image: {e}")

    def document_exists(self):
        try:
            return True if self._document else False
        except Exception as e:
            print(f"Error checking document existence: {e}")
            return False

    def get_central_topic(self) -> 'MindmapTopic':
        try:
            topic = self._document.CentralTopic
            return self.get_mindmaptopic_from_topic(topic)
        except Exception as e:
            raise Exception(f"Error getting central topic: {e}")
        
    def get_mindmaptopic_from_topic(self, topic) -> 'MindmapTopic':
        mindmap_topic = MindmapTopic()
        mindmap_topic.guid=self.get_guid_from_topic(topic)
        mindmap_topic.text=self.get_text_from_topic(topic)
        mindmap_topic.rtf=self.get_title_from_topic(topic)
        mindmap_topic.level=self.get_level_from_topic(topic)
        return mindmap_topic
    
    def get_mindmaptopic_from_topic_content(self, topic) -> 'MindmapTopic':
        mindmap_topic = self.get_mindmaptopic_from_topic(topic)
        mindmap_topic.notes = self.get_notes_from_topic(topic)
        return mindmap_topic
    
    def get_mindmaptopic_from_topic_full(self, topic) -> 'MindmapTopic':
        mindmap_topic = self.get_mindmaptopic_from_topic(topic)
        mindmap_topic.notes = self.get_notes_from_topic(topic)
        mindmap_topic.links = self.get_links_from_topic(topic)
        mindmap_topic.image = self.get_image_from_topic(topic)
        mindmap_topic.icons = self.get_icons_from_topic(topic)
        mindmap_topic.tags = self.get_tags_from_topic(topic)
        mindmap_topic.references = self.get_references_from_topic(topic)
        return mindmap_topic
    
    def get_topic_by_id(self, id):
        try:
            return self._document.FindByGuid(id)
        except Exception as e:
            print(f"Error in get_topic_by_id: {e}")
            return None

    def get_selection(self):
        selection = []
        try:
            objs = self._document.Selection
            for obj in objs:
                try:
                    class_name = obj._oleobj_.GetTypeInfo().GetDocumentation(-1)[0]
                    if class_name == "ITopic":
                        selection.append(obj)
                except Exception as e:
                    print(f"Error in get_selection, getting class name: {e}")
                    continue
        except Exception as e:
            print(f"Error in get_selection: {e}")
        return selection

    def get_level_from_topic(self, topic):
        try:
            return topic.Level
        except Exception as e:
            print(f"Error in get_level_from_topic: {e}")
            return None

    def get_text_from_topic(self, topic):
        try:
            return topic.Text.replace('"', '`').replace("'", "`").replace("\r", "").replace("\n", "")
        except Exception as e:
            print(f"Error in get_text_from_topic: {e}")
            return ""

    def get_title_from_topic(self, topic):
        try:
            title = topic.Title
            text = title.TextRTF if title.TextRTF != '' else ''
            return text
        except Exception as e:
            print(f"Error in get_title_from_topic: {e}")
            return ""

    def get_subtopics_from_topic(self, topic):
        try:
            return topic.AllSubTopics
        except Exception as e:
            print(f"Error in get_subtopics_from_topic: {e}")
            return None
    
    def get_links_from_topic(self, topic) -> list[MindmapLink]:
        hyperlinks = []
        try:
            if topic.HasHyperlink:
                for hyperlink in topic.Hyperlinks:
                    link = MindmapLink(
                        text=hyperlink.Title,
                        url=hyperlink.Address,
                        guid=hyperlink.TopicLabelGuid
                    )
                    hyperlinks.append(link)
        except Exception as e:
            print(f"Error in get_links_from_topic: {e}")
        return hyperlinks

    def get_image_from_topic(self, topic) -> MindmapImage:
        try:
            if topic.HasImage:
                image = topic.Image
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    temp_filename = tmp.name
                image.Save(temp_filename, 3)  # 3=PNG
                return MindmapImage(text=temp_filename)
        except Exception as e:
            print(f"Error in get_image_from_topic: {e}")
        return None

    def get_icons_from_topic(self, topic) -> list[MindmapIcon]:
        icons = []
        try:
            user_icons = topic.UserIcons
            if user_icons.Count > 0:
                for icon in user_icons:
                    if icon.Type == 1 and icon.IsValid == True:  # Stock Icon
                        icons.append(MindmapIcon(
                            text=icon.Name,
                            index=icon.StockIcon
                        ))
                    elif icon.Type == 2 and icon.IsValid == True:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                            temp_filename = tmp.name
                        icon.Save(temp_filename, 3)  # 3=PNG
                        icons.append(MindmapIcon(
                            text=icon.Name,
                            is_stock_icon=False,
                            signature=icon.CustomIconSignature,
                            path=temp_filename
                        ))
        except Exception as e:
            print(f"Error in get_icons_from_topic: {e}")
        return icons

    def get_notes_from_topic(self, topic) -> MindmapNotes:
        try:
            notes = topic.Notes
            topic_notes = None
            if notes:
                if notes.IsValid == True and not notes.IsEmpty:
                    topic_notes = MindmapNotes()
                    if notes.TextRTF != "":
                        topic_notes.rtf = notes.TextRTF
                    if notes.TextXHTML != "":
                        topic_notes.xhtml = notes.TextXHTML
                    if notes.Text != "":
                        topic_notes.text = notes.Text
            return topic_notes
        except Exception as e:
            print(f"Error in get_notes_from_topic: {e}")
            return None

    def get_tags_from_topic(self, topic) -> list[MindmapTag]:
        tags = []
        try:
            text_labels = topic.TextLabels
            if text_labels.Count > 0 and text_labels.IsValid == True:
                for text_label in text_labels:
                    if text_label.IsValid == True and text_label.GroupId == "":
                        tags.append(MindmapTag(text=text_label.Name))
        except Exception as e:
            print(f"Error in get_tags_from_topic: {e}")
        return tags

    def get_references_from_topic(self, topic) -> list[MindmapReference]:
        references = []
        try:
            relationships = topic.AllRelationships
            if relationships.Count > 0 and relationships.IsValid == True:
                for relation in relationships:
                    if relation.IsValid == True:
                        connected_topic_guid_1 = relation.ConnectedObject1
                        connected_topic_guid_2 = relation.ConnectedObject2
                        reference_direction = 1 if connected_topic_guid_1 == topic else 2
                        references.append(MindmapReference(
                            guid_1=str(connected_topic_guid_1.Guid),
                            guid_2=str(connected_topic_guid_2.Guid),
                            direction=reference_direction,
                            label=''
                        ))
        except Exception as e:
            print(f"Error in get_references_from_topic: {e}")
        return references
    
    def get_guid_from_topic(self, topic) -> str:
        try:
            return topic.Guid
        except Exception as e:
            print(f"Error in get_guid_from_topic: {e}")
            return ""
        
    def add_subtopic_to_topic(self, topic, topic_text):
        try:
            return topic.AddSubtopic(topic_text)
        except Exception as e:
            print(f"Error in add_subtopic_to_topic: {e}")
            return None

    def get_parent_from_topic(self, topic):
        try:
            return topic.ParentTopic
        except Exception as e:
            print(f"Error in get_parent_from_topic: {e}")
            return None

    def set_text_to_topic(self, topic, topic_text):
        try:
            topic.Text = topic_text
        except Exception as e:
            print(f"Error in set_text_to_topic: {e}")

    def set_title_to_topic(self, topic, topic_rtf):
        try:
            if topic_rtf != "":
                topic.Title.TextRTF = topic_rtf
        except Exception as e:
            print(f"Error in set_title_to_topic: {e}")

    def add_tag_to_topic(self, topic=None, tag_text='', topic_guid=None):
        try:
            if topic_guid:
                topic = self.get_topic_by_id(topic_guid)
            if topic:
                topic.TextLabels.AddTextLabelFromGroup(tag_text, '', True)
        except Exception as e:
            print(f"Error in add_tag_to_topic: {e}")

    def set_topic_from_mindmap_topic(self, topic, mindmap_topic, map_icons):
        self.set_text_to_topic(topic, mindmap_topic.text)
        self.set_title_to_topic(topic, mindmap_topic.rtf)
        self.add_tags_to_topic(topic, mindmap_topic.tags)
        self.set_notes_to_topic(topic, mindmap_topic.notes)
        self.add_icons_to_topic(topic, mindmap_topic.icons, map_icons)
        self.add_image_to_topic(topic, mindmap_topic.image)
        self.add_links_to_topic(topic, mindmap_topic.links)
        return topic, topic.Guid
    
    def add_links_to_topic(self, topic, mindmap_topic_links):
        try:
            if mindmap_topic_links:
                for topic_link in mindmap_topic_links:
                    if topic_link.guid == "" and topic_link.url != "":
                        link = topic.Hyperlinks.AddHyperlink(topic_link.url)
                        link.Title = topic_link.text
        except Exception as e:
            print(f"Error in add_links_to_topic: {e}")

    def add_image_to_topic(self, topic, mindmap_topic_image):
        try:
            if mindmap_topic_image:
                topic.CreateImage(mindmap_topic_image.text)
        except Exception as e:
            print(f"Error in add_image_to_topic: {e}")

    def add_icons_to_topic(self, topic, mindmap_topic_icons, map_icons):
        try:
            if len(mindmap_topic_icons) > 0:
                for topic_icon in mindmap_topic_icons:
                    if topic_icon.is_stock_icon:
                        topic.UserIcons.AddStockIcon(topic_icon.index)
                    else:
                        if len(map_icons) > 0 and topic_icon.signature != "":
                            topic.UserIcons.AddCustomIconFromMap(topic_icon.signature)
                        else:
                            if os.path.exists(topic_icon.path):
                                topic.UserIcons.AddCustomIcon(topic_icon.path)
        except Exception as e:
            print(f"Error in add_icons_to_topic: {e}")

    def set_notes_to_topic(self, topic, mindmap_topic_notes):
        try:
            if mindmap_topic_notes:
                if mindmap_topic_notes.text:
                    topic.Notes.Text = mindmap_topic_notes.text
                else:
                    if mindmap_topic_notes.xhtml:
                        try:
                            topic.Notes.TextXHTML = mindmap_topic_notes.xhtml
                        except Exception as e:
                            print(f"Error setting TextXHTML: {e}")
                            print(f"Topic: `{topic.Text}`")
                    else:
                        if mindmap_topic_notes.rtf:
                            topic.Notes.TextRTF = mindmap_topic_notes.rtf
        except Exception as e:
            print(f"Error in set_notes_to_topic: {e}")


    def add_tags_to_topic(self, topic, mindmap_topic_tags):
        try:
            if len(mindmap_topic_tags) > 0:
                for topic_tag in mindmap_topic_tags:
                    topic.TextLabels.AddTextLabelFromGroup(topic_tag.text, '', True)
        except Exception as e:
            print(f"Error in add_tags_to_topic: {e}")

    def create_map_icons(self, map_icons):
        try:
            if len(map_icons) > 0:
                icon_groups = set(map_icon.group for map_icon in map_icons if map_icon.group)
                for icon_group in icon_groups:
                    group = self._document.MapMarkerGroups.AddIconMarkerGroup(icon_group)
                    for map_icon in map_icons:
                        if map_icon.group == icon_group:
                            label = map_icon.text
                            marker = group.AddCustomIconMarker(label, map_icon.path)
                            map_icon.signature = marker.Icon.CustomIconSignature
        except Exception as e:
            print(f"Error in create_map_icons: {e}")

    def create_tags(self, tags: list['str'], DUPLICATED_TAG: str):
        try:
            if len(tags) > 0:
                map_marker_group = self._document.MapMarkerGroups.GetMandatoryMarkerGroup(10)
                for tag in tags:
                    map_marker_group.AddTextLabelMarker(tag)
                if DUPLICATED_TAG != '' and DUPLICATED_TAG not in tags:
                    map_marker_group.AddTextLabelMarker(DUPLICATED_TAG)
        except Exception as e:
            print(f"Error in create_tags: {e}")

    def add_relationship(self, guid1, guid2, label=''):
        try:
            object1 = self.get_topic_by_id(guid1)
            object2 = self.get_topic_by_id(guid2)
            if object1 and object2:
                if object1.ParentTopic == object2 or object2.ParentTopic == object1:
                    return
                object1.AllRelationships.AddToTopic(object2, label)
        except Exception as e:
            print(f"Error in add_relationship: {e}")

    def add_topic_link(self, guid1, guid2, label=''):
        try:
            object1 = self.get_topic_by_id(guid1)
            object2 = self.get_topic_by_id(guid2)
            if object1 and object2:
                hyperlinks = object1.Hyperlinks
                link = hyperlinks.AddHyperlinkToTopicByGuid(guid2)
                link.Title = label if label != "" else object2.Title.Text
        except Exception as e:
            print(f"Error in add_topic_link: {e}")

    def add_document(self, max_topic_level):
        try:
            style = self._document.StyleXml
            new_document = self._mindmanager.Documents.Add()
            new_document.StyleXml = style
            self._document = new_document
        except Exception as e:
            print(f"Error in add_document: {e}")

    def finalize(self, max_topic_level):
        try:
            centralTopic = self._document.CentralTopic
            layout = centralTopic.SubTopicsLayout
            growthDirection = layout.CentralTopicGrowthDirection
            cnt_subtopics = len(centralTopic.AllSubTopics)
                               
            # collapse/uncollapse outer topics
            if max_topic_level > 3:
                for topic in self._document.Range(2, True):  # 2 = all topics
                    if topic.Level > 2:
                        topic.Collapsed = True
                    else:
                        if topic.Level != 0:
                            topic.Collapsed = False
            else:
                for topic in self._document.Range(2, True):  # 2 = all topics
                    if topic.Level > 3:
                        topic.Collapsed = True
                    else:
                        if topic.Level != 0:
                            topic.Collapsed = False
                            
            # org chart            
            if self._charttype == "orgchart" or self._charttype == "auto":
                if max_topic_level > 2 and cnt_subtopics > 4:
                    if growthDirection == 1:
                        layout.CentralTopicGrowthDirection = 5
                        
            # radial map
            if self._charttype == "radial" or self._charttype == "auto":
                if max_topic_level > 2 and cnt_subtopics < 5:
                    if growthDirection != 1:
                        layout.CentralTopicGrowthDirection = 1
                if max_topic_level < 3 and cnt_subtopics > 4:
                    if growthDirection != 1:
                        layout.CentralTopicGrowthDirection = 1

            self._document.Zoom(1)
            self._mindmanager.Visible = True
        except Exception as e:
            print(f"Error in finalize: {e}")