from mindmap.mindmap import *
from mindmap import helpers

import json
import re
import uuid

IGNORE_RTF = True

def serialize_object(obj, guid_mapping, name='', visited=None, ignore_rtf=True):
    """Serialize an object recursively, handling special fields and mapping GUIDs to IDs.
    
    Args:
        obj: The object to serialize
        guid_mapping: Dictionary mapping GUIDs to numeric IDs
        name (str, optional): The name of the attribute being serialized. Defaults to ''.
        visited (set, optional): Set of object IDs that have been visited to prevent cycles. Defaults to None.
        ignore_rtf (bool, optional): Whether to ignore RTF content. Defaults to True.
        
    Returns:
        object: Serialized representation of the input object to be exported at JSON
    """
    if visited is None:
        visited = set()
    if name == 'topic':
        if id(obj) in visited:
            return None
        visited.add(id(obj))
    visited.add(id(obj))
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, list):
        attr_name = 'topic' if name == 'subtopics' else ''
        return [serialize_object(item, guid_mapping, attr_name, visited) for item in obj]
    if isinstance(obj, dict):
        return {str(k): serialize_object(v, guid_mapping, visited=visited) for k, v in obj.items()}
    if hasattr(obj, '__dict__'):
        serialized = {}
        for attr_name, attr_value in vars(obj).items():
            if attr_name in ["parent", "level", "selected"]: 
                continue
            if attr_name in ["rtf"]:
                if ignore_rtf == True:
                    continue
            if attr_value is None or attr_value == "" or attr_value == []:
                continue
            new_attr_name = attr_name
            if new_attr_name in ["guid", "guid_1", "guid_2"]:
                if new_attr_name == "guid":
                    new_attr_name = "id"
                elif new_attr_name == "guid_1":
                    new_attr_name = "id_1"
                elif new_attr_name == "guid_2":
                    new_attr_name = "id_2"
                serialized[new_attr_name] = guid_mapping[attr_value]
            else:
                dict_val = serialize_object(attr_value, guid_mapping, attr_name, visited)
                if dict_val != {}:
                    serialized[new_attr_name] = dict_val
        return serialized
    return str(obj)

def serialize_object_simple(obj, name='', visited=None, ignore_rtf=True):
    """Serialize an object recursively without GUID mapping.
    
    Args:
        obj: The object to serialize
        name (str, optional): The name of the attribute being serialized. Defaults to ''.
        visited (set, optional): Set of object IDs that have been visited to prevent cycles. Defaults to None.
        ignore_rtf (bool, optional): Whether to ignore RTF content. Defaults to True.
        
    Returns:
        object: Simplified serialized representation of the input object to be exported at JSON
    """
    if visited is None:
        visited = set()
    if name == 'topic':
        if id(obj) in visited:
            return None
        visited.add(id(obj))
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, list):
        attr_name = 'topic' if name == 'subtopics' else ''
        return [serialize_object_simple(item, attr_name, visited) for item in obj]
    if isinstance(obj, dict):
        return {str(k): serialize_object_simple(v, k, visited) for k, v in obj.items()}
    if hasattr(obj, '__dict__'):
        serialized = {}
        for attr_name, attr_value in vars(obj).items():
            if attr_name in ["parent", "level", "selected"]:
                continue
            if attr_name in ["rtf"]:
                if ignore_rtf == True:
                    continue
            if attr_value is None or attr_value == "" or attr_value == []:
                continue
            dict_val = serialize_object_simple(attr_value, attr_name, visited)
            if dict_val != {}:
                serialized[attr_name] = dict_val
        return serialized
    return str(obj)

