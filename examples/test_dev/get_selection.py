import mindm.mindmanager as mm
import mindmap.serialization as mms
import json

m = mm.Mindmanager(macos_access="applescript")
selection = m.get_selection()
for topic in selection:
    print(json.dumps(mms.serialize_object_simple(topic)))
