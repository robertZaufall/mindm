import yaml
import mindmap.mindmap as mm
import mindmap.serialization as mms

document = mm.MindmapDocument()
document.get_mindmap()

guid_mapping = {}
mms.build_mapping(document.mindmap, guid_mapping)

yaml_data = mms.serialize_object(document.mindmap, guid_mapping)
print(yaml.dump(yaml_data, sort_keys=False))
