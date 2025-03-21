import mindmap.mindmap as mm

document = mm.MindmapDocument(turbo_mode=True)
document.get_mindmap(mode="content")
document.create_mindmap()
