import json
import os

import pytest

from mindmap import export as mm_export


def _require_smoke_enabled() -> None:
    if os.getenv("MINDM_SMOKE") != "1":
        pytest.skip("Set MINDM_SMOKE=1 to run MindManager smoke exports.")


def _macos_access() -> str:
    return os.getenv("MINDM_MACOS_ACCESS", "applescript")


def test_export_json_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("json", _macos_access())[1]
    data = json.loads(output)
    assert isinstance(data, dict)


def test_export_mermaid_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("mermaid", _macos_access())[1]
    assert output.startswith("mindmap")


def test_export_mermaid_html_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("mermaid_html", _macos_access())[1]
    assert "<div class=\"mermaid\">" in output
    assert "mermaid.min.js" in output


def test_export_markmap_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("markmap", _macos_access())[1]
    assert output.startswith("---")
    assert "markmap:" in output


def test_export_markmap_html_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("markmap_html", _macos_access())[1]
    assert "<div class=\"markmap\">" in output
    assert "markmap-autoloader" in output


def test_export_markdown_html_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("markdown_html", _macos_access())[1]
    assert "<body>" in output
    assert "</h2><hr/>" in output or "<ul" in output


def test_export_markdown_smoke() -> None:
    _require_smoke_enabled()
    output = mm_export.export_mindmap("markdown", _macos_access())[1]
    assert isinstance(output, str) and output.strip()


def test_export_yaml_smoke() -> None:
    _require_smoke_enabled()
    try:
        import yaml  # noqa: F401
    except Exception:
        pytest.skip("pyyaml is not installed.")
    output = mm_export.export_mindmap("yaml", _macos_access())[1]
    assert isinstance(output, str) and output.strip()
