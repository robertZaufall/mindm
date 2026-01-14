from mindmap.mindmap import (
    MindmapDocument,
    MindmapIcon,
    MindmapLink,
    MindmapReference,
    MindmapTag,
    MindmapTopic,
)
from mindmap.mindmap import DUPLICATE_LABEL, DUPLICATED_TAG


class DummyTopic:
    def __init__(self, guid: str, text: str, level: int, parent=None):
        self.guid = guid
        self.text = text
        self.level = level
        self.parent = parent
        self.subtopics: list["DummyTopic"] = []


class DummyMindm:
    def __init__(self, selection=None, platform="darwin"):
        self._selection = selection or []
        self.platform = platform
        self.calls = []

    def get_level_from_topic(self, topic):
        return topic.level

    def get_parent_from_topic(self, topic):
        return topic.parent

    def get_guid_from_topic(self, topic):
        return topic.guid

    def get_text_from_topic(self, topic):
        return topic.text

    def get_selection(self):
        return self._selection

    def get_mindmaptopic_from_topic_full(self, topic):
        return MindmapTopic(guid=topic.guid, text=topic.text, level=topic.level)

    def get_mindmaptopic_from_topic_content(self, topic):
        return MindmapTopic(guid=topic.guid, text=topic.text, level=topic.level)

    def get_mindmaptopic_from_topic(self, topic):
        return MindmapTopic(guid=topic.guid, text=topic.text, level=topic.level)

    def get_subtopics_from_topic(self, topic):
        return topic.subtopics

    def add_document(self, index):
        self.calls.append(("add_document", index))

    def create_map_icons(self, icons):
        self.calls.append(("create_map_icons", icons))

    def create_tags(self, tags, duplicate_tag):
        self.calls.append(("create_tags", tags, duplicate_tag))

    def set_topic_from_mindmap_topic(self, topic, mindmap_topic, map_icons):
        self.calls.append(("set_topic_from_mindmap_topic", topic, mindmap_topic, map_icons))

    def add_topic_link(self, link_from, link_to, label):
        self.calls.append(("add_topic_link", link_from, link_to, label))

    def add_tag_to_topic(self, topic=None, tag_text="", topic_guid=""):
        self.calls.append(("add_tag_to_topic", topic, tag_text, topic_guid))

    def finalize(self, max_level):
        self.calls.append(("finalize", max_level))

    def set_document_background_image(self, image_path):
        self.calls.append(("set_document_background_image", image_path))


def _doc() -> MindmapDocument:
    return MindmapDocument.__new__(MindmapDocument)


def _tree() -> MindmapTopic:
    root = MindmapTopic(guid="root", text="Root", level=0)
    child = MindmapTopic(guid="child", text="Child", level=1)
    grand = MindmapTopic(guid="grand", text="Grand", level=2)
    root.subtopics = [child]
    child.parent = root
    child.subtopics = [grand]
    grand.parent = child
    return root


def test_get_max_topic_level_handles_cycles() -> None:
    doc = _doc()
    root = _tree()
    root.subtopics.append(root)
    max_level = doc.get_max_topic_level(root)
    assert max_level == 2


def test_get_parent_topic_returns_none_for_root() -> None:
    doc = _doc()
    doc.mindm = DummyMindm()
    root = DummyTopic("root", "Root", 0)
    assert doc.get_parent_topic(root) is None


def test_get_parent_topic_builds_chain() -> None:
    doc = _doc()
    doc.mindm = DummyMindm()
    root = DummyTopic("root", "Root", 0)
    child = DummyTopic("child", "Child", 1, parent=root)
    parent = doc.get_parent_topic(child)
    assert parent is not None
    assert parent.guid == "root"
    assert parent.parent is None


def test_get_selection_builds_selected_topics() -> None:
    root = DummyTopic("root", "Root", 0)
    child = DummyTopic("child", "Child", 1, parent=root)
    doc = _doc()
    doc.mindm = DummyMindm(selection=[root, child])
    selection = doc.get_selection()
    assert [t.guid for t in selection] == ["root", "child"]
    assert selection[0].selected is True
    assert selection[1].parent is not None
    assert doc.central_topic_selected is True
    assert doc.selected_topic_texts == ["Child"]
    assert doc.selected_topic_levels == [1]
    assert doc.selected_topic_ids == ["child"]


