import os

import mindm.mindmanager as mgr
import mindmap.mindmap as mm
import mindmap.serialization as mms
import pytest


def _require_smoke_enabled() -> None:
    if os.getenv("MINDM_SMOKE") != "1":
        pytest.skip("Set MINDM_SMOKE=1 to run MindManager smoke tests.")


def _macos_access() -> str:
    return os.getenv("MINDM_MACOS_ACCESS", "applescript")


def test_smoke_infrastructure() -> None:
    _require_smoke_enabled()
    mindmanager = mgr.Mindmanager(macos_access=_macos_access())
    assert isinstance(mindmanager.platform, str)
    assert isinstance(mindmanager.get_version(), str)
    assert isinstance(mindmanager.get_library_folder(), str)
    mindmanager.get_mindmanager_object()
    mindmanager.get_active_document_object()
    assert isinstance(mindmanager.document_exists(), bool)


def test_smoke_low_level_selection() -> None:
    _require_smoke_enabled()
    mindmanager = mgr.Mindmanager(macos_access=_macos_access())
    selection = mindmanager.get_selection()
    assert isinstance(selection, list)


def test_smoke_get_central_topic() -> None:
    _require_smoke_enabled()
    mindmanager = mgr.Mindmanager(macos_access=_macos_access())
    central = mindmanager.get_central_topic()
    assert central is not None


def test_smoke_selection() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(turbo_mode=True, macos_access=_macos_access())
    selection = document.get_selection()
    assert isinstance(selection, list)


def test_smoke_selection_extended() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(charttype="auto", turbo_mode=True, macos_access=_macos_access())
    selection = document.get_selection()
    assert isinstance(selection, list)


def test_smoke_serialization_json_simple() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    result = mms.serialize_object_simple(document.mindmap)
    assert isinstance(result, dict)


def test_smoke_serialization_json_full() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    guid_mapping: dict[str, int] = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    result = mms.serialize_object(document.mindmap, guid_mapping)
    assert isinstance(result, dict)
    assert "id" in result


def test_smoke_serialization_mermaid_simple() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    mermaid = mms.serialize_mindmap_simple(document.mindmap)
    assert mermaid.startswith("mindmap")


def test_smoke_serialization_mermaid_id_only() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    guid_mapping: dict[str, int] = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    mermaid = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=True)
    assert "id1[" in mermaid


def test_smoke_serialization_mermaid_full() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    guid_mapping: dict[str, int] = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    mermaid = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
    assert mermaid.startswith("mindmap")
    assert "%%" in mermaid


def test_smoke_deserialize_mermaid_with_id_live() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    guid_mapping: dict[str, int] = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    mermaid = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=True)
    root = mms.deserialize_mermaid_with_id(mermaid, guid_mapping)
    assert root.guid == document.mindmap.guid


def test_smoke_library_folder() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    assert isinstance(document.get_library_folder(), str)


def test_smoke_grounding_information() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    top, subtopics = document.get_grounding_information()
    assert isinstance(top, str)
    assert isinstance(subtopics, str)


def test_smoke_get_mindmap_text_mode() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap(mode="text")
    assert document.mindmap is not None


def test_smoke_deserialize_mermaid_simple_static() -> None:
    _require_smoke_enabled()
    mermaid = """
    mindmap
      Root
        Child A
        Child B
    """
    root = mms.deserialize_mermaid_simple(mermaid)
    assert root.text == "Root"
    assert [t.text for t in root.subtopics] == ["Child A", "Child B"]


def test_smoke_deserialize_mermaid_full_static() -> None:
    _require_smoke_enabled()
    mermaid = """
    mindmap
      [Root] %% {"id": 1}
        [Child] %% {"id": 2, "notes": {"text": "Note"}}
    """
    guid_mapping: dict[str, int] = {}
    root = mms.deserialize_mermaid_full(mermaid, guid_mapping)
    assert root.text == "Root"
    assert root.subtopics[0].notes is not None


def test_smoke_roundtrip_mermaid_full() -> None:
    _require_smoke_enabled()
    document = mm.MindmapDocument(macos_access=_macos_access())
    document.get_mindmap()
    guid_mapping: dict[str, int] = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    mermaid = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
    deserialized = mms.deserialize_mermaid_full(mermaid, guid_mapping)
    assert deserialized.text == document.mindmap.text
