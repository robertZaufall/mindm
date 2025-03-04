import mindmap.mindmap as mm

# load and clone mindmap to new a document
document = mm.MindmapDocument()
if not document.get_mindmap():
    print("No mindmap found.")
else:
    document.create_mindmap()