def test_get_mindmap_topic_from_topic_full_sets_parent() -> None:
    root = DummyTopic("root", "Root", 0)
    child = DummyTopic("child", "Child", 1, parent=root)
    root.subtopics = [child]
    doc = _doc()
    doc.mindm = DummyMindm()
    result = doc.get_mindmap_topic_from_topic(root, parent_topic=None, mode="full")
    assert result.subtopics[0].parent is result


def test_get_mindmap_topic_from_topic_text_builds_tree() -> None:
    root = DummyTopic("root", "Root", 0)
    child = DummyTopic("child", "Child", 1, parent=root)
    root.subtopics = [child]
    doc = _doc()
    doc.mindm = DummyMindm()
    result = doc.get_mindmap_topic_from_topic(root, parent_topic=None, mode="text")
    assert result.text == "Root"
    assert [t.text for t in result.subtopics] == ["Child"]


def test_get_relationships_from_mindmap_filters_direction() -> None:
    doc = _doc()
    root = _tree()
    root.references = [
        MindmapReference(guid_1="a", guid_2="b", direction=1, label="ok"),
        MindmapReference(guid_1="c", guid_2="d", direction=0, label="skip"),
    ]
    refs: list[MindmapReference] = []
    doc.get_relationships_from_mindmap(root, refs)
    assert [(r.guid_1, r.guid_2, r.direction) for r in refs] == [("a", "b", 1)]


def test_get_topic_links_from_mindmap_creates_references() -> None:
    doc = _doc()
    root = _tree()
    root.links = [MindmapLink(text="Link", url="u", guid="target")]
    refs: list[MindmapReference] = []
    doc.get_topic_links_from_mindmap(root, refs)
    assert [(r.guid_1, r.guid_2, r.label) for r in refs] == [("root", "target", "Link")]


def test_get_tags_from_mindmap_uniques() -> None:
    doc = _doc()
    root = _tree()
    root.tags = [MindmapTag(text="a"), MindmapTag(text="a"), MindmapTag(text="b")]
    tags: list[str] = []
    doc.get_tags_from_mindmap(root, tags)
    assert tags == ["a", "b"]


def test_get_parents_from_mindmap_builds_mapping() -> None:
    doc = _doc()
    root = _tree()
    parents: dict[str, str] = {}
    doc.get_parents_from_mindmap(root, parents)
    assert parents == {"child": "root", "grand": "child"}


def test_get_map_icons_and_fix_refs_from_mindmap_reuses_icons() -> None:
    doc = _doc()
    root = _tree()
    icon = MindmapIcon(text="Type", is_stock_icon=False, signature="sig", group="Types")
    root.icons = [icon]
    map_icons: list[MindmapIcon] = []
    doc.get_map_icons_and_fix_refs_from_mindmap(root, map_icons)
    assert len(map_icons) == 1
    assert root.icons[0] is map_icons[0]


def test_count_parent_and_child_occurrences_counts() -> None:
    doc = _doc()
    root = _tree()
    root.guid = ""
    counts: dict[str, dict[str, int]] = {}
    doc.count_parent_and_child_occurrences(root, counts)
    assert root.guid != ""
    assert counts[root.guid]["parent"] == 1


def test_get_topic_texts_from_selection_sets_state() -> None:
    doc = _doc()
    root = MindmapTopic(guid="r", text="Root", level=0, selected=True)
    child = MindmapTopic(guid="c", text="Child", level=1, selected=True)
    doc.get_topic_texts_from_selection([root, child])
    assert doc.central_topic_selected is True
    assert doc.selected_topic_texts == ["Child"]
    assert doc.selected_topic_levels == [1]
    assert doc.selected_topic_ids == ["c"]


def test_clone_mindmap_topic_copies_subtopics() -> None:
    doc = _doc()
    root = _tree()
    clone = doc.clone_mindmap_topic(root, subtopics=root.subtopics)
    assert clone is not root
    assert clone.text == root.text
    assert clone.subtopics and clone.subtopics[0] is not root.subtopics[0]


def test_check_parent_exists_recursive() -> None:
    doc = _doc()
    doc.parents = {"child": "root", "grand": "child"}
    assert doc.check_parent_exists("grand", "root") is True
    assert doc.check_parent_exists("root", "child") is False


