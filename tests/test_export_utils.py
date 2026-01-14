from pathlib import Path

from mindmap import export as mm_export


def test_export_extension_map() -> None:
    assert mm_export.export_extension("mermaid_html") == ".htm"
    assert mm_export.export_extension("json") == ".json"
    assert mm_export.export_extension("yaml") == ".yaml"
    assert mm_export.export_extension("mermaid") == ".mmd"
    assert mm_export.export_extension("markmap") == ".md"
    assert mm_export.export_extension("markdown") == ".md"
    assert mm_export.export_extension("other") == ".txt"


def test_resolve_output_path_defaults_to_docs_dir(tmp_path: Path) -> None:
    output = mm_export.resolve_output_path(None, "json", docs_dir=str(tmp_path))
    assert output.startswith(str(tmp_path))
    assert output.endswith(".json")


def test_resolve_output_path_directory(tmp_path: Path) -> None:
    output = mm_export.resolve_output_path(str(tmp_path), "markdown_html")
    assert output.startswith(str(tmp_path))
    assert output.endswith(".htm")


def test_build_markmap_data_includes_header() -> None:
    data = mm_export.build_markmap_data("# Title")
    assert "markmap:" in data
    assert "# Title" in data


def test_build_markdown_html_adds_hr() -> None:
    html = mm_export.build_markdown_html("## Title")
    assert "</h2><hr/>" in html


def test_build_mermaid_html_contains_script() -> None:
    html = mm_export.build_mermaid_html("mindmap\n  A")
    assert "<div class=\"mermaid\">" in html
    assert "mermaid.min.js" in html


def test_build_markmap_html_contains_script() -> None:
    html = mm_export.build_markmap_html("## Title")
    assert "<div class=\"markmap\">" in html
    assert "markmap-autoloader" in html


def test_resolve_output_path_file_creates_dir(tmp_path: Path) -> None:
    output_path = tmp_path / "nested" / "out.htm"
    resolved = mm_export.resolve_output_path(str(output_path), "mermaid_html")
    assert resolved == str(output_path)
    assert (tmp_path / "nested").exists()


def test_open_file_darwin(monkeypatch) -> None:
    calls = {}

    def fake_popen(args):
        calls["args"] = args

    monkeypatch.setattr(mm_export.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(mm_export.sys, "platform", "darwin")
    mm_export.open_file("/tmp/example.htm")
    assert calls["args"] == ["open", "/tmp/example.htm"]


def test_main_stream(monkeypatch, capsys) -> None:
    def fake_export(_export_type: str, _macos_access: str):
        return "source", "stream-output"

    monkeypatch.setattr(mm_export, "export_mindmap", fake_export)
    result = mm_export.main(["--type", "json", "--stream"])
    captured = capsys.readouterr()
    assert result == 0
    assert captured.out == "stream-output"
