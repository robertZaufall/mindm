import json
import mindmap.mindmap as mm
import mindmap.serialization as mms

# irrelevant for windows
macos_access = "applescript"
#macos_access = "appscript"

mermaid = """
mindmap
  [Creating an AI startup] %% {"id": 1}
    [Vision & Strategy] %% {"id": 2}
      [Mission and Value] %% {"id": 3}
        [Problem statement] %% {"id": 4}
        [Value proposition] %% {"id": 5}
        [Long term goals] %% {"id": 6}
      [Competitive Positioning] %% {"id": 7}
        [Differentiation pillars] %% {"id": 8}
        [Key competitors map] %% {"id": 9}
        [Barrier strategies] %% {"id": 10}
    [Product & Tech] %% {"id": 19}
      [MVP Design] %% {"id": 20}
        [Core feature set] %% {"id": 21, "notes": {"text": "Some Notes"}, "icons": [{"type": "star"}]}
        [User flows map] %% {"id": 22, "links": [{"text": "label", "url": "https://example.com"}]}
        [Rapid prototyping] %% {"id": 23, "references": [{"id_1": 23, "id_2": 6, "direction": 1}]}
        [Topic] %% {"id": 24, "notes": {"text": "Notes"}, "references": [{"id_1": 24, "id_2": 5, "direction": 1}], "links": [{"text": "label", "url": "https://example.com"}], "image": {"text": "C:\\path\\to\\image.png"}, "icons": [{"text": "StockIcon-36", "is_stock_icon": true, "index": 36}], "tags": ["tag1"]}
"""

guid_mapping = {}
deserialized = mms.deserialize_mermaid_full(mermaid, guid_mapping)
print(json.dumps(mms.serialize_object_simple(deserialized), indent=1))
document_new = mm.MindmapDocument(macos_access=macos_access)
document_new.mindmap = deserialized
document_new.create_mindmap()

serialized = mms.serialize_mindmap(document_new.mindmap, guid_mapping, id_only=False)
print(serialized)

print("Done")
