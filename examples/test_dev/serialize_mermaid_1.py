import mindmap.mindmap as mm
import mindmap.serialization as mms
import json

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

mermaid_id_only = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=True)
print(mermaid_id_only)

#deserialized = mms.deserialize_mermaid_with_id(mermaid_id_only, guid_mapping)
#print(json.dumps(mms.serialize_object_simple(deserialized), indent=1))
