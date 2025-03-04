import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

mermaid_data = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
print(mermaid_data)
