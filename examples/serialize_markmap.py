import mindmap.mindmap as mm
import mindmap.serialization as mms

import os
import sys
import uuid
import markdown

MARKMAP_TEMPLATE = """
<div class="markmap">
<script type="text/template">
---
markmap:
colorFreezeLevel: {{colorFreezeLevel}}
initialExpandLevel: -1
---
{{markmap}}
</script>
</div>
"""

HTML_TEMPLATE = """
<!DOCTYPE html><html lang="en">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{title}}</title>
<style>
svg.markmap{width:100%;height:100vh;}
</style>
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@latest"></script>
</head><body>
{{body}}
</body></html>
"""

def generate_html(content, guid):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "docs")
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    this_content = MARKMAP_TEMPLATE.replace("{{colorFreezeLevel}}", "3").replace("{{markmap}}", content)
    template = HTML_TEMPLATE
    html = template.replace("{{body}}", this_content).replace("{{title}}", "Markmap")
    file_path = os.path.join(folder_path, f"{guid}.html")
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(html)
    if sys.platform.startswith('darwin'):
        os.system(f"open {file_path}")
    elif sys.platform.startswith('win'):
        import subprocess
        subprocess.Popen(f'cmd /k start explorer.exe "{file_path}"', shell=False)

document = mm.MindmapDocument()
document.get_mindmap(mode='content')

md = mms.serialize_mindmap_markdown(document.mindmap, include_notes=False)

guid = uuid.uuid4()
generate_html(md, guid)