def test_update_done_adds_links_and_tags() -> None:
    doc = _doc()
    doc.mindm = DummyMindm()
    topic = MindmapTopic(guid="dup", text="Topic")
    doc.guid_counts = {"dup": {"child": 0, "parent": 0}}
    done = {}
    done_global = {"dup": ["existing-guid"]}
    doc.update_done("new-guid", topic, 2, done, done_global)
    assert done_global["dup"] == ["existing-guid", "new-guid"]
    link_calls = [c for c in doc.mindm.calls if c[0] == "add_topic_link"]
    tag_calls = [c for c in doc.mindm.calls if c[0] == "add_tag_to_topic"]
    assert link_calls == [
        ("add_topic_link", "new-guid", "existing-guid", DUPLICATE_LABEL),
        ("add_topic_link", "existing-guid", "new-guid", DUPLICATE_LABEL),
    ]
    assert tag_calls == [
        ("add_tag_to_topic", None, DUPLICATED_TAG, "existing-guid"),
        ("add_tag_to_topic", None, DUPLICATED_TAG, "new-guid"),
    ]


def test_create_mindmap_darwin_applescript_path() -> None:
    doc = _doc()
    doc.macos_access = "applescript"
    doc.mindm = DummyMindm(platform="darwin")
    doc.get_mindmap = lambda *args, **kwargs: None
    root = _tree()
    root.tags = [MindmapTag(text="tag1")]
    root.icons = [MindmapIcon(text="Icon", is_stock_icon=False, signature="sig", group="Types")]
    root.links = [MindmapLink(text="Link", url="u", guid="target")]
    root.references = [MindmapReference(guid_1="root", guid_2="child", direction=1, label="rel")]
    doc.mindmap = root
    doc.create_mindmap()
    call_names = [c[0] for c in doc.mindm.calls]
    assert "add_document" in call_names
    assert "create_map_icons" in call_names
    assert "create_tags" in call_names
    assert "set_topic_from_mindmap_topic" in call_names


def test_finalize_computes_max_level() -> None:
    doc = _doc()
    doc.mindm = DummyMindm()
    doc.mindmap = _tree()
    doc.max_topic_level = 0
    doc.finalize()
    assert doc.max_topic_level == 2
    assert doc.mindm.calls[-1] == ("finalize", 2)


def test_set_background_image_calls_mindm() -> None:
    doc = _doc()
    doc.mindm = DummyMindm()
    doc.set_background_image("/tmp/bg.png")
    assert doc.mindm.calls[-1] == ("set_document_background_image", "/tmp/bg.png")


def test_get_grounding_information_no_selection() -> None:
    doc = _doc()
    doc.mindmap = MindmapTopic(guid="root", text="Root", level=0)

    def fake_selection():
        doc.central_topic_selected = False
        doc.selected_topic_texts = []
        doc.selected_topic_levels = []
        doc.selected_topic_ids = []
        return []

    doc.get_selection = fake_selection
    top, subtopics = doc.get_grounding_information()
    assert top == "Root"
    assert subtopics == ""


def test_get_grounding_information_central_selected() -> None:
    doc = _doc()
    doc.mindmap = MindmapTopic(guid="root", text="Root", level=0)

    def fake_selection():
        doc.central_topic_selected = True
        doc.selected_topic_texts = ["A", "B"]
        doc.selected_topic_levels = [1, 1]
        doc.selected_topic_ids = ["a", "b"]
        return []

    doc.get_selection = fake_selection
    top, subtopics = doc.get_grounding_information()
    assert top == "Root"
    assert subtopics == "A,B"


def test_get_grounding_information_mixed_levels() -> None:
    doc = _doc()
    doc.mindmap = MindmapTopic(guid="root", text="Root", level=0)

    def fake_selection():
        doc.central_topic_selected = False
        doc.selected_topic_texts = ["A", "B"]
        doc.selected_topic_levels = [1, 2]
        doc.selected_topic_ids = ["a", "b"]
        return []

    doc.get_selection = fake_selection
    top, subtopics = doc.get_grounding_information()
    assert top == "A"
    assert subtopics == "B"


def test_create_mindmap_and_finalize_calls_both() -> None:
    doc = _doc()
    calls = {"create": 0, "finalize": 0}
    doc.create_mindmap = lambda: calls.__setitem__("create", calls["create"] + 1)
    doc.finalize = lambda: calls.__setitem__("finalize", calls["finalize"] + 1)
    doc.create_mindmap_and_finalize()
    assert calls == {"create": 1, "finalize": 1}
