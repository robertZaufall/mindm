import json

from mindmap import actions as mm_cli


def test_main_get_mindmap_outputs_json(monkeypatch, capsys) -> None:
    def fake_get_mindmap(*_args, **_kwargs):
        return {"root": {"text": "A"}}

    monkeypatch.setattr(mm_cli, "get_mindmap", fake_get_mindmap)

    result = mm_cli.main(["get-mindmap"])
    captured = capsys.readouterr()

    assert result == 0
    assert json.loads(captured.out) == {"root": {"text": "A"}}


def test_main_serialize_mermaid_raw(monkeypatch, capsys) -> None:
    def fake_serialize(*_args, **_kwargs):
        return "mindmap\n  A"

    monkeypatch.setattr(
        mm_cli, "serialize_current_mindmap_to_mermaid", fake_serialize
    )

    result = mm_cli.main(["serialize-mermaid"])
    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == "mindmap\n  A"


def test_main_error_exit(monkeypatch, capsys) -> None:
    def fake_get_selection(*_args, **_kwargs):
        return {"error": "MindManager Error", "message": "No document"}

    monkeypatch.setattr(mm_cli, "get_selection", fake_get_selection)

    result = mm_cli.main(["get-selection"])
    captured = capsys.readouterr()

    assert result == 1
    assert json.loads(captured.out)["error"] == "MindManager Error"
