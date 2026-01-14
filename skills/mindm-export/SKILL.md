---
name: mindm-export
description: Export MindManager mindmaps to Mermaid, Markmap, Markdown, JSON, or YAML (HTML or data-only). Use when output must be generated or streamed, or when a map must be opened.
---

# Mindm Export

## Overview

Export the current MindManager map to HTML or data-only output. Preferred
one-liner is `uvx` (no install). Also available via `mindm-export` or
`python -m mindmap.export`. Choose `mermaid_html`, `markmap_html`,
`markdown_html`, or the data-only `mermaid`, `markmap`, `markdown`,
`json`, `yaml`.

## Quick start

Run an export and open it (recommended, no install):

```bash
uvx --from mindm mindm-export --type mermaid_html --open
```

Run an export and open it (installed console script):

```bash
mindm-export --type mermaid_html --open
```

Run via the module entry point (source checkout):

```bash
python -m mindmap.export --type json --output /tmp/mindmap.json
```

Stream HTML to stdout:

```bash
mindm-export --type markmap --stream
```

Write to a specific file path:

```bash
mindm-export --type markdown_html --output /tmp/mindmap.htm
```

## Notes

- Keep MindManager open with the target map active before running the CLI.
- For macOS access, use `--macos-access applescript` (default) or `--macos-access appscript`.
- For deeper flag and behavior details, read `skills/mindm-export/references/cli.md`.
