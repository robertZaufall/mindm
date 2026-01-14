import argparse
import json
import os
import subprocess
import sys
import uuid
from typing import Optional, Sequence, Tuple

import markdown
import mindmap.mindmap as mm
import mindmap.serialization as mms

MARKMAP_DATA_TEMPLATE = """---
markmap:
colorFreezeLevel: {{colorFreezeLevel}}
initialExpandLevel: -1
---
{{markmap}}
"""

MARKMAP_TEMPLATE = """
<div class="markmap">
<script type="text/template">
{{markmap}}
</script>
</div>
"""

MERMAID_TEMPLATE = """
<div class="mermaid">
%%{init: {"theme": "light"}}%%
{{mermaid}}
</div>
"""

MARKMAP_HTML_TEMPLATE = """
<!DOCTYPE html><html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{title}}</title>
<style>
svg.markmap{width:100%;height:100vh;}
</style>
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@latest"></script>
</head><body>
{{body}}
</body></html>
"""

MERMAID_HTML_TEMPLATE = """
<!DOCTYPE html><html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{title}}</title>
<style>
svg.mermaid{width:100%;height:100vh;}
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  mermaid.initialize({ startOnLoad: true });
});
</script>
</head><body>
{{body}}
</body></html>
"""

MARKDOWN_HTML_TEMPLATE = """
<!DOCTYPE html><html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{title}}</title>
<style>
body{font-family:Helvetica,Arial,sans-serif;}
h2{margin-block-start:0;margin-block-end:0}
hr{margin-block-start:0;margin-block-end:0}
ul{margin-block-start:8px}
</style>
</head><body>
{{body}}
</body></html>
"""


def build_markmap_data(markdown_text: str) -> str:
    return MARKMAP_DATA_TEMPLATE.replace("{{colorFreezeLevel}}", "3").replace(
        "{{markmap}}", markdown_text
    )


def build_markmap_html(markmap_text: str) -> str:
    content = MARKMAP_TEMPLATE.replace("{{markmap}}", markmap_text)
    html = MARKMAP_HTML_TEMPLATE.replace("{{title}}", "Markmap")
    return html.replace("{{body}}", content)


def build_mermaid_html(mermaid_text: str) -> str:
    content = MERMAID_TEMPLATE.replace("{{mermaid}}", mermaid_text)
    html = MERMAID_HTML_TEMPLATE.replace("{{title}}", "Mermaid")
    return html.replace("{{body}}", content)


def build_markdown_html(markdown_text: str) -> str:
    body_html = markdown.markdown(markdown_text)
    body_html = body_html.replace("</h2>", "</h2><hr/>")
    html = MARKDOWN_HTML_TEMPLATE.replace("{{title}}", "Mindmap")
    return html.replace("{{body}}", body_html)


def open_file(path: str) -> None:
    if sys.platform.startswith("darwin"):
        subprocess.Popen(["open", path])
    elif sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    else:
        subprocess.Popen(["xdg-open", path])


def export_extension(export_type: str) -> str:
    if export_type.endswith("_html"):
        return ".htm"
    if export_type == "json":
        return ".json"
    if export_type == "yaml":
        return ".yaml"
    if export_type == "mermaid":
        return ".mmd"
    if export_type in ("markmap", "markdown"):
        return ".md"
    return ".txt"


def resolve_output_path(
    output: Optional[str], export_type: str, docs_dir: Optional[str] = None
) -> str:
    extension = export_extension(export_type)
    if output:
        if os.path.isdir(output):
            os.makedirs(output, exist_ok=True)
            return os.path.join(os.path.abspath(output), f"{uuid.uuid4()}{extension}")

        output_path = os.path.abspath(output)
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        return output_path

    if docs_dir is None:
        docs_dir = os.path.join(os.getcwd(), "docs")
    os.makedirs(docs_dir, exist_ok=True)
    return os.path.join(docs_dir, f"{uuid.uuid4()}{extension}")


