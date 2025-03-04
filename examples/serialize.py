import os
import yaml
import mindmap.mindmap as mindmap
import mindmap.serialization as mms

import json
from collections import deque

IGNORE_RTF = True

def main():

    document = mindmap.MindmapDocument(charttype="auto")
    document.get_mindmap()

    guid_mapping = {}
    mms.build_mapping(document.mindmap, guid_mapping)

    os.system('cls||clear')

    print("\n\n**************************************************\nJSON serialization\n**************************************************\n")

    serialize_simple_result = mms.serialize_object_simple(document.mindmap, ignore_rtf=IGNORE_RTF)
    print(json.dumps(serialize_simple_result, indent=1))

    print("\n\n**************************************************\nJSON serialization with GUID mapping\n**************************************************\n")

    serialize_result = mms.serialize_object(document.mindmap, guid_mapping, ignore_rtf=IGNORE_RTF)
    print(json.dumps(serialize_result, indent=1))

    print("\n\n**************************************************\nYAML serialization with GUID mapping\n**************************************************\n")
    yaml_data = mms.serialize_object(document.mindmap, guid_mapping, ignore_rtf=IGNORE_RTF)
    print(yaml.dump(yaml_data, sort_keys=False))

    print("\n\n**************************************************\nMermaid serialization, id only\n**************************************************\n")
    mermaid_id_only = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=True)
    print(mermaid_id_only)

    print("\n\n**************************************************\nMermaid serialization, full\n**************************************************\n")
    mermaid_data = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
    print(mermaid_data)

    print("\n\n**************************************************\nMermaid serialization, id only, deserialization, serialization\n**************************************************\n")

    data = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=True)
    print(data)
    deserialized_root = mms.deserialize_mermaid_with_id(data, guid_mapping)
    print(json.dumps(mms.serialize_object_simple(deserialized_root), indent=1))

    print("\n\n**************************************************\nMermaid serialization, full, deserialization, serialization\n**************************************************\n")
    data = mms.serialize_mindmap(document.mindmap, guid_mapping, id_only=False)
    print(data)
    deserialized_root = mms.deserialize_mermaid_full(data, guid_mapping)
    print(json.dumps(mms.serialize_object_simple(deserialized_root), indent=1))

    # create mindmap from deserialized data
    document.mindmap = deserialized_root
    document.create_mindmap()

    return

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
