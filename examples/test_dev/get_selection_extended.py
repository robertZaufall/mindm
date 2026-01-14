import mindmap.mindmap as mm
import mindmap.serialization as mms
import json

document = mm.MindmapDocument(charttype='auto', turbo_mode=True, macos_access='applescript')
selection = document.get_selection()
for topic in selection:
    print(json.dumps(mms.serialize_object_simple(topic)))