def serialize_mindmap(root_topic, guid_mapping, id_only=False):
    """Serialize a mindmap to valid Mermaid format including id and all other attributes (optional).
    
    Args:
        root_topic (MindmapTopic): Root topic of the mindmap
        guid_mapping (dict): Dictionary mapping GUIDs to numeric IDs
        id_only (bool, optional): If True, only include IDs without detailed attributes. Defaults to False.
        
    Returns:
        str: Mermaid formatted string representing the mindmap
    """
    lines = ["mindmap"]

    def serialize_topic_attributes(topic, guid_mapping, ignore_rtf=True):
        """Extract and serialize the attributes of a MindmapTopic.
        
        Args:
            topic (MindmapTopic): The topic to serialize
            guid_mapping (dict): Dictionary mapping GUIDs to numeric IDs
            
        Returns:
            dict: Dictionary containing serialized topic attributes
        """
        d = {}
        d["id"] = guid_mapping.get(topic.guid, topic.guid)
        #d["text"] = topic.text
        if topic.rtf != topic.text and not ignore_rtf == True:
            d["rtf"] = topic.rtf
        if topic.selected == True:
            d["selected"] = topic.selected
        if topic.links:
            d["links"] = []
            for link in topic.links:
                l = {}
                if link.text:
                    l["text"] = link.text
                if link.url:
                    l["url"] = link.url
                if link.guid:
                    l["id"] = guid_mapping.get(link.guid, link.guid)
                d["links"].append(l)
        if topic.image:
            d["image"] = {"text": topic.image.text}
        if topic.icons:
            d["icons"] = []
            for icon in topic.icons:
                i = {}
                if icon.text:
                    i["text"] = icon.text
                if icon.is_stock_icon is not None:
                    i["is_stock_icon"] = icon.is_stock_icon
                if icon.index is not None:
                    i["index"] = icon.index
                if icon.signature:
                    i["signature"] = icon.signature
                if icon.path:
                    i["path"] = icon.path
                if icon.group:
                    i["group"] = icon.group
                d["icons"].append(i)
        if topic.notes and (topic.notes.text or topic.notes.xhtml or topic.notes.rtf):
            notes = {}
            if topic.notes.text:
                notes["text"] = topic.notes.text
            if topic.notes.xhtml:
                notes["xhtml"] = topic.notes.xhtml
            if topic.notes.rtf:
                notes["rtf"] = topic.notes.rtf
            if notes != {}:
                d["notes"] = notes
        if topic.tags:
            d["tags"] = [tag.text for tag in topic.tags]
        if topic.references:
            d["references"] = []
            for ref in topic.references:
                r = {}
                if ref.guid_1:
                    r["id_1"] = guid_mapping.get(ref.guid_1, ref.guid_1)
                if ref.guid_2:
                    r["id_2"] = guid_mapping.get(ref.guid_2, ref.guid_2)
                if ref.direction:
                    r["direction"] = ref.direction
                if ref.label:
                    r["label"] = ref.label
                d["references"].append(r)
        d = helpers.replace_unicode_in_obj(d)
        return d
    
    def traverse(topic, indent):
        indent_str = "  " * indent
        node_text = helpers.escape_mermaid_text(topic.text)
        if id_only:
            id = guid_mapping.get(topic.guid, topic.guid)
            line = f"{indent_str}id{id}[{node_text}]"
            #line = f"{indent_str}({node_text})"
            #topic_attrs = {"id": id}
        else:
            line = f"{indent_str}[{node_text}]"
            topic_attrs = serialize_topic_attributes(topic, guid_mapping, ignore_rtf=IGNORE_RTF)
            json_comment = json.dumps(topic_attrs, ensure_ascii=True)
            line += f" %% {json_comment}"
        lines.append(line)
        for sub in topic.subtopics:
            traverse(sub, indent + 1)

    traverse(root_topic, 1)
    return "\n".join(lines)


