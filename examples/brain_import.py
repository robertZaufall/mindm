#!/usr/bin/env python3
import os
import json
from collections import Counter

import mindmap.mindmap as mm

def get_generic(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def get_mindmap_from_brain(thoughts, links, attachments, file_path):
    id_to_tag_topic = {}
    for thought in thoughts:
        kind = thought.get('Kind')
        if kind == 4:
            id_to_tag_topic[thought['Id']] = thought['Name']

    thought_id_to_tag_links = {}
    for thought in thoughts:
        thought_tag_links = []
        for link in links:
            if link['ThoughtIdB'] == thought['Id'] and link['ThoughtIdA'] in id_to_tag_topic:
                thought_tag_links.append(link['ThoughtIdA'])
        if len(thought_tag_links) > 0:
            thought_id_to_tag_links[thought['Id']] = thought_tag_links

    id_to_topic = {}
    for thought in thoughts:
        kind = thought.get('Kind')
        if kind in [3, 4, 5]:
            continue
        thought_id = thought.get('Id')
        tags = []
        if thought_id in thought_id_to_tag_links:
            for tag_id in thought_id_to_tag_links[thought_id]:
                tag_name = id_to_tag_topic[tag_id]
                tags.append(mm.MindmapTag(text=tag_name))
        topic = mm.MindmapTopic(guid=thought['Id'], text=thought.get('Name', ''), level=0, tags=tags)
        id_to_topic[thought['Id']] = topic
    
    child_ids = set()
    for link in links:
        direction = link.get('Direction', 0)
        meaning = link.get('Meaning', '')
        kind = link.get('Kind', '')
        relation = link.get('Relation', '')
        parent_id = link['ThoughtIdA']
        child_id = link['ThoughtIdB']
        if direction == -1 and meaning in [1] and relation in [1] and kind in [1]:
            if parent_id in id_to_topic and child_id in id_to_topic:
                parent_topic = id_to_topic[parent_id]
                child_topic = id_to_topic[child_id]
                child_topic.topic_parent = parent_topic
                parent_topic.subtopics.append(child_topic)
                child_ids.add(child_id)
    
    root_topics = [t for t_id, t in id_to_topic.items() if t_id not in child_ids]
    central_topic = mm.MindmapTopic(guid='central_brain_topic', text='Brain', level=0)
    num_root_topics_with_subtopics = sum(1 for root in root_topics if len(root.subtopics) > 1)
    if num_root_topics_with_subtopics == 1:
        for root in root_topics:
            if len(root.subtopics) > 0:
                central_topic = root
    else:
        for root in root_topics:
            if len(root.subtopics) > 0:
                root.topic_parent = central_topic
                central_topic.subtopics.append(root)
    return central_topic

def import_file(file_path):
    thoughts = get_generic(os.path.join(file_path, "thoughts.json"))
    links = get_generic(os.path.join(file_path, "links.json"))
    attachments = get_generic(os.path.join(file_path, "attachments.json"))

    document = mm.MindmapDocument()
    document.mindmap = get_mindmap_from_brain(thoughts, links, attachments, file_path)
    document.create_mindmap()

def main():
    # *********************
    file_path = 'C://brain'
    # *********************

    import_file(file_path)

if __name__ == "__main__":
    try:
        main()
        print("Done.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
