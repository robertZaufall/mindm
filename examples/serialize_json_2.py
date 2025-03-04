import json
import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

serialize_result = mms.serialize_object(document.mindmap, guid_mapping)
print(json.dumps(serialize_result, indent=1))