def serialize_mindmap_markdown(root_topic, include_notes=True):
    """Serialize a mindmap to markdown including notes (optional).
    
    Args:
        root_topic (MindmapTopic): Root topic of the mindmap
        include_notes (bool, optional): If True, notes are included
        
    Returns:
        str: Markdown formatted string representing the mindmap
    """

    import html2text
    import pypandoc

    lines = []
    
    def traverse(topic, lines, level, prefix, index):
        text = topic.text
        notes_text = ""
        notes_xhtml = ""
        notes_rtf = ""

        if level > 0:
            if prefix == '':
                prefix = str(index)
            else:
                prefix = f"{prefix}.{index}"
        
        if topic.notes and topic.notes.text or topic.notes.xhtml or topic.notes.rtf:
            if topic.notes.text:
                notes_text = topic.notes.text
            if topic.notes.xhtml:
                xhtml = topic.notes.xhtml
                root_match = re.search(r'<(?:root|body)[^>]*>(.*?)</(?:root|body)>', xhtml, re.DOTALL | re.IGNORECASE)
                if root_match:
                    xhtml = root_match.group(1)
                xhtml = re.sub(r'<\?xml[^>]*\?>', '', xhtml)
                xhtml = re.sub(r'<!DOCTYPE[^>]*>', '', xhtml)
                try:
                    h = html2text.HTML2Text()
                    h.ignore_links = False
                    h.ignore_images = False
                    h.body_width = 0  # Don't wrap lines
                    notes_xhtml = h.handle(xhtml).strip()
                except ImportError:
                    notes_xhtml = re.sub(r'<[^>]*>', '', xhtml).strip()
            if topic.notes.rtf:
                rtf = topic.notes.rtf
                try:
                    rtf = pypandoc.convert_text(rtf, to='md', format='rtf')
                except ImportError:
                    rtf = re.sub(r'\\[a-z]+\s*', '', rtf)
                    rtf = rtf.replace('{', '').replace('}', '')
                notes_rtf = rtf

        if include_notes and (notes_text or notes_xhtml or notes_rtf):
            notes = f"Notes: {notes_text or notes_xhtml or notes_rtf}  "
        else:
            notes = ""
        
        if topic.subtopics:
            line = f"{(level + 1) * '#'} {prefix if level > 0 else ''} {text}  "
            lines.append(line)
            if notes:
                lines.append(notes)

            sub_index = 0
            for sub in topic.subtopics:
                sub_index += 1
                traverse(sub, lines, level + 1, prefix, sub_index)
        else:
            line = f"- {text}  "
            lines.append(line)
            if notes:
                lines.append(notes)

    traverse(root_topic, lines, 0, '', 0)
    return "\n".join(lines)


def deserialize_mermaid_with_id(mermaid_text: str, guid_mapping: dict) -> MindmapTopic:
    """Convert Mermaid text with id to a Mindmap structure.
    
    Args:
        mermaid_text (str): Mermaid formatted string to parse
        guid_mapping (dict): Dictionary mapping numeric IDs to GUIDs
        
    Returns:
        MindmapTopic: Root topic of the deserialized mindmap
    """
    id_to_guid = {id_num: guid for guid, id_num in guid_mapping.items()}
    lines = [line for line in mermaid_text.splitlines() if line.strip()]
    if lines and lines[0].strip().lower() == "mindmap":
        lines = lines[1:]
    node_pattern = re.compile(r"^(id(\d+))\[(.*)\]$")
    root = None
    stack = []
    for line in lines:
        indent = len(line) - len(line.lstrip(" "))
        level = indent // 2
        stripped = line.lstrip(" ")
        match = node_pattern.match(stripped)
        if not match:
            continue        
        node_id_str = match.group(1)
        id_number = int(match.group(2))
        node_text = match.group(3)        
        if id_number in id_to_guid:
            guid = id_to_guid[id_number]
        else:
            guid = str(uuid.uuid4())
            id_to_guid[id_number] = guid
        node = MindmapTopic(guid=guid, text=node_text, level=level)
        if root is None:
            root = node
            stack.append((level, node))
            continue
        while stack and stack[-1][0] >= level:
            stack.pop()
        if stack:
            parent = stack[-1][1]
            node.parent = parent
            parent.subtopics.append(node)
        else:
            root.subtopics.append(node)
            node.parent = root
        stack.append((level, node))
    return root

