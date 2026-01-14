import mindmap.mindmap as mm
import mindmap.serialization as mms
import json

document = mm.MindmapDocument(macos_access="applescript")
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

mermaid_data = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
print(mermaid_data)

#deserialized = mms.deserialize_mermaid_full(mermaid_data, guid_mapping)
#print(json.dumps(mms.serialize_object_simple(deserialized), indent=1))
