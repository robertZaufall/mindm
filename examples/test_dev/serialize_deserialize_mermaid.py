import json
import mindmap.mindmap as mm
import mindmap.serialization as mms

# irrelevant for windows
macos_access = "applescript"
#macos_access = "appscript"

document = mm.MindmapDocument(macos_access=macos_access)
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

serialized = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
print(serialized)

deserialized = mms.deserialize_mermaid_full(serialized, guid_mapping)
print(json.dumps(mms.serialize_object_simple(deserialized), indent=1))

document_new = mm.MindmapDocument(macos_access=macos_access)
document_new.mindmap = deserialized
document_new.create_mindmap()

print("Done")
