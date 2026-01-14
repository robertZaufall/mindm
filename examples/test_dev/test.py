import mindm.mindmanager as mgr
import mindmap.mindmap as mm
import mindmap.serialization as mms

# mindmanager tests
mindmanager = mgr.Mindmanager(macos_access='applescript')
platform = mindmanager.platform
mindmanager_object = mindmanager.get_mindmanager_object()
active_document_object = mindmanager.get_active_document_object()
library_folder_result = mindmanager.get_library_folder()
version_result = mindmanager.get_version()
document_exists_result = mindmanager.document_exists()
central_topic = mindmanager.get_central_topic() # full tree on macos
mindmap_topic_from_topic = 

# minmap tests
document = mm.MindmapDocument(charttype='auto', turbo_mode=True, macos_access='applescript')
selection = document.get_selection()
for topic in selection:
    pass

print("Done.")
