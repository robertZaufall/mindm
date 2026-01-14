import mindmap.mindmap as mm

document = mm.MindmapDocument(turbo_mode=True, macos_access='applescript')
document.get_mindmap(mode="content")
document.create_mindmap()
