# Mindm Export CLI

## Location

- Console script: `mindm-export`
- Module entry point: `python -m mindmap.export`
- Exports the currently open MindManager map via `mindmap.serialization`.

## Recommended one-liner

Run without installing (uvx + PyPI):

```bash
uvx --from mindm mindm-export --type mermaid_html --open
```

## Core flags

- `--type {mermaid_html,markmap_html,markdown_html,mermaid,markmap,markdown,json,yaml}`.
- `yaml` requires `pyyaml`; the CLI only imports it when that type is used.
- `--open`: Write output to a file and open it.
- `--stream`: Write output to stdout (no file is written).
- `--output PATH`: Write to a specific path or directory.
- `--macos-access {applescript,appscript}`: Optional; default is `applescript`.

## Behavior details

- Default output path is `./docs/<uuid>` when using `mindm-export` or
  `python -m mindmap.export`.
- Extensions are chosen by `--type` (HTML, `.json`, `.yaml`, `.md`, or `.mmd`).
- `--stream` suppresses all other output; stdout is the selected format only.
- `--open` implies file output; the CLI prints the path before opening it.
- `markdown_html` exports also write a `.md` file next to the HTML file.

## Schema

- JSON schema for `json` lives at `docs/mindmap-json.schema.json`.
- YAML schema (mirrors `json`) lives at `docs/mindmap-yaml.schema.json`.

## Examples

Mermaid, default output path:

```bash
mindm-export --type mermaid_html
```

Markmap, open after export:

```bash
mindm-export --type markmap_html --open
```

Markdown, write to a specific file:

```bash
mindm-export --type markdown_html --output /tmp/mindmap.htm
```

YAML, stream to stdout:

```bash
mindm-export --type yaml --stream
```
