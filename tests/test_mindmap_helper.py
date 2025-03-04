import unittest
from unittest.mock import MagicMock, patch
import uuid

import mindmap.mindmap as mh


class TestMindmapClasses(unittest.TestCase):
    """Test the helper classes for mindmap data structures."""
    
    def test_mindmap_link_init(self):
        """Test MindmapLink initialization."""
        link = mh.MindmapLink(text="Test Link", url="https://example.com", guid="12345")
        self.assertEqual(link.text, "Test Link")
        self.assertEqual(link.url, "https://example.com")
        self.assertEqual(link.guid, "12345")
        
        # Test default values
        default_link = mh.MindmapLink()
        self.assertEqual(default_link.text, "")
        self.assertEqual(default_link.url, "")
        self.assertEqual(default_link.guid, "")

    def test_mindmap_image_init(self):
        """Test MindmapImage initialization."""
        image = mh.MindmapImage(text="path/to/image.png")
        self.assertEqual(image.text, "path/to/image.png")
        
        # Test default values
        default_image = mh.MindmapImage()
        self.assertEqual(default_image.text, "")

    def test_mindmap_notes_init(self):
        """Test MindmapNotes initialization."""
        notes = mh.MindmapNotes(text="Plain text", xhtml="<p>HTML</p>", rtf="{\\rtf1}")
        self.assertEqual(notes.text, "Plain text")
        self.assertEqual(notes.xhtml, "<p>HTML</p>")
        self.assertEqual(notes.rtf, "{\\rtf1}")
        
        # Test default values
        default_notes = mh.MindmapNotes()
        self.assertEqual(default_notes.text, "")
        self.assertEqual(default_notes.xhtml, "")
        self.assertEqual(default_notes.rtf, "")

    def test_mindmap_icon_init(self):
        """Test MindmapIcon initialization."""
        icon = mh.MindmapIcon(
            text="Icon Name", 
            is_stock_icon=False, 
            index=5, 
            signature="abc123", 
            path="icons/custom.png",
            group="Types"
        )
        self.assertEqual(icon.text, "Icon Name")
        self.assertEqual(icon.is_stock_icon, False)
        self.assertEqual(icon.index, 5)
        self.assertEqual(icon.signature, "abc123")
        self.assertEqual(icon.path, "icons/custom.png")
        self.assertEqual(icon.group, "Types")
        
        # Test default values
        default_icon = mh.MindmapIcon()
        self.assertEqual(default_icon.text, "")
        self.assertTrue(default_icon.is_stock_icon)
        self.assertEqual(default_icon.index, 1)
        self.assertEqual(default_icon.signature, "")
        self.assertEqual(default_icon.path, "")
        self.assertEqual(default_icon.group, "")

    def test_mindmap_tag_init(self):
        """Test MindmapTag initialization."""
        tag = mh.MindmapTag(text="Important")
        self.assertEqual(tag.text, "Important")
        
        # Test default values
        default_tag = mh.MindmapTag()
        self.assertEqual(default_tag.text, "")

    def test_mindmap_reference_init(self):
        """Test MindmapReference initialization."""
        ref = mh.MindmapReference(
            guid_1="topic1", 
            guid_2="topic2", 
            direction=2, 
            label="Relates to"
        )
        self.assertEqual(ref.guid_1, "topic1")
        self.assertEqual(ref.guid_2, "topic2")
        self.assertEqual(ref.direction, 2)
        self.assertEqual(ref.label, "Relates to")
        
        # Test default values
        default_ref = mh.MindmapReference()
        self.assertEqual(default_ref.guid_1, "")
        self.assertEqual(default_ref.guid_2, "")
        self.assertEqual(default_ref.direction, 1)
        self.assertEqual(default_ref.label, "")

    def test_mindmap_topic_init(self):
        """Test MindmapTopic initialization."""
        # Create child and parent topics
        parent = mh.MindmapTopic(guid="parent", text="Parent Topic", level=0)
        child = mh.MindmapTopic(
            guid="child",
            text="Child Topic",
            rtf="{\\rtf Child}",
            level=1,
            selected=True,
            parent=parent
        )
        
        self.assertEqual(child.guid, "child")
        self.assertEqual(child.text, "Child Topic")
        self.assertEqual(child.rtf, "{\\rtf Child}")
        self.assertEqual(child.level, 1)
        self.assertTrue(child.selected)
        self.assertEqual(child.parent, parent)
        self.assertEqual(len(child.subtopics), 0)
        
        # Test default values
        default_topic = mh.MindmapTopic()
        self.assertEqual(default_topic.guid, "")
        self.assertEqual(default_topic.text, "")
        self.assertEqual(default_topic.level, 0)
        self.assertFalse(default_topic.selected)
        self.assertIsNone(default_topic.parent)
        
        # Test lists initialization
        self.assertEqual(len(default_topic.links), 0)
        self.assertEqual(len(default_topic.icons), 0)
        self.assertEqual(len(default_topic.tags), 0)
        self.assertEqual(len(default_topic.references), 0)
        
        # Test special character handling in text
        special_chars_topic = mh.MindmapTopic(text="Text with 'quotes' and \"double quotes\" and \nnewlines")
        self.assertEqual(special_chars_topic.text, "Text with `quotes` and `double quotes` and newlines")


