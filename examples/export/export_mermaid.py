import mindmap.mindmap as mm
import mindmap.serialization as mms

import os
import sys
import uuid

MERMAID_TEMPLATE= """
<div class="mermaid">
%%{init: {"theme": "light"}}%% 
{{mermaid}}
</div>
"""

HTML_TEMPLATE = """
<!DOCTYPE html><html lang="en">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{title}}</title>
<style>
svg.mermaid{width:100%;height:100vh;}
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>document.addEventListener('DOMContentLoaded', () => { mermaid.initialize({ startOnLoad: true }); });</script>  
</head><body>
{{body}}
</body></html>
"""

def generate_html(content, guid, open_file = False):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "docs")
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    this_content = MERMAID_TEMPLATE.replace("{{mermaid}}", content)
    template = HTML_TEMPLATE
    html = template.replace("{{body}}", this_content).replace("{{title}}", "Mermaid")
    file_path = os.path.join(folder_path, f"{guid}.html")
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(html)

    if open_file:
        if sys.platform.startswith('darwin'):
            os.system(f"open {file_path}")
        elif sys.platform.startswith('win'):
            import subprocess
            subprocess.Popen(f'cmd /k start explorer.exe "{file_path}"', shell=False)

document = mm.MindmapDocument(macos_access='applescript')
document.get_mindmap(mode='content')

md = mms.serialize_mindmap_simple(document.mindmap)

guid = uuid.uuid4()
generate_html(md, guid, open_file=True)