def mermaid(document: mm.MindmapDocument) -> str:
    return mms.serialize_mindmap_simple(document.mindmap)


def markmap(document: mm.MindmapDocument) -> str:
    markdown_text = mms.serialize_mindmap_markdown(
        document.mindmap, include_notes=False
    )
    return build_markmap_data(markdown_text)


def markdown_data(document: mm.MindmapDocument) -> str:
    return mms.serialize_mindmap_markdown(document.mindmap, include_notes=True)


def export_json(document: mm.MindmapDocument) -> str:
    guid_mapping = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    data = mms.serialize_object(document.mindmap, guid_mapping)
    return json.dumps(data, indent=1)


def export_yaml(document: mm.MindmapDocument) -> str:
    import yaml

    guid_mapping = {}
    mms.build_mapping(document.mindmap, guid_mapping)
    data = mms.serialize_object(document.mindmap, guid_mapping)
    return yaml.dump(data, sort_keys=False)


def mermaid_html(
    document: mm.MindmapDocument, mermaid_text: Optional[str] = None
) -> str:
    if mermaid_text is None:
        mermaid_text = mermaid(document)
    return build_mermaid_html(mermaid_text)


def markmap_html(
    document: mm.MindmapDocument, markmap_text: Optional[str] = None
) -> str:
    if markmap_text is None:
        markmap_text = markmap(document)
    return build_markmap_html(markmap_text)


def markdown_html(
    document: mm.MindmapDocument, markdown_text: Optional[str] = None
) -> str:
    if markdown_text is None:
        markdown_text = markdown_data(document)
    return build_markdown_html(markdown_text)


def export_mindmap(export_type: str, macos_access: str) -> Tuple[str, str]:
    document = mm.MindmapDocument(macos_access=macos_access)
    document.get_mindmap(mode="content")

    if export_type == "mermaid_html":
        data = mermaid(document)
        return data, mermaid_html(document, data)

    if export_type == "markmap_html":
        data = markmap(document)
        return data, markmap_html(document, data)

    if export_type == "markdown_html":
        data = markdown_data(document)
        return data, markdown_html(document, data)

    if export_type == "json":
        data = export_json(document)
        return data, data

    if export_type == "yaml":
        data = export_yaml(document)
        return data, data

    if export_type == "mermaid":
        data = mermaid(document)
        return data, data

    if export_type == "markmap":
        data = markmap(document)
        return data, data

    data = markdown_data(document)
    return data, data


def write_output(output_path: str, output: str, source: str, export_type: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    if export_type == "markdown_html":
        markdown_path = os.path.splitext(output_path)[0] + ".md"
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(source)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export the current MindManager mindmap to HTML or data-only output "
            "for mermaid, markmap, markdown, JSON, or YAML."
        )
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=(
            "mermaid_html",
            "markmap_html",
            "markdown_html",
            "json",
            "yaml",
            "mermaid",
            "markmap",
            "markdown",
        ),
        help="Export type to generate (HTML or data-only).",
    )
    parser.add_argument(
        "--output",
        help=(
            "Output file path. Defaults to docs/<uuid> plus an extension based on "
            "--type."
        ),
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--open",
        action="store_true",
        help="Open the generated output file after export.",
    )
    mode_group.add_argument(
        "--stream",
        action="store_true",
        help="Write the generated output to stdout instead of writing a file.",
    )
    parser.add_argument(
        "--macos-access",
        default="applescript",
        choices=("applescript", "appscript"),
        help="macOS MindManager access method.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None, docs_dir: Optional[str] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    source, output = export_mindmap(args.type, args.macos_access)

    if args.stream:
        sys.stdout.write(output)
        return 0

    output_path = resolve_output_path(args.output, args.type, docs_dir=docs_dir)
    write_output(output_path, output, source, args.type)
    print(output_path)

    if args.open:
        open_file(output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
