---
name: mindm-mindmap
description: High-level MindManager mindmap operations via the mindm-mindmap CLI or python -m mindmap.actions. Use when a map must be read (mindmap, selection, grounding info), serialized to Mermaid, or created from Mermaid.
---

# Mindm Mindmap

## Overview

Use the mindm-mindmap CLI to query the current MindManager map or create a new
map from Mermaid. This skill targets high-level map operations that mirror the
MCP server capabilities.

## Quick start

Get the current mindmap as JSON:

```bash
uvx --from mindm mindm-mindmap get-mindmap --mode content
```

Get the current selection:

```bash
mindm-mindmap get-selection --mode content
```

Get grounding information:

```bash
mindm-mindmap get-grounding-information --mode content
```

Serialize to Mermaid:

```bash
mindm-mindmap serialize-mermaid
mindm-mindmap serialize-mermaid --mode full --id-only
```

Create a map from Mermaid:

```bash
mindm-mindmap create-from-mermaid --input /tmp/map.mmd
```

Create a map from Mermaid (full metadata or simplified indentation).
The CLI auto-detects the format.

Round-trip test (serialize → create):

```bash
mindm-mindmap serialize-mermaid --mode full | mindm-mindmap create-from-mermaid
```

## Notes

- Keep MindManager open with the target map active before running the CLI.
- For macOS, use --macos-access applescript (default) or appscript.
- For full flag details, read skills/mindm-mindmap/references/cli.md.
- For full Mermaid metadata (notes, links, icons, tags), read skills/mindm-mindmap/references/mermaid.md.
- JSON responses return the raw data for the command. Errors return {"error": "...", "message": "..."}.
