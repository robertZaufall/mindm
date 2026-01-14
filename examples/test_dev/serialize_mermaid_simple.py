import mindmap.mindmap as mm
import mindmap.serialization as mms
import json

# irrelevant for windows
macos_access = "applescript"
#macos_access = "appscript"

document = mm.MindmapDocument(macos_access=macos_access)
document.get_mindmap()

mermaid = mms.serialize_mindmap_simple(document.mindmap)
print(mermaid)
