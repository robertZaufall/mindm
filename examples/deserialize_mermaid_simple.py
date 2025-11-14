import json
import mindmap.mindmap as mm
import mindmap.serialization as mms

# irrelevant for windows
macos_access = "applescript"
#macos_access = "appscript"

mermaid = """
mindmap
  Creating an AI startup
    Vision & Strategy
      Mission and Value
        Problem statement
        Value proposition
        Long term goals
      Competitive Positioning
        Differentiation pillars
        Key competitors map
        Barrier strategies
    Product & Tech
      MVP Design
        Core feature set
        User flows map
        Rapid prototyping
"""

document = mm.MindmapDocument(macos_access=macos_access)
deserialized = mms.deserialize_mermaid_simple(mermaid)
print(json.dumps(mms.serialize_object_simple(deserialized), indent=1))
document_new = mm.MindmapDocument(macos_access=macos_access)
document_new.mindmap = deserialized
document_new.create_mindmap()

print("Done")
