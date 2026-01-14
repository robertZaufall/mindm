import mindmap.mindmap as mmap
import mindm.mindmanager as mm

document = mmap.MindmapDocument()
library_path = document.get_library_folder()
print(f"Library path: {library_path}")

mindmanager = mm.Mindmanager()
version = mindmanager.get_version()
print(f"Version: {version}")
platform = mindmanager.platform
print(f"Platform: {platform}")

mindmanager_object = mindmanager.get_mindmanager_object()
document_object = mindmanager.get_active_document_object()

print("Done.")
