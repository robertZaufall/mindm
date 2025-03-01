import unittest
from unittest.mock import MagicMock, patch

import mindm.mindmap_helper as mh


class TestMindmapRelationships(unittest.TestCase):
    """Test relationship handling in MindmapDocument class."""
    
    @patch('mindm.mindmap_helper.mm.Mindmanager')
    def setUp(self, mock_mindmanager):
        """Set up test fixtures."""
        self.mock_mindmanager = mock_mindmanager
        self.document = mh.MindmapDocument()
        self.mock_mindm = self.document.mindm
        
        # Create a test mindmap with relationships and tags
        self.central = mh.MindmapTopic(guid="central", text="Central Topic", level=0)
        self.topic1 = mh.MindmapTopic(guid="topic1", text="Topic 1", level=1)
        self.topic2 = mh.MindmapTopic(guid="topic2", text="Topic 2", level=1)
        
        # Add subtopics to central
        self.central.subtopics = [self.topic1, self.topic2]
        
        # Add references (relationships) between topics
        self.reference = mh.MindmapReference(
            guid_1="topic1", 
            guid_2="topic2", 
            direction=1, 
            label="Relates to"
        )
        self.topic1.references = [self.reference]
        
        # Add tags to topics
        self.tag1 = mh.MindmapTag(text="Important")
        self.tag2 = mh.MindmapTag(text="Urgent")
        self.topic1.tags = [self.tag1]
        self.topic2.tags = [self.tag2]
        
        # Add a topic link
        self.link = mh.MindmapLink(text="Link to topic2", url="", guid="topic2")
        self.topic1.links = [self.link]
        
        # Mock the mindmap property
        self.document.mindmap = self.central
        
    def test_get_relationships_from_mindmap(self):
        """Test extracting relationships from the mindmap."""
        relationships = []
        self.document.get_relationships_from_mindmap(self.central, relationships)
        
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0].guid_1, "topic1")
        self.assertEqual(relationships[0].guid_2, "topic2")
        self.assertEqual(relationships[0].label, "Relates to")
        
        # Test with circular references
        # Create circular reference
        circular_ref = mh.MindmapReference(
            guid_1="topic2", 
            guid_2="topic1", 
            direction=1, 
            label="Circular"
        )
        self.topic2.references = [circular_ref]
        
        relationships = []
        self.document.get_relationships_from_mindmap(self.central, relationships)
        
        self.assertEqual(len(relationships), 2)
        
    def test_get_topic_links_from_mindmap(self):
        """Test extracting topic links from the mindmap."""
        links = []
        self.document.get_topic_links_from_mindmap(self.central, links)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].guid_1, "topic1")
        self.assertEqual(links[0].guid_2, "topic2")
        self.assertEqual(links[0].label, "Link to topic2")
        
        # Test with empty guid (should be ignored)
        empty_link = mh.MindmapLink(text="Empty link", url="", guid="")
        self.topic2.links = [empty_link]
        
        links = []
        self.document.get_topic_links_from_mindmap(self.central, links)
        
        self.assertEqual(len(links), 1)  # Should still be only one link
        
    def test_get_tags_from_mindmap(self):
        """Test collecting unique tags from the mindmap."""
        tags = []
        self.document.get_tags_from_mindmap(self.central, tags)
        
        self.assertEqual(len(tags), 2)
        self.assertIn("Important", tags)
        self.assertIn("Urgent", tags)
        
        # Test with duplicate tags
        duplicate_tag = mh.MindmapTag(text="Important")  # Same as tag1
        self.topic2.tags.append(duplicate_tag)
        
        tags = []
        self.document.get_tags_from_mindmap(self.central, tags)
        
        self.assertEqual(len(tags), 2)  # Should still be 2 unique tags
        
        # Test with empty tag (should be ignored)
        empty_tag = mh.MindmapTag(text="")
        self.topic1.tags.append(empty_tag)
        
        tags = []
        self.document.get_tags_from_mindmap(self.central, tags)
        
        self.assertEqual(len(tags), 2)  # Empty tag should be ignored
        
    def test_get_parents_from_mindmap(self):
        """Test building parent-child GUID mappings."""
        parents = {}
        self.document.get_parents_from_mindmap(self.central, parents)
        
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents["topic1"], "central")
        self.assertEqual(parents["topic2"], "central")
        
        # Add a subtopic to topic1
        subtopic = mh.MindmapTopic(guid="subtopic", text="Subtopic", level=2)
        self.topic1.subtopics = [subtopic]
        
        parents = {}
        self.document.get_parents_from_mindmap(self.central, parents)
        
        self.assertEqual(len(parents), 3)
        self.assertEqual(parents["subtopic"], "topic1")
        
        # Test with circular references
        circular_parent = mh.MindmapTopic(guid="circular", text="Circular", level=2)
        circular_child = mh.MindmapTopic(guid="circular_child", text="Child", level=3)
        circular_parent.subtopics = [circular_child]
        circular_child.subtopics = [circular_parent]  # Create circular reference
        self.topic2.subtopics = [circular_parent]
        
        parents = {}
        self.document.get_parents_from_mindmap(self.central, parents)
        
        self.assertEqual(parents["circular"], "topic2")
        self.assertEqual(parents["circular_child"], "circular")
        # The circular reference shouldn't appear again
        
    def test_check_parent_exists(self):
        """Test checking if a parent-child relationship exists."""
        # Set up parent dictionary
        self.document.parents = {
            "topic1": "central",
            "topic2": "central",
            "subtopic": "topic1",
            "subsubtopic": "subtopic"
        }
        
        # Direct parent relationship
        self.assertTrue(self.document.check_parent_exists("topic1", "central"))
        
        # Ancestor relationship
        self.assertTrue(self.document.check_parent_exists("subsubtopic", "central"))
        
        # No relationship
        self.assertFalse(self.document.check_parent_exists("topic2", "topic1"))
        
        # Self-parent (should be false)
        self.assertFalse(self.document.check_parent_exists("central", "central"))
        
        # Topic not in parents dictionary
        self.assertFalse(self.document.check_parent_exists("nonexistent", "central"))
        
    def test_get_map_icons_and_fix_refs_from_mindmap(self):
        """Test extracting icons from mindmap topics."""
        # Set up icons in topics
        icon1 = mh.MindmapIcon(
            text="Icon 1", 
            is_stock_icon=False, 
            signature="sig1", 
            group="Types"
        )
        icon2 = mh.MindmapIcon(
            text="Icon 2", 
            is_stock_icon=False, 
            signature="sig2", 
            group="Types"
        )
        stock_icon = mh.MindmapIcon(
            text="Stock Icon", 
            is_stock_icon=True, 
            index=1
        )
        diff_group_icon = mh.MindmapIcon(
            text="Different Group", 
            is_stock_icon=False, 
            signature="sig3", 
            group="OtherGroup"
        )
        
        self.topic1.icons = [icon1, stock_icon]
        self.topic2.icons = [icon2, diff_group_icon]
        
        # Extract icons
        map_icons = []
        self.document.get_map_icons_and_fix_refs_from_mindmap(self.central, map_icons)
        
        # Should only have Types group, non-stock icons
        self.assertEqual(len(map_icons), 2)
        signatures = [icon.signature for icon in map_icons]
        self.assertIn("sig1", signatures)
        self.assertIn("sig2", signatures)
        
        # Test reference fixing
        self.assertEqual(id(self.topic1.icons[0]), id(map_icons[0]))  # Should be the same object
        
    def test_get_grounding_information(self):
        """Test extracting grounding information."""
        # Case 1: No selected topics
        self.document.selected_topic_texts = []
        self.document.selected_topic_levels = []
        self.document.selected_topic_ids = []
        self.document.central_topic_selected = False
        
        top_most, subtopics = self.document.get_grounding_information()
        self.assertEqual(top_most, "Central Topic")
        self.assertEqual(subtopics, "")
        
        # Case 2: Central topic selected with other topics
        self.document.selected_topic_texts = ["Topic 1", "Topic 2"]
        self.document.selected_topic_levels = [1, 1]
        self.document.selected_topic_ids = ["topic1", "topic2"]
        self.document.central_topic_selected = True
        
        top_most, subtopics = self.document.get_grounding_information()
        self.assertEqual(top_most, "Central Topic")
        self.assertEqual(subtopics, "Topic 1,Topic 2")
        
        # Case 3: Same level topics selected
        self.document.selected_topic_texts = ["Topic 1", "Topic 2"]
        self.document.selected_topic_levels = [1, 1]
        self.document.selected_topic_ids = ["topic1", "topic2"]
        self.document.central_topic_selected = False
        
        top_most, subtopics = self.document.get_grounding_information()
        self.assertEqual(top_most, "Central Topic")
        self.assertEqual(subtopics, "Topic 1,Topic 2")
        
        # Case 4: Mixed level topics selected
        self.document.selected_topic_texts = ["Topic 1", "Subtopic 1", "Subtopic 2"]
        self.document.selected_topic_levels = [1, 2, 2]
        self.document.selected_topic_ids = ["topic1", "subtopic1", "subtopic2"]
        self.document.central_topic_selected = False
        
        top_most, subtopics = self.document.get_grounding_information()
        self.assertEqual(top_most, "Topic 1")
        self.assertEqual(subtopics, "Subtopic 1,Subtopic 2")


if __name__ == '__main__':
    unittest.main()