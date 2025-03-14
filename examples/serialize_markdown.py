import mindmap.mindmap as mm
import mindmap.serialization as mms

import os
import sys
import uuid
import markdown

HTML_TEMPLATE = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />  
<title>{{title}}</title><style>
body{font-family:Helvetica,Arial,sans-serif;} 
h2{margin-block-start:0;margin-block-end:0} 
hr{margin-block-start:0;margin-block-end:0}
ul{margin-block-start:8px}
</style></head><body>
{{body}}
</body></html>
"""

def generate_html(content, guid):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "docs")
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    with open(os.path.join(folder_path, f"{guid}.md"), 'w', encoding="utf-8") as f:
        f.write(content)
    html = HTML_TEMPLATE.replace("{{title}}", "Mindmap").replace("{{body}}", markdown.markdown(content).replace("</h2>", "</h2><hr/>"))
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

md = mms.serialize_mindmap_markdown(document.mindmap)

guid = uuid.uuid4()
generate_html(md, guid)