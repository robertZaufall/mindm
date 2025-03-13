import json
import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

serialize_simple_result = mms.serialize_object_simple(document.mindmap)
print(json.dumps(serialize_simple_result, indent=1))
