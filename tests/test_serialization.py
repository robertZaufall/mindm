import json

from mindmap.mindmap import (
    MindmapIcon,
    MindmapImage,
    MindmapLink,
    MindmapNotes,
    MindmapReference,
    MindmapTag,
    MindmapTopic,
)
import mindmap.serialization as mms


def _build_sample_tree() -> MindmapTopic:
    root = MindmapTopic(guid="root-guid", text='Root "A"')
    root.notes = MindmapNotes(text="Root note")
    root.tags = [MindmapTag(text="tag-1")]
    root.links = [MindmapLink(text="Link", url="http://x", guid="link-guid")]
    root.image = MindmapImage(text="/tmp/image.png")
    root.icons = [
        MindmapIcon(text="Icon", is_stock_icon=True, index=1, signature="sig", group="Types")
    ]
    root.references = [
        MindmapReference(guid_1="root-guid", guid_2="child-guid", direction=1, label="ref")
    ]

    child = MindmapTopic(guid="child-guid", text="Child")
    child.notes = MindmapNotes(text="Child note")
    root.subtopics.append(child)
    child.parent = root
    return root


def test_mindmap_topic_sanitizes_text() -> None:
    topic = MindmapTopic(guid="g", text="A \"B\"\nC")
    assert topic.text == "A `B`C"


def test_build_mapping_assigns_sequential_ids() -> None:
    root = _build_sample_tree()
    mapping: dict[str, int] = {}
    mms.build_mapping(root, mapping)
    assert mapping == {"root-guid": 1, "child-guid": 2}


def test_serialize_mindmap_simple_indentation() -> None:
    root = _build_sample_tree()
    output = mms.serialize_mindmap_simple(root)
    assert output.splitlines()[:3] == ["mindmap", "  Root `A`", "    Child"]


def test_serialize_mindmap_markdown_includes_notes() -> None:
    root = _build_sample_tree()
    output = mms.serialize_mindmap_markdown(root, include_notes=True)
    assert "Notes: Root note" in output
    assert "Notes: Child note" in output


def test_serialize_mindmap_full_includes_json_metadata() -> None:
    root = _build_sample_tree()
    mapping: dict[str, int] = {}
    mms.build_mapping(root, mapping)
    output = mms.serialize_mindmap(root, mapping, id_only=False)
    assert "%%" in output
    assert "\"id\"" in output


def test_serialize_mindmap_id_only_prefix() -> None:
    root = _build_sample_tree()
    mapping: dict[str, int] = {}
    mms.build_mapping(root, mapping)
    output = mms.serialize_mindmap(root, mapping, id_only=True)
    assert "id1[" in output


def test_deserialize_mermaid_with_id_uses_mapping() -> None:
    mapping = {"guid-a": 1}
    mermaid = "mindmap\n  id1[Root]"
    root = mms.deserialize_mermaid_with_id(mermaid, mapping)
    assert root.guid == "guid-a"


def test_deserialize_mermaid_full_roundtrip() -> None:
    root = _build_sample_tree()
    mapping: dict[str, int] = {}
    mms.build_mapping(root, mapping)
    mermaid = mms.serialize_mindmap(root, mapping, id_only=False)
    deserialized = mms.deserialize_mermaid_full(mermaid, mapping)
    assert deserialized.text == root.text
    assert deserialized.subtopics[0].text == "Child"


def test_serialize_object_simple_excludes_rtf_and_parent() -> None:
    root = _build_sample_tree()
    root.rtf = "{rtf}"
    child = root.subtopics[0]
    child.rtf = "{rtf-child}"
    result = mms.serialize_object_simple(root)
    assert "rtf" not in json.dumps(result)
    assert "parent" not in result
    assert result["guid"] == "root-guid"


def test_serialize_object_full_maps_ids() -> None:
    root = _build_sample_tree()
    mapping: dict[str, int] = {}
    mms.build_mapping(root, mapping)
    mapping["link-guid"] = 3
    result = mms.serialize_object(root, mapping)
    assert result["id"] == 1
    assert result["subtopics"][0]["id"] == 2


def test_deserialize_mermaid_simple_parses_comments_and_brackets() -> None:
    mermaid = """
    mindmap
      [Root]
        Child %% comment
      Sibling
    """
    root = mms.deserialize_mermaid_simple(mermaid)
    assert root.text == "Root"
    assert [t.text for t in root.subtopics] == ["Child", "Sibling"]
