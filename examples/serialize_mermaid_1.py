import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

mermaid_id_only = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=True)
print(mermaid_id_only)