def deserialize_mermaid_full(mermaid_text: str, guid_mapping: dict) -> MindmapTopic:
    """Convert Mermaid text with metadata to a Mindmap structure.
    
    Args:
        mermaid_text (str): Mermaid formatted string with JSON metadata to parse
        guid_mapping (dict): Dictionary mapping numeric IDs to GUIDs
        
    Returns:
        MindmapTopic: Root topic of the fully deserialized mindmap with all attributes
    """
    id_to_guid = {v: k for k, v in guid_mapping.items()}
    lines = [line for line in mermaid_text.splitlines() if line.strip()]
    if lines and lines[0].strip().lower() == "mindmap":
        lines = lines[1:]
    pattern = re.compile(r"^( *)(\[.*?\])\s*%%\s*(\{.*\})\s*$")
    root = None
    stack = []
    
    def restore_guid(numeric_id):
        try:
            num = int(numeric_id)
        except:
            return str(uuid.uuid4())
        if num in id_to_guid:
            return id_to_guid[num]
        else:
            new_guid = str(uuid.uuid4())
            id_to_guid[num] = new_guid
            return new_guid

    def process_subobject(field_dict: dict, id_field: str) -> dict:
        if id_field in field_dict:
            field_dict[id_field] = restore_guid(field_dict[id_field])
        return field_dict

    for line in lines:
        m = pattern.match(line)
        if not m:
            continue
        indent_str, bracket_part, json_part = m.groups()
        level = len(indent_str) // 2
        fallback_text = bracket_part.strip()[1:-1]
        try:
            attrs = json.loads(json_part)
        except Exception as e:
            attrs = {}
        if "id" in attrs:
            node_guid = restore_guid(attrs["id"])
        else:
            node_guid = str(uuid.uuid4())
        node_text = attrs.get("text", fallback_text)
        node_rtf = attrs.get("rtf", "")
        selected = attrs.get("selected", False)
        links = []
        if "links" in attrs and isinstance(attrs["links"], list):
            for link_dict in attrs["links"]:
                ld = dict(link_dict)
                ld = process_subobject(ld, "id")
                link_text = ld.get("text", "")
                link_url = ld.get("url", "")
                link_guid = ld.get("id", "")
                links.append(MindmapLink(text=link_text, url=link_url, guid=link_guid))
        image_obj = None
        if "image" in attrs and isinstance(attrs["image"], dict):
            image_obj = MindmapImage(text=attrs["image"].get("text", ""))
        icons = []
        if "icons" in attrs and isinstance(attrs["icons"], list):
            for icon_dict in attrs["icons"]:
                idict = dict(icon_dict)
                icons.append(MindmapIcon(
                    text=idict.get("text", ""),
                    is_stock_icon=idict.get("is_stock_icon", True),
                    index=idict.get("index", 1),
                    signature=idict.get("signature", ""),
                    path=idict.get("path", ""),
                    group=idict.get("group", "")
                ))
        notes_obj = None
        if "notes" in attrs:
            if isinstance(attrs["notes"], dict):
                notes_obj = MindmapNotes(
                    text=attrs["notes"].get("text", ""),
                    xhtml=attrs["notes"].get("xhtml", ""),
                    rtf=attrs["notes"].get("rtf", "")
                )
            elif isinstance(attrs["notes"], str):
                notes_obj = MindmapNotes(text=attrs["notes"])
        tags = []
        if "tags" in attrs and isinstance(attrs["tags"], list):
            for tag_item in attrs["tags"]:
                if isinstance(tag_item, dict):
                    tag_text = tag_item.get("text", "")
                else:
                    tag_text = str(tag_item)
                tags.append(MindmapTag(text=tag_text))
        references = []
        if "references" in attrs and isinstance(attrs["references"], list):
            for ref_dict in attrs["references"]:
                rd = dict(ref_dict)
                rd = process_subobject(rd, "id_1")
                rd = process_subobject(rd, "id_2")
                direction = rd.get("direction", None)
                label = rd.get("label", "")
                references.append(MindmapReference(
                    guid_1=rd.get("id_1", ""),
                    guid_2=rd.get("id_2", ""),
                    direction=direction,
                    label=label
                ))
        node = MindmapTopic(guid=node_guid, text=node_text, rtf=node_rtf, level=level, selected=selected)
        node.links = links
        node.image = image_obj
        node.icons = icons
        node.notes = notes_obj
        node.tags = tags
        node.references = references
        while stack and stack[-1][0] >= level:
            stack.pop()
        if stack:
            parent = stack[-1][1]
            node.parent = parent
            parent.subtopics.append(node)
        else:
            root = node
        stack.append((level, node))
    return root

def build_mapping(topic, guid_mapping):
    """Build a mapping of GUIDs to numeric IDs for an entire mindmap.
    
    Args:
        topic (MindmapTopic): Root topic of the mindmap
        guid_mapping (dict): Dictionary to store GUID to ID mappings
        
    Returns:
        None: The mapping is updated in-place
    """
    if topic.guid not in guid_mapping:
        guid_mapping[topic.guid] = len(guid_mapping) + 1
    for sub in topic.subtopics:
        build_mapping(sub, guid_mapping)
