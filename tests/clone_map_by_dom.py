#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mindm.mindmap_helper as mm
def main(charttype="auto"):
    document = mm.MindmapDocument(charttype=charttype)
    if not document.get_mindmap():
        return
    document.create_mindmap()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