class TestMindmapDocument(unittest.TestCase):
    """Test the MindmapDocument class."""
    
    @patch('mindmap.mindmap.mm.Mindmanager')
    def setUp(self, mock_mindmanager):
        """Set up test fixtures."""
        self.mock_mindmanager = mock_mindmanager
        self.document = mh.MindmapDocument()
        self.mock_mindm = self.document.mindm
        
        # Create a mock central topic
        self.central_topic = MagicMock()
        self.mock_mindm.get_central_topic.return_value = self.central_topic
        self.mock_mindm.document_exists.return_value = True
        
        # Mock the properties of the central topic
        self.mock_mindm.get_guid_from_topic.return_value = "central_guid"
        self.mock_mindm.get_text_from_topic.return_value = "Central Topic"
        self.mock_mindm.get_title_from_topic.return_value = "{\\rtf Central Topic}"
        self.mock_mindm.get_level_from_topic.return_value = 0
        self.mock_mindm.get_links_from_topic.return_value = []
        self.mock_mindm.get_image_from_topic.return_value = None
        self.mock_mindm.get_icons_from_topic.return_value = []
        self.mock_mindm.get_notes_from_topic.return_value = None
        self.mock_mindm.get_tags_from_topic.return_value = []
        self.mock_mindm.get_references_from_topic.return_value = []
        
        # Mock empty subtopics initially
        self.mock_mindm.get_subtopics_from_topic.return_value = []
        
    def test_init(self):
        """Test MindmapDocument initialization."""
        doc = mh.MindmapDocument(charttype="radial", turbo_mode=True, inline_editing_mode=True, mermaid_mode=False)
        self.assertEqual(doc.charttype, "radial")
        self.assertTrue(doc.turbo_mode)
        self.assertTrue(doc.inline_editing_mode)
        self.assertFalse(doc.mermaid_mode)
        self.assertIsNone(doc.mindmap)
        
        # Create a new mock and test with it to avoid conflicts with setUp
        with patch('mindmap.mindmap.mm.Mindmanager') as new_mock:
            test_doc = mh.MindmapDocument(charttype="radial")
            new_mock.assert_called_once_with("radial")
        
    def test_get_mindmap_no_document(self):
        """Test get_mindmap when no document exists."""
        self.mock_mindm.document_exists.return_value = False
        result = self.document.get_mindmap()
        self.assertFalse(result)
        self.assertIsNone(self.document.mindmap)
        
    def test_get_mindmap_empty(self):
        """Test get_mindmap with a document containing only a central topic."""
        result = self.document.get_mindmap()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.document.mindmap)
        self.assertEqual(self.document.mindmap.guid, "central_guid")
        self.assertEqual(self.document.mindmap.text, "Central Topic")
        self.assertEqual(self.document.mindmap.level, 0)
        self.assertEqual(len(self.document.mindmap.subtopics), 0)
        
    def test_get_mindmap_with_subtopics(self):
        """Test get_mindmap with a document containing subtopics."""
        # Mock a subtopic
        subtopic = MagicMock()
        self.mock_mindm.get_subtopics_from_topic.return_value = [subtopic]
        
        # Ensure text value is not None for all topics
        self.mock_mindm.get_text_from_topic.return_value = "Central Topic"
        
        # Mock the subtopic properties
        subtopic_values = {
            "guid": "subtopic_guid",
            "text": "Subtopic",
            "title": "{\\rtf Subtopic}",
            "level": 1
        }
        
        def get_property_from_topic(topic, prop_name=None):
            if topic == subtopic:
                if prop_name == "guid":
                    return subtopic_values["guid"]
                elif prop_name == "text":
                    return subtopic_values["text"]
                elif prop_name == "title":
                    return subtopic_values["title"]
                elif prop_name == "level":
                    return subtopic_values["level"]
            elif topic == self.central_topic:
                if prop_name == "guid":
                    return "central_guid"
                elif prop_name == "text":
                    return "Central Topic"
                elif prop_name == "title":
                    return "{\\rtf Central Topic}"
                elif prop_name == "level":
                    return 0
            return ""  # Return empty string instead of None for safety
        
        # Set up the mock to handle different parameters
        self.mock_mindm.get_guid_from_topic.side_effect = lambda topic: get_property_from_topic(topic, "guid")
        self.mock_mindm.get_text_from_topic.side_effect = lambda topic: get_property_from_topic(topic, "text")
        self.mock_mindm.get_title_from_topic.side_effect = lambda topic: get_property_from_topic(topic, "title")
        self.mock_mindm.get_level_from_topic.side_effect = lambda topic: get_property_from_topic(topic, "level")
        
        # Mock additional methods to return empty lists/None
        self.mock_mindm.get_links_from_topic.return_value = []
        self.mock_mindm.get_image_from_topic.return_value = None
        self.mock_mindm.get_icons_from_topic.return_value = []
        self.mock_mindm.get_notes_from_topic.return_value = None
        self.mock_mindm.get_tags_from_topic.return_value = []
        self.mock_mindm.get_references_from_topic.return_value = []
        
        # Mock empty subtopics for the subtopic
        self.mock_mindm.get_subtopics_from_topic.side_effect = lambda topic: [] if topic == subtopic else [subtopic]
        
        # Execute the method
        result = self.document.get_mindmap()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.document.mindmap)
        self.assertEqual(self.document.mindmap.guid, "central_guid")
        self.assertEqual(len(self.document.mindmap.subtopics), 1)
        
        # Check the subtopic
        subtopic_obj = self.document.mindmap.subtopics[0]
        self.assertEqual(subtopic_obj.guid, "subtopic_guid")
        self.assertEqual(subtopic_obj.text, "Subtopic")
        self.assertEqual(subtopic_obj.level, 1)
        
    def test_get_max_topic_level(self):
        """Test get_max_topic_level method."""
        # Create a mindmap with different levels
        central = mh.MindmapTopic(guid="central", text="Central", level=0)
        subtopic1 = mh.MindmapTopic(guid="sub1", text="Sub1", level=1, parent=central)
        subtopic2 = mh.MindmapTopic(guid="sub2", text="Sub2", level=2, parent=subtopic1)
        subtopic3 = mh.MindmapTopic(guid="sub3", text="Sub3", level=3, parent=subtopic2)
        
        central.subtopics = [subtopic1]
        subtopic1.subtopics = [subtopic2]
        subtopic2.subtopics = [subtopic3]
        
        max_level = self.document.get_max_topic_level(central)
        self.assertEqual(max_level, 3)
        
        # Test with circular references (shouldn't get stuck in infinite recursion)
        circular1 = mh.MindmapTopic(guid="circ1", text="Circ1", level=1)
        circular2 = mh.MindmapTopic(guid="circ2", text="Circ2", level=2)
        circular1.subtopics = [circular2]
        circular2.subtopics = [circular1]  # Create circular reference
        
        max_level = self.document.get_max_topic_level(circular1)
        self.assertEqual(max_level, 2)
        
    def test_clone_mindmap_topic(self):
        """Test clone_mindmap_topic method."""
        # Create source topic with subtopics
        source = mh.MindmapTopic(
            guid="source",
            text="Source",
            rtf="{\\rtf Source}",
            level=1,
            links=[mh.MindmapLink(text="Link", url="https://example.com", guid="link_guid")],
            icons=[mh.MindmapIcon(text="Icon", index=2, group="Group")],
            notes=mh.MindmapNotes(text="Notes text")
        )
        
        subtopic = mh.MindmapTopic(guid="subtopic", text="Subtopic", level=2)
        source.subtopics = [subtopic]
        
        # Clone the topic with explicit subtopics parameter
        cloned = self.document.clone_mindmap_topic(source, subtopics=source.subtopics)
        
        # Verify clone has same properties but is a different object
        self.assertEqual(cloned.guid, source.guid)
        self.assertEqual(cloned.text, source.text)
        self.assertEqual(cloned.rtf, source.rtf)
        self.assertEqual(cloned.level, source.level)
        
        # Check that subtopics were cloned
        self.assertEqual(len(cloned.subtopics), 1)
        self.assertEqual(cloned.subtopics[0].guid, "subtopic")
        self.assertEqual(cloned.subtopics[0].text, "Subtopic")
        
        # Check that links were copied
        self.assertEqual(len(cloned.links), 1)
        self.assertEqual(cloned.links[0].text, "Link")
        self.assertEqual(cloned.links[0].url, "https://example.com")
        
        # Check that icons were copied
        self.assertEqual(len(cloned.icons), 1)
        self.assertEqual(cloned.icons[0].text, "Icon")
        self.assertEqual(cloned.icons[0].index, 2)
        
        # Check that notes were copied
        self.assertIsNotNone(cloned.notes)
        self.assertEqual(cloned.notes.text, "Notes text")
        
    def test_count_parent_and_child_occurrences(self):
        """Test count_parent_and_child_occurrences method."""
        # Create a mindmap with parent-child relationships
        central = mh.MindmapTopic(guid="central", text="Central", level=0)
        child1 = mh.MindmapTopic(guid="child1", text="Child1", level=1)
        child2 = mh.MindmapTopic(guid="child2", text="Child2", level=1)
        grandchild = mh.MindmapTopic(guid="grandchild", text="Grandchild", level=2)
        
        central.subtopics = [child1, child2]
        child1.subtopics = [grandchild]
        
        guid_counts = {}
        self.document.count_parent_and_child_occurrences(central, guid_counts)
        
        # Check parent counts
        self.assertEqual(guid_counts["central"]["parent"], 2)  # Has 2 children
        self.assertEqual(guid_counts["child1"]["parent"], 1)   # Has 1 child
        self.assertEqual(guid_counts["child2"]["parent"], 0)   # Has no children
        self.assertEqual(guid_counts["grandchild"]["parent"], 0)  # Has no children
        
        # Check child counts
        self.assertEqual(guid_counts["central"]["child"], 0)   # Has no parent
        self.assertEqual(guid_counts["child1"]["child"], 1)    # Has 1 parent
        self.assertEqual(guid_counts["child2"]["child"], 1)    # Has 1 parent
        self.assertEqual(guid_counts["grandchild"]["child"], 1)  # Has 1 parent
        
        # Test with missing guid (should generate a UUID)
        topic_no_guid = mh.MindmapTopic(text="No GUID", level=1)
        guid_counts = {}
        self.document.count_parent_and_child_occurrences(topic_no_guid, guid_counts)
        
        # Should have created a UUID and added it to the counts
        self.assertEqual(len(guid_counts), 1)
        self.assertIn("parent", list(guid_counts.values())[0])
        self.assertIn("child", list(guid_counts.values())[0])

    def test_get_topic_texts_from_selection(self):
        """Test get_topic_texts_from_selection method."""
        # Create selected topics
        central = mh.MindmapTopic(guid="central", text="Central", level=0, selected=True)
        topic1 = mh.MindmapTopic(guid="topic1", text="Topic 1", level=1, selected=True)
        topic2 = mh.MindmapTopic(guid="topic2", text="Topic 2", level=2, selected=True)
        topic3 = mh.MindmapTopic(guid="topic3", text="Topic 3", level=2, selected=False)  # Not selected
        
        selection = [central, topic1, topic2, topic3]
        
        texts, levels, ids, central_selected = self.document.get_topic_texts_from_selection(selection)
        
        # Check results
        self.assertEqual(texts, ["Topic 1", "Topic 2"])  # Central topic not included in texts
        self.assertEqual(levels, [1, 2])
        self.assertEqual(ids, ["topic1", "topic2"])
        self.assertTrue(central_selected)


if __name__ == '__main__':
    unittest.main()