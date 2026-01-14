from mindmap import helpers


def test_escape_mermaid_text_escapes_specials() -> None:
    text = 'Line "A"\\\nB\rΩ'
    escaped = helpers.escape_mermaid_text(text)
    assert escaped == "Line \\\"A\\\"\\\\\\nB\\u03a9"


def test_replace_unicode_in_obj_recursive() -> None:
    obj = {"a": ["x", {"b": "y"}], "c": 1}
    assert helpers.replace_unicode_in_obj(obj) == obj
