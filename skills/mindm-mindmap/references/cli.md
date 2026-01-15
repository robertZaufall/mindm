# mindm-mindmap CLI

## Entry points

- Console script: mindm-mindmap
- Module entry point: python -m mindmap.actions

## Commands

### Read

- get-mindmap
- get-selection
- get-grounding-information
- get-library-folder

### Serialize

- serialize-mermaid
  - Default output is simplified Mermaid (no %% JSON comments).
  - Use --mode full to include metadata comments; combine with --id-only to emit IDs only.

### Create

- create-from-mermaid
  - Auto-detects full Mermaid (with %% metadata comments) vs simplified Mermaid.
  - For metadata details (notes, links, icons, tags), see references/mermaid.md.

## Shared options

- --mode (full, content, text) for read and serialize commands
- --turbo-mode for text-only operations (default off)
- --charttype (auto, orgchart, radial)
- --macos-access (applescript, appscript)
- --json to force JSON output for text responses
- --pretty to pretty-print JSON

## Output shape

- JSON responses return the raw data for the command. Errors return {"error": "...", "message": "..."}.
- Text commands print raw output unless --json is provided.

## Create options

- --input /path/to/file.mmd
- --text "mermaid text"
- Or pipe Mermaid via stdin

## Examples

```bash
python -m mindmap.actions get-mindmap --mode content
mindm-mindmap serialize-mermaid --id-only
mindm-mindmap create-from-mermaid --text "mindmap\n  Root"
mindm-mindmap serialize-mermaid --mode full | mindm-mindmap create-from-mermaid
